#!/usr/bin/env bash
# Run every service's unit tests (standard library only, no dependencies).
set -euo pipefail
cd "$(dirname "$0")/.."
status=0
for dir in services/*/; do
  [ -d "$dir/tests" ] || continue
  echo "== ${dir%/}"
  (cd "$dir" && python3 -m unittest discover -s tests -q) || status=1
done
exit $status
