# GhostBusters

A small pygame game about finding a ghost hidden on a grid. You can't see the
ghost, but you can probe cells with a sensor and watch the ghost's position
being tracked by a **Hidden Markov Model**: every cell shows the current
probability that the ghost is there, and it updates after each probe and each
time step (forward filtering).

## How to play

1. Pick the number of rows and columns in the start menu and press **Play**.
2. Click any grid cell to probe it. The cell lights up:
   - **Red**: the ghost is within Manhattan distance 2.
   - **Orange**: mid range.
   - **Green**: far away.

   The probabilities on the board update immediately.
3. Click **TIME** (bottom left) to let the ghost move one step. The belief is
   pushed through the movement model, then the real ghost moves.
4. Click **CATCH** (bottom right), then click the cell you think the ghost is
   in. The board shows **CAUGHT** or **MISSED** and marks the ghost's real
   position in gray.
5. Press **Esc** to go back to the menu, or close the window to quit.

The ghost moves to an orthogonal neighbour with high probability, to a diagonal
neighbour with low probability, and occasionally stays put. The sensor in this
version never lies. Both models live in `ghostbusters/hmm.py` and can be tuned
there (for example by moving mass off the diagonal of `EMISSION` to make the
sensor noisy).

## Running it on a new machine

Requirements: `git`, and either [pyenv](https://github.com/pyenv/pyenv) or a
Python 3.9+ interpreter on your `PATH`. The project pins Python 3.12.13 in
`.python-version`; pyenv picks that up automatically.

```bash
git clone <this repo> && cd GhostBusters
./run.sh
```

`run.sh` calls `setup.sh` the first time, which installs the pinned Python with
pyenv (if pyenv is available), creates a virtualenv in `.venv` and installs the
dependencies from `requirements.txt`. After that it just starts the game.

Manual equivalent:

```bash
pyenv install --skip-existing          # reads .python-version
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py                          # or: python -m ghostbusters
```

If you use [uv](https://github.com/astral-sh/uv) instead, this works out of the
box:

```bash
uv run main.py
```

## Development

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

The tests cover the probabilistic model only (transition rows sum to one, the
belief stays normalised and never drops the real ghost, zone thresholds, and so
on). The pygame code is kept thin so that the model stays testable without a
display.

## Project layout

```
main.py                   convenience entry point (python main.py)
ghostbusters/
  __main__.py             python -m ghostbusters
  app.py                  start menu, size validation, launches a game
  play.py                 event loop (clicks, Esc, quit)
  game.py                 game state: real ghost, cell colours, click handling
  board.py                drawing: cells, labels, TIME/CATCH bar
  hmm.py                  pure-Python HMM: transition + sensor model, belief
  constants.py            window size, board limits, colours
tests/test_hmm.py         unit tests for the model
setup.sh / run.sh         environment bootstrap and launcher
requirements*.txt         runtime / dev dependencies
pyproject.toml            package metadata (pip install -e . also works)
.python-version           Python version for pyenv / uv
```
