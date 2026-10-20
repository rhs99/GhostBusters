"""Hidden Markov Model of a ghost wandering on a grid.

This module is pure Python (no pygame) so the probabilistic model can be
unit-tested on its own. The model has two parts:

* Transition model: at each time step the ghost moves to an orthogonal
  neighbour, a diagonal neighbour, or stays put. The weight of each move
  depends on how many orthogonal neighbours the source cell has
  (2 = corner, 3 = edge, 4 = interior) so that the weights of all legal
  moves from a cell sum to 1.
* Sensor model: probing a cell reports a colour that depends on the
  Manhattan distance from the probed cell to the ghost. RED means close,
  ORANGE mid-range and GREEN far. ``EMISSION`` gives P(reading | zone).

``GhostHMM`` keeps the belief distribution over the ghost's position and
updates it with the forward algorithm (``advance_time`` and ``observe``).
"""

from __future__ import annotations

import math
import random
from typing import Dict, Iterator, List, Optional, Tuple

Cell = Tuple[int, int]

RED, ORANGE, GREEN = "red", "orange", "green"
READINGS = (RED, ORANGE, GREEN)

ORTHOGONAL = ((0, 1), (0, -1), (1, 0), (-1, 0))
DIAGONAL = ((-1, 1), (1, 1), (1, -1), (-1, -1))

# Keyed by the number of orthogonal neighbours of the source cell.
STRAIGHT_WEIGHT = {2: 0.48, 3: 0.32, 4: 0.24}
DIAGONAL_WEIGHT = {2: 0.036, 3: 0.018, 4: 0.009}
STAY_WEIGHT = 0.004

# P(reading | zone). The identity matrix means the sensor never lies;
# move mass off the diagonal to make the game harder.
EMISSION: Dict[str, Dict[str, float]] = {
    RED: {RED: 1.0, ORANGE: 0.0, GREEN: 0.0},
    ORANGE: {RED: 0.0, ORANGE: 1.0, GREEN: 0.0},
    GREEN: {RED: 0.0, ORANGE: 0.0, GREEN: 1.0},
}


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class GhostHMM:
    """Belief state over the ghost's position plus the sampling helpers
    the game uses to move the real ghost and to read the sensor."""

    def __init__(self, rows: int, cols: int, rng: Optional[random.Random] = None):
        if rows < 2 or cols < 2:
            raise ValueError("grid must be at least 2x2")
        self.rows = rows
        self.cols = cols
        self.rng = rng if rng is not None else random.Random()

        # Zone radii (Manhattan distance). Everything past orange is green.
        self.red_radius = 2
        remaining = rows + cols - 2 - self.red_radius
        self.orange_radius = self.red_radius + math.ceil(remaining / 2)

        self.belief: List[List[float]] = []
        self.reset()

    # ----- grid helpers -------------------------------------------------

    def reset(self) -> None:
        """Start from a uniform belief: the ghost could be anywhere."""
        p = 1.0 / (self.rows * self.cols)
        self.belief = [[p] * self.cols for _ in range(self.rows)]

    def cells(self) -> Iterator[Cell]:
        for r in range(self.rows):
            for c in range(self.cols):
                yield (r, c)

    def in_bounds(self, cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < self.rows and 0 <= c < self.cols

    def random_cell(self) -> Cell:
        return (self.rng.randrange(self.rows), self.rng.randrange(self.cols))

    def zone(self, distance: int) -> str:
        if distance <= self.red_radius:
            return RED
        if distance <= self.orange_radius:
            return ORANGE
        return GREEN

    # ----- transition model ---------------------------------------------

    def transitions(self, cell: Cell) -> Dict[Cell, float]:
        """P(next cell | current cell) for every reachable next cell."""
        r, c = cell
        straight = [(r + dr, c + dc) for dr, dc in ORTHOGONAL]
        straight = [n for n in straight if self.in_bounds(n)]
        diagonal = [(r + dr, c + dc) for dr, dc in DIAGONAL]
        diagonal = [n for n in diagonal if self.in_bounds(n)]

        kind = len(straight)  # 2 corner, 3 edge, 4 interior
        probs: Dict[Cell, float] = {}
        for n in straight:
            probs[n] = STRAIGHT_WEIGHT[kind]
        for n in diagonal:
            probs[n] = DIAGONAL_WEIGHT[kind]
        probs[cell] = STAY_WEIGHT

        total = sum(probs.values())
        return {dst: p / total for dst, p in probs.items()}

    def advance_time(self) -> None:
        """Forward step: push the belief through the transition model."""
        new = [[0.0] * self.cols for _ in range(self.rows)]
        for src in self.cells():
            mass = self.belief[src[0]][src[1]]
            if mass == 0.0:
                continue
            for (r, c), p in self.transitions(src).items():
                new[r][c] += mass * p
        self.belief = new
        self._normalize()

    def sample_move(self, cell: Cell) -> Cell:
        """Draw the ghost's next position from the transition model."""
        trans = self.transitions(cell)
        return self.rng.choices(list(trans), weights=list(trans.values()))[0]

    # ----- sensor model -------------------------------------------------

    def sample_reading(self, probe: Cell, ghost: Cell) -> str:
        """Draw a sensor reading for probing ``probe`` while the ghost is at ``ghost``."""
        row = EMISSION[self.zone(manhattan(probe, ghost))]
        return self.rng.choices(READINGS, weights=[row[x] for x in READINGS])[0]

    def observe(self, probe: Cell, reading: str) -> None:
        """Bayesian update of the belief after reading ``reading`` at ``probe``."""
        for r, c in self.cells():
            zone = self.zone(manhattan(probe, (r, c)))
            self.belief[r][c] *= EMISSION[zone][reading]
        self._normalize()

    # ----- internals ----------------------------------------------------

    def _normalize(self) -> None:
        total = sum(sum(row) for row in self.belief)
        if total <= 0.0:
            # Every hypothesis was ruled out, which only happens with a
            # sensor model that contradicts itself. Start over rather
            # than divide by zero.
            self.reset()
            return
        self.belief = [[p / total for p in row] for row in self.belief]
