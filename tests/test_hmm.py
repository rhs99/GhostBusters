import math
import random

import pytest

from ghostbusters import hmm
from ghostbusters.hmm import GhostHMM


def total(model):
    return sum(sum(row) for row in model.belief)


@pytest.mark.parametrize("rows,cols", [(2, 2), (2, 3), (3, 3), (6, 6), (4, 9)])
def test_transitions_are_distributions_over_in_bounds_cells(rows, cols):
    model = GhostHMM(rows, cols)
    for cell in model.cells():
        trans = model.transitions(cell)
        assert math.isclose(sum(trans.values()), 1.0)
        assert all(model.in_bounds(dst) for dst in trans)
        assert all(p > 0 for p in trans.values())
        assert cell in trans  # the ghost may stay put


def test_transition_weights_match_cell_kind():
    model = GhostHMM(6, 6)
    corner, edge, interior = (0, 0), (0, 3), (3, 3)
    assert len(model.transitions(corner)) == 4  # 2 straight + 1 diagonal + stay
    assert len(model.transitions(edge)) == 6  # 3 straight + 2 diagonal + stay
    assert len(model.transitions(interior)) == 9
    assert math.isclose(model.transitions(interior)[(3, 4)], hmm.STRAIGHT_WEIGHT[4])
    assert math.isclose(model.transitions(interior)[(4, 4)], hmm.DIAGONAL_WEIGHT[4])
    assert math.isclose(model.transitions(interior)[(3, 3)], hmm.STAY_WEIGHT)


def test_zones_for_6x6():
    model = GhostHMM(6, 6)
    assert model.red_radius == 2
    assert model.orange_radius == 6
    assert [model.zone(d) for d in range(0, 11)] == (
        [hmm.RED] * 3 + [hmm.ORANGE] * 4 + [hmm.GREEN] * 4
    )


def test_initial_belief_is_uniform():
    model = GhostHMM(3, 4)
    assert all(math.isclose(p, 1 / 12) for row in model.belief for p in row)


def test_advance_time_from_certainty_equals_transition_row():
    model = GhostHMM(5, 5)
    model.belief = [[0.0] * 5 for _ in range(5)]
    model.belief[2][2] = 1.0
    model.advance_time()
    expected = model.transitions((2, 2))
    for (r, c), p in expected.items():
        assert math.isclose(model.belief[r][c], p)
    assert math.isclose(total(model), 1.0)


def test_observe_red_rules_out_far_cells_and_renormalises():
    model = GhostHMM(6, 6)
    model.observe((0, 0), hmm.RED)
    assert math.isclose(total(model), 1.0)
    for r, c in model.cells():
        if hmm.manhattan((0, 0), (r, c)) <= model.red_radius:
            assert model.belief[r][c] > 0
        else:
            assert model.belief[r][c] == 0


def test_sample_move_only_uses_legal_moves():
    model = GhostHMM(4, 4, rng=random.Random(1))
    ghost = (0, 0)
    for _ in range(200):
        ghost = model.sample_move(ghost)
        assert model.in_bounds(ghost)


def test_noiseless_sensor_reports_true_zone():
    model = GhostHMM(6, 6, rng=random.Random(0))
    ghost = (5, 5)
    assert model.sample_reading((5, 5), ghost) == hmm.RED
    assert model.sample_reading((1, 5), ghost) == hmm.ORANGE
    assert model.sample_reading((0, 0), ghost) == hmm.GREEN


def test_belief_never_loses_the_true_ghost():
    """Filtering with truthful readings must keep positive belief on the ghost."""
    rng = random.Random(42)
    model = GhostHMM(6, 6, rng=rng)
    ghost = model.random_cell()
    for _ in range(100):
        if rng.random() < 0.5:
            probe = model.random_cell()
            model.observe(probe, model.sample_reading(probe, ghost))
        else:
            model.advance_time()
            ghost = model.sample_move(ghost)
        assert model.belief[ghost[0]][ghost[1]] > 0
        assert math.isclose(total(model), 1.0)


@pytest.mark.parametrize("rows,cols", [(1, 5), (5, 1), (0, 0)])
def test_rejects_tiny_grids(rows, cols):
    with pytest.raises(ValueError):
        GhostHMM(rows, cols)
