# odysseus-dev/odysseus — #5049

## Status

In review

## Issue

https://github.com/odysseus-dev/odysseus/issues/5049
"Scheduled research crashes on a non-numeric research_max_tokens in settings.json"

## Pull Request

[#6473 — fix(scheduler): fall back to defaults for non-numeric research settings](https://github.com/odysseus-dev/odysseus/pull/6473)

- Base branch: `dev`
- Opened: 2026-10-03
- State: open, mergeable
- Fork head: `ShahabAhmed01:fix/scheduler-research-settings-guard-5049`

## Branch

`fix/scheduler-research-settings-guard-5049`

## Commits

- `35e3b298f4a5b7c8d9e0f1a2b3c4d5e6f7a8b9c0` — fix(scheduler): fall back to defaults for non-numeric research settings

## Context

Open child of maintainer subtracker #5335 with explicit acceptance criteria.
Prior PR #5050 (another contributor) was closed unmerged in the 2026-07-23
transfer and never resubmitted — this redo credits that history.

## Problem

`src/task_scheduler.py` reads the three research settings with
`int(get_setting("research_max_tokens", 8192))` and friends. A non-numeric
value in `settings.json` raises `ValueError` and the scheduled research task
crashes instead of falling back.

## Solution

Wrap the three reads (`research_max_tokens`, `research_extraction_timeout_seconds`,
`research_extraction_concurrency`) in try/except and fall back to the
documented defaults `8192` / `90` / `3`.

## Files Changed

- `src/task_scheduler.py` — guarded reads with default fallbacks
- `tests/test_scheduler_research_settings_guard.py` — focused tests

## Tests

- Focused suite for the guard behaviour
- Syntax: `compileall` clean

## CI

PR checks passing (description, Conventional Commits, unmergeable). The
`CI`/`CodeQL`/scan workflows are `action_required` pending maintainer approval
for a first-time contributor — an expected gate, not a failure.

## Review

No maintainer review yet.

## Merge

Not merged.

## Notes

Reconciled against live GitHub state 2026-10-09; upstream/dev still reads the
settings unguarded, so the fix is still required.
