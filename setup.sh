#!/usr/bin/env bash
# One-time setup: install the pinned Python with pyenv (if available),
# create a virtualenv in .venv and install the dependencies.
set -euo pipefail
cd "$(dirname "$0")"

PY_VERSION="$(cat .python-version)"

if command -v pyenv >/dev/null 2>&1; then
    echo "Installing Python $PY_VERSION with pyenv (skipped if present)..."
    pyenv install --skip-existing "$PY_VERSION"
    PYTHON="$(PYENV_VERSION="$PY_VERSION" pyenv which python)"
else
    echo "pyenv not found; using python3 from PATH (want $PY_VERSION)." >&2
    PYTHON="python3"
fi

echo "Using $("$PYTHON" --version) at $PYTHON"
"$PYTHON" -m venv .venv
.venv/bin/python -m pip install --upgrade pip --quiet
.venv/bin/python -m pip install -r requirements-dev.txt

echo
echo "Done. Start the game with ./run.sh"
