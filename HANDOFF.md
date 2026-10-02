# Contribution Handoff

Updated: 2026-10-03T00:05:00Z

## Current Project

odysseus-dev/odysseus — self-hosted AI workspace (Python/FastAPI, AGPL-3.0)

## Current Issue

[#2740 — Resolve SQLAlchemy 2.0 deprecation warnings in core/database.py](https://github.com/odysseus-dev/odysseus/issues/2740)

## Current PR

[#6453 — fix(core): import declarative_base and declared_attr from sqlalchemy.orm](https://github.com/odysseus-dev/odysseus/pull/6453)

- Base branch: `dev` (correct target)
- State: open, mergeable
- Automated PR checks: description ✅, title ✅, unmergeable ✅
- CI workflows (`CI`, CodeQL, secret scan, container scan, dependency review):
  **`action_required`** — GitHub requires a maintainer to approve workflow runs
  for a first-time contributor. This is not a failure and must not be bypassed.
- Copilot review: quota notice only, no actionable feedback.

## Current Branch

`fix/sqlalchemy-declarative-import-2740` (fork: `ShahabAhmed01/odysseus`)

## Current Commit

`45d372b2481ae4f46b0134572304a9075c70cc0f` — 22 files, +22/−23

## Current CI State

Awaiting maintainer approval to run. Local validation is complete and green:
full suite `5952 passed, 4 skipped`; `compileall` clean; zero `MovedIn20Warning`
lines; app run healthy (`/api/health` 200, `/api/version` 200, tables created).

## Current Review State

No human review yet.

## Current Blocker

Two one-time human actions remain:

1. **GitHub Actions `workflow` scope** — required to publish the tracker's
   scheduled sync workflow:
   `gh auth refresh -s workflow`
   (browser/device authorization; no secret is pasted anywhere).
2. Nothing else is blocked. CI approval is the maintainer's call.

## Durable monitoring

- Public tracker: https://github.com/ShahabAhmed01/opensource-contributions
- Local fallback: systemd user timer `odysseus-tracker.timer` (every 6 h) runs
  `scripts/sync_tracker.sh`, which pushes only when the ledger changed.
- Once the `workflow` scope is granted, the pending
  `.github/workflows/track-contributions.yml` can be committed and the local
  timer can be disabled.

## Next Action

1. Watch PR #6453 for maintainer CI approval, review comments, and merge.
2. Respond to any substantive review feedback on the same branch.
3. On merge: verify the merge commit on `dev`, update this ledger, close out
   the contribution record, then select the next issue.

## Resume Instruction

RESUME CONTRIBUTIONS
