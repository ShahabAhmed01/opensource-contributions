# brekkylab/backlot — #586

## Status

**PR OPEN, AWAITING REVIEW** — PR #620 opened 2026-10-11T16:45:32Z, ready for
review (never a draft). CI 7/7 green on the first push; `mergeStateStatus`
CLEAN. Only the copilot non-review so far. Not merged.

## Issue

https://github.com/brekkylab/backlot/issues/586
"slack: conversations.history checks a bad cursor before a bad oldest or latest, and oldest before latest, where real checks latest, then oldest, then the cursor"
Labels: `good first issue`, `help wanted`, `fidelity`, `hacktoberfest`

Filed by maintainer `nuriyoo` on 2026-10-10T06:45:56Z, explicitly "Found while
reviewing an open pull request that answers a non-finite `oldest` or `latest`
with these errors" — that PR was ours (#577, merged 2026-10-10T13:59:45Z). So
this is a direct continuation of work already merged and reviewed on the same
handler.

At selection: unassigned, 0 comments, no competing PR. Re-verified open and
claim-clean immediately before the PR (Phase 13).

## Pull Request

[#620 — slack: conversations.history answers its errors in the order real reads them — latest, then oldest, then the cursor](https://github.com/brekkylab/backlot/pull/620)

- Base branch: `main` (the repo's only development branch)
- Opened: 2026-10-11T16:45:32Z, ready for review
- State: **open**, mergeable, CLEAN (all 7 checks green)
- Fork head: `ShahabAhmed01:contrib/issue-586-history-error-order`
- Closes: #586 (in the description, per policy item 5 — `Closes #N` in the body,
  no issue number in the title)

## Branch

`contrib/issue-586-history-error-order` (from `upstream/main` @ `0c879173b26637aeda4a668ca2af271815f52bb1`)

## Commits

- `b9af620c82acc1ecc260c3421635eb63dc26e785` — slack: conversations.history answers its errors in the order real reads them (fixes #586) (2 files, +41/−5)

## Problem

`conversations_history` in `backlot/routers/slack.py` checked the arguments in
the wrong order: the cursor first (`invalid_cursor`), then `oldest`
(`invalid_ts_oldest`), then `latest` (`invalid_ts_latest`). Real Slack reads
`latest`, then `oldest`, then the cursor, and answers in that order. So a
request carrying two or more unreadable arguments was named by whichever
Backlot happened to read first, not by the one real would name.

The issue measured a full table against slack.com/api on 2026-10-10 (user
token, one workspace, scopes `channels:history`, `channels:read`,
`search:read`, `users:read`, one request per row against a readable public
channel). Two divergence classes:

1. `oldest` and `latest` both unreadable: real names `latest`, Backlot named
   `oldest`.
2. An unreadable `oldest` or `latest` beside an undecodable cursor: real names
   the timestamp's error, Backlot named `invalid_cursor`.

## Root Cause

The three guards ran in the order Backlot happened to parse them in, not the
order real reads them. `offset = decode_cursor_or_none(...)` and its
`invalid_cursor` guard sat *before* the `lo`/`hi` `_slack_ts` checks, and
within those checks `lo is False` was tested before `hi is False`.

## Solution

A pure reorder of the three error guards in `backlot/routers/slack.py`
(`conversations_history`), so they run in real's reading order:

1. `hi is False` → `invalid_ts_latest` (latest read first)
2. `lo is False` → `invalid_ts_oldest` (oldest read second)
3. `offset is None` → `invalid_cursor` (cursor read last)

`lo` and `hi` are computed exactly as before (`_slack_ts` unchanged), and the
downstream time-window logic (`_in_window`, `ts_lo`/`ts_hi`, pagination) is
untouched — only the guard order changed. One comment cites the 2026-10-10
slack.com/api measurement.

## Files Changed

- `backlot/routers/slack.py` — reordered the three guards in `conversations_history` (+9/−5)
- `tests/test_slack.py` — new parametrised regression test `test_slack_history_names_the_first_error_real_would` (+32)

## Tests

`test_slack_history_names_the_first_error_real_would` encodes the issue's
measured table as 11 parametrised rows, asserting status 200 and the exact
`{"ok": false, "error": …}` body for each:

- 8 divergence rows: two unreadable timestamps, an unreadable timestamp beside
  an undecodable cursor (both ways), all three unreadable, the non-finite
  `inf` pairs, and `oldest=nan&cursor=zzz`.
- 3 single-argument control rows (`cursor=zzz`, `oldest=abc`, `latest=abc`)
  that pin the answers the reorder must not move.

**Regression proof (TDD):** with `backlot/routers/slack.py` stashed back to
unmodified `main`, **8 of 11 rows fail** (each divergence row answered
`invalid_cursor` or `invalid_ts_oldest` where real answers the other) and the
3 controls pass. With the fix restored, all 11 pass.

The non-finite rows (`oldest=nan&cursor=zzz`, the `inf` pairs) became
answerable at all only because the `isfinite` guard from merged #577 is on
`main` now — the issue noted those rows were left out of its `8a69e96` table
for that reason, and this branch completes them.

- **Focused:** `pytest tests/test_slack.py` — pass (207 tests in the file).
- **Full suite (2026-10-11):** `pytest` on a `.[dev,official-sdk,llamaindex]`
  install, Python 3.11 — **6346 passed, 10 skipped**, 0 failed. The 10 skips
  are the extras not installed here (`mcp`, `mirage`, `gdrive_fsspec`,
  `llama-index-readers-hubspot`).
- **Lint:** `ruff check . && ruff format --check .` — `All checks passed!`,
  `152 files already formatted`.
- **Prose check:** one pre-existing finding at `tests/test_google.py:6355`, a
  file this change does not touch. No new findings (the handler comment carries
  the measurement date; the test docstring points at the handler rather than
  re-dating it, per the "said once" rule).

## CI

- First push (2026-10-11T16:45:32Z): `gate`, `lint`, `scan`,
  `test (3.11)`–`test (3.14)` all passing — **7/7**, verified at 16:50Z.
  `mergeStateStatus` CLEAN, mergeable.
- No first-time-contributor `action_required` gate (previous merged PR #577
  lifted it; workflows ran on push without waiting).

## Review

- `copilot-pull-request-reviewer` left a non-review (COMMENTED).
- No human review yet. Awaiting `nuriyoo`/`khj809`.

## Merge

**Not merged.** GitHub confirms PR #620 is OPEN, MERGEABLE and CLEAN at head
`b9af620`, with no human review and no approval.

## Lessons Learned

- The best follow-up task is often filed by the maintainer *while reviewing
  your own merged PR* — it comes pre-scoped, pre-measured, and is a direct
  continuation of code you already understand. Watching the review thread for
  newly filed issues paid off here.
- The fix was a pure reorder — zero new logic — because the correct answers
  already existed; only the precedence was wrong. Small, provable, and easy to
  review.
- Encoding the issue's *entire* measured table (including the control rows that
  must not move) in one parametrised test makes the ordering claim self-evident
  and makes the regression replay a single stashed-file rerun.
- The non-finite rows were only testable because a *previous* merged PR (#577)
  had landed the `isfinite` guard first. Sequencing matters: this task was
  blocked-on-nothing only after #577 merged.
