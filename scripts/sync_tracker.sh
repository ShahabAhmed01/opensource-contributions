#!/usr/bin/env bash
# Sync the contribution tracker with GitHub and push when the ledger changed.
# Used by the optional local systemd user timer as a fallback while the
# GitHub Actions workflow is unavailable.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/update_tracker.py

if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
  exit 0
fi

git add -A
git commit -m "chore: sync contribution status"
git push
