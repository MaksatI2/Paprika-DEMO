#!/usr/bin/env bash
# Simulate a release of one service before a Paprika demo: bump its version and push.
#
#   scripts/simulate-release.sh checkout 12.6.2            # branch + push; open the PR from the printed link
#   scripts/simulate-release.sh checkout 12.6.2 --direct   # commit straight to main (a deployment is recorded)
#
# Paprika then sees the commit, the pull request and the deployment through the GitHub MCP:
# the incident's Recent Changes tab, the Release Regression Agent and WF06 use them.
set -euo pipefail
svc=${1:?usage: simulate-release.sh <service> <version> [--direct]}
ver=${2:?usage: simulate-release.sh <service> <version> [--direct]}
mode=${3:-pr}
cd "$(git rev-parse --show-toplevel)"
[ -f "services/$svc/VERSION" ] || { echo "unknown service: $svc" >&2; exit 1; }

git fetch -q origin main
git checkout -q main
git pull -q --ff-only origin main
old=$(cat "services/$svc/VERSION")
branch="release/$svc-$ver"
[ "$mode" = "--direct" ] || git checkout -q -b "$branch"

echo "$ver" > "services/$svc/VERSION"
sed -i.bak "s#\(image: ghcr.io/acme/$svc:\).*#\1$ver#" "deploy/production/$svc.yaml"
rm -f "deploy/production/$svc.yaml.bak"
git add "services/$svc/VERSION" "deploy/production/$svc.yaml"
git commit -q -m "release($svc): $ver" -m "Bumps $svc from $old to $ver."

if [ "$mode" = "--direct" ]; then
  git push -q origin main
  echo "Pushed to main. The Deploy workflow records a production deployment of $svc $ver."
else
  git push -q -u origin "$branch"
  git checkout -q main
  echo "Open and merge the PR: https://github.com/paprikabit-labs/Paprika_demo/compare/main...$branch?expand=1"
fi
