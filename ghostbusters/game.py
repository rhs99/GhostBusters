"""Game state: the real ghost, the player's belief, and click handling."""

import random
from typing import List, Optional

import pygame

from . import hmm
from .board import Board
from .constants import BLACK, GRAY, GREEN, ORANGE, RED, YELLOW1, YELLOW2

READING_COLOURS = {hmm.RED: RED, hmm.ORANGE: ORANGE, hmm.GREEN: GREEN}


class Game:
    def __init__(self, win: pygame.Surface, rows: int, cols: int, rng: Optional[random.Random] = None):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.board = Board(win, rows, cols)
        self.model = hmm.GhostHMM(rows, cols, rng)
        self.ghost = self.model.random_cell()

        self.base_colours: List[List[tuple]] = [
            [YELLOW1 if (r + c) % 2 == 0 else YELLOW2 for c in range(cols)] for r in range(rows)
        ]
        self.cell_colours: List[List[tuple]] = []
        self.message = ""
        self.catch_mode = False
        self.reset_colours()

    # ----- rendering ----------------------------------------------------

    def reset_colours(self) -> None:
        self.cell_colours = [row[:] for row in self.base_colours]
        self.message = ""

    def draw(self) -> None:
        self.win.fill(BLACK)
        for r, c in self.model.cells():
            label = f"{self.model.belief[r][c]:.3f}"
            self.board.draw_cell(r, c, self.cell_colours[r][c], label)
        self.board.draw_controls(self.message)

    # ----- actions ------------------------------------------------------

    def probe(self, row: int, col: int) -> None:
        """Take a sensor reading at a cell and update the belief."""
        reading = self.model.sample_reading((row, col), self.ghost)
        self.cell_colours[row][col] = READING_COLOURS[reading]
        self.model.observe((row, col), reading)

    def advance_time(self) -> None:
        """Push the belief one step forward, then move the real ghost."""
        self.model.advance_time()
        self.ghost = self.model.sample_move(self.ghost)

    def reveal(self, row: int, col: int) -> None:
        """Attempt to catch the ghost at a cell; show where it really is."""
        self.message = "CAUGHT" if (row, col) == self.ghost else "MISSED"
        self.cell_colours[self.ghost[0]][self.ghost[1]] = GRAY

    def handle_click(self, row: int, col: int) -> None:
        if self.model.in_bounds((row, col)):
            self.reset_colours()
            if self.catch_mode:
                self.reveal(row, col)
                self.catch_mode = False
            else:
                self.probe(row, col)
        elif row == self.rows and col == 0:
            self.reset_colours()
            self.advance_time()
            self.catch_mode = False
        elif row == self.rows and col == self.cols - 1:
            self.reset_colours()
            self.catch_mode = True
