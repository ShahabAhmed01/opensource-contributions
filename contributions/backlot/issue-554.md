# brekkylab/backlot — #554

## Status

In review — PR open, all checks passing

## Issue

https://github.com/brekkylab/backlot/issues/554
"slack: conversations.history with `oldest=inf` or `oldest=nan` is a 500, where real answers invalid_ts_oldest"
Labels: `bug`, `good first issue`, `help wanted`, `fidelity`, `hacktoberfest`

Unassigned, no competing PR, no claim comments at selection time or at PR
creation (verified before implementation, before commit, and again at
2026-10-09T18:41Z, immediately before the PR).

## Pull Request

[#577 — slack: an oldest or latest with no finite value is the named invalid_ts error, as real answers it](https://github.com/brekkylab/backlot/pull/577)

- Base branch: `main` (the repo's only development branch)
- Opened: 2026-10-09T18:42:00Z
- State: open, mergeable, not a draft
- Fork head: `ShahabAhmed01:contrib/issue-554-non-finite-ts`
- Closes: #554 (GitHub confirms the link)

## Branch

`contrib/issue-554-non-finite-ts` (from `upstream/main` @ `12ce3450e858`)
— rebased once before commit to absorb an unrelated hubspot merge (#538).

## Commits

- `2013db90851350c2dcc41ad770a56cab92908edd` — slack: an oldest or latest
  with no finite value is the named invalid_ts error, as real answers it
  (2 files, +26/−2)

## Problem

`conversations.history` answers `500 Internal Server Error` for
`oldest=inf`, `oldest=nan`, `latest=inf` and `latest=nan`, where the real
Slack Web API answers `200 {"ok":false,"error":"invalid_ts_oldest"}` (or
`invalid_ts_latest`). A 5xx is what an SDK retries, so a request that can
never succeed burns the whole retry budget.

## Root Cause

`_slack_ts` in `backlot/routers/slack.py` accepts anything `float()`
accepts. `float("inf")` and `float("nan")` parse, so the `False`
unparseable marker never fires, and the window computation
`ts_lo = int(lo) - 1` then raises `OverflowError` on infinity and
`ValueError` on NaN — neither caught anywhere. The issue measured the
real API's answers on 2026-10-09 (user token, scopes `channels:history`,
`channels:read`, `search:read`, `users:read`, one request per row with a
cache-buster) and located the crashing path precisely.

## Solution

One guard in `_slack_ts`: a reading that is not finite is marked `False`,
exactly like a string that does not parse, so the call site's existing
`is False` checks answer `invalid_ts_oldest`/`invalid_ts_latest`
unchanged. `from math import isfinite` added. `int()` never sees a value
it can raise on. The spellings `float()` reads non-finite (`Infinity`,
`-inf`, `NaN`, `1e999`) take the same branch; each was a 500 before, and
no window can be built from any of them.

Deliberately out of scope, stated in the PR: a finite ts beyond SQLite's
64-bit bind range (`oldest=1e19` and up) still 500s at the binding; the
real API's lenient parse of such strings is the separate change the
issue names (`abc123` as 123, `1e9` as 19), and the value that parse
yields is a window bound, so the case belongs with it.

## Files Changed

- `backlot/routers/slack.py` — `isfinite` guard in `_slack_ts`; docstring
  records the measurement (no issue number and no repeated date, per
  `scripts/prose_check.py`'s two rules)
- `tests/test_slack.py` — `test_slack_history_rejects_a_non_finite_timestamp`:
  both params × seven non-finite spellings, asserting status 200 and the
  exact error body

## Tests

- **Regression proof:** the 14 new cases were run against the pre-fix
  router (stash/reapply): 14 FAILED (each a 500); with the fix, 14 pass.
- **Focused:** `pytest tests/test_slack.py` — all pass.
- **Full suite:** `pytest` on a `.[dev,official-sdk,llamaindex]` install
  (uv venv, Python 3.14) — 6088 passed, 10 skipped (skips are the extras
  not installed: `mcp` 1, `mirage` 1, `gdrive-fsspec` 7,
  `llama_index.readers.hubspot` 1 — none touches the Slack surface).
- **Touched-surface extras:** `.[official-sdk]` — `tests/test_sdk.py` +
  `tests/test_s3.py` 1371 passed, 0 skipped (Slack SDK
  `conversations.history` included); `.[llamaindex]` —
  `tests/test_llamaindex.py` + `tests/test_integrations.py` 26 passed,
  9 skipped (the Slack reader construction test ran).
- **Lint:** `ruff check . && ruff format --check .` — clean;
  `python scripts/prose_check.py` — clean.

## Runtime Validation

Bundled corpus (`backlot import backlot/data/hello.jsonl`) over
`backlot.serve()`, replaying the issue's rows: `oldest=inf`,
`oldest=nan`, `oldest=-inf`, `oldest=Infinity`, `oldest=NaN`,
`oldest=1e999` → 200 `invalid_ts_oldest`; `latest=inf`, `latest=nan` →
200 `invalid_ts_latest`; control `oldest=1` → 200 `ok:true` with
messages; `oldest=abc` unchanged.

## CI

All checks passing on the PR at first look (2026-10-09T18:5xZ):
`gate`, `lint`, `scan`, `test (3.11)`, `test (3.12)`, `test (3.13)`,
`test (3.14)`. GitHub reported the PR MERGEABLE.

## Review

`copilot-pull-request-reviewer` left a generic bot summary (no inline
findings). No human review yet — awaiting maintainer review (the repo's
reviewers are `nuriyoo` and `khj809`, who turn comparable fidelity PRs
around in 1–2 days).

## Merge

_Not merged._

## Lessons Learned

- This repo mints pre-measured fidelity issues: the live-API
  measurement lives in the issue, so a first PR needs no vendor token —
  cite the issue's measurement and replay only the Backlot side.
- `scripts/prose_check.py` has two rules beyond ruff: no `#NNN` issue
  numbers in comments/docstrings (the number goes in the PR
  description), and a date must not appear both in a code comment and a
  test comment. Write the comment for the measured fact, not the fix
  history.
- One open PR at a time until the first merge; drafts are not reviewed
  and are closed after seven days.
