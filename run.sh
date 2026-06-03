#!/usr/bin/env bash
#
# run.sh — convenience wrapper for the mouse-jiggler utilities.
#
# Usage:
#   ./run.sh                       # start the mouse jiggler loop (default)
#   ./run.sh jiggle                # start the mouse jiggler loop
#   ./run.sh type "<text>"         # auto-type literal text after a 5s countdown
#   ./run.sh type @path/to/file    # auto-type the contents of a file
#   ./run.sh sync                  # install/sync dependencies from uv.lock
#   ./run.sh help                  # show this help

set -euo pipefail

# Run from the script's own directory so relative paths work anywhere.
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: 'uv' is not installed. See https://docs.astral.sh/uv/" >&2
  exit 1
fi

usage() {
  sed -n '3,12p' "$0" | sed 's/^# \{0,1\}//'
}

cmd="${1:-jiggle}"

case "$cmd" in
  jiggle|main)
    uv run python main.py
    ;;
  type)
    if [ $# -lt 2 ]; then
      echo "Error: 'type' needs an argument (text or @file)." >&2
      echo "Example: ./run.sh type \"hello world\"" >&2
      exit 1
    fi
    uv run python type.py "$2"
    ;;
  sync)
    uv sync
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo >&2
    usage >&2
    exit 1
    ;;
esac
