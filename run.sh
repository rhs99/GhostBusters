#!/usr/bin/env bash
# Run the game, setting up the environment first if needed.
set -euo pipefail
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || ./setup.sh
exec .venv/bin/python -m ghostbusters "$@"
