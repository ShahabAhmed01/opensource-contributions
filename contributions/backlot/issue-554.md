# brekkylab/backlot — #554

## Status

Changes requested by the maintainer and addressed — PR open, all checks
passing on the response commit (`ab32213`), awaiting re-review. Not merged.

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
`main` has since moved (+10); GitHub still reports the PR MERGEABLE and
the maintainer tested this branch merged with today's `main` themselves,
so no branch update was requested.

## Commits

- `2013db90851350c2dcc41ad770a56cab92908edd` — slack: an oldest or latest
  with no finite value is the named invalid_ts error, as real answers it
  (2 files, +26/−2)
- `ab32213` — Address review: one parametrised test, 1e999 dropped,
  docstring states the measurement (2 files, +12/−26)

## Problem

`conversations.history` answers `500 Internal Server Error` for
`oldest=inf`, `oldest=nan`, `latest=inf` and `latest=nan`, where the real
Slack Web API answers `200 {"ok":false,"error":"invalid_ts_oldest"}` (or
`invalid_ts_latest`). A 5xx is what a client that retries one will retry,
so a request that can never succeed burns the whole retry budget.

## Root Cause

`_slack_ts` in `backlot/routers/slack.py` accepts anything `float()`
accepts. `float("inf")` and `float("nan")` parse, so the `False`
unparseable marker never fires, and the window computation
`ts_lo = int(lo) - 1` then raises `OverflowError` on infinity and
`ValueError` on NaN — neither caught anywhere. The issue measured the
real API's answers on 2026-10-09 (user token, scopes `channels:history`,
`channels:read`, `search:read`, `users:read`, one request per row with a
cache-buster) and located the crashing path precisely; the maintainer's
review measurement on 2026-10-10 extended the spelling set (see Review).

## Solution

One guard in `_slack_ts`: a reading that is not finite is marked `False`,
exactly like a string that does not parse, so the call site's existing
`is False` checks answer `invalid_ts_oldest`/`invalid_ts_latest`
unchanged. `import math` / `math.isfinite`, matching `byo.py` and
`protojson.py`. `int()` never sees a value it can raise on. The
spellings `float()` reads non-finite (`inf`, `-inf`, `nan`, `Infinity`,
`-Infinity`, `NaN`) take the same branch; each was a 500 before, and no
window can be built from any of them.

Deliberately out of scope, stated in the PR: a finite ts beyond SQLite's
64-bit bind range (`oldest=1e19` and up) still 500s at the binding; the
real API's lenient parse of such strings is the separate change the
issue names (`abc123` as 123, `1e9` as 19). The review added
`1e999` to this list: real reads it as 1999 and answers a window
(`"oldest": "0000001999.000000"`, measured 2026-10-10), this branch
answers `invalid_ts_*` (it was a 500), and matching the lenient parse
belongs with the `1e19` case.

## Files Changed

- `backlot/routers/slack.py` — `math.isfinite` guard in `_slack_ts`;
  docstring states the 2026-10-10 measurement of which spellings real
  refuses and that `1e999` is not one of them (no issue number and no
  repeated date, per `scripts/prose_check.py`'s two rules)
- `tests/test_slack.py` — `test_slack_history_rejects_a_malformed_timestamp`
  parametrised over both params × seven spellings (`not-a-ts` plus the
  six non-finite), asserting status 200 and the exact error body; the
  separate non-finite test from the first commit was folded in at review

## Tests

- **Regression proof:** with the guard reverted to `return ts`, the
  merged test's 12 non-finite rows FAIL (each a 500) and the 2
  `not-a-ts` rows pass either way; restored, all 14 pass. Replayed at
  `ab32213` after the review response.
- **Focused:** `pytest tests/test_slack.py` — 158 passed.
- **Full suite:** first run on a `.[dev,official-sdk,llamaindex]` install
  (uv venv, Python 3.14) — 6088 passed, 10 skipped; after the review
  response (two test rows fewer from the merge) in this workspace's venv
  (Python 3.11) — 6086 passed, 10 skipped. Skips are the extras not
  installed: `mcp` 1, `mirage` 1, `gdrive-fsspec` 7,
  `llama_index.readers.hubspot` 1 — none touches the Slack surface.
- **Touched-surface extras:** `.[official-sdk]` — `tests/test_sdk.py` +
  `tests/test_s3.py` 1371 passed, 0 skipped (Slack SDK
  `conversations.history` included); `.[llamaindex]` —
  `tests/test_llamaindex.py` + `tests/test_integrations.py` 26 passed,
  9 skipped (the Slack reader construction test ran).
- **Lint:** `ruff check . && ruff format --check .` — clean (152 files);
  `python scripts/prose_check.py` — clean.

## Runtime Validation

Bundled corpus (`backlot import backlot/data/hello.jsonl`) over
`backlot.serve()`, replaying the issue's rows: `oldest=inf`,
`oldest=nan`, `oldest=-inf`, `oldest=Infinity`, `oldest=NaN` →
200 `invalid_ts_oldest`; `latest=inf`, `latest=nan` →
200 `invalid_ts_latest`; control `oldest=1` → 200 `ok:true` with
messages; `oldest=abc` unchanged. `oldest=1e999` also answers
`invalid_ts_oldest` on this branch (a 500 before) — the real API answers
a window for it, which is the documented out-of-scope divergence.

## CI

- First push (2026-10-09T18:5xZ): `gate`, `lint`, `scan`,
  `test (3.11)`–`test (3.14)` all passing; PR MERGEABLE.
- Review-response commit `ab32213` (2026-10-10): same 7 checks all
  passing; PR MERGEABLE.

## Review

- `copilot-pull-request-reviewer` left a generic bot summary (no inline
  findings) on the first commit.
- **`nuriyoo` (maintainer) requested changes at 2026-10-10T06:49:20Z** —
  the first human review. Required: (1) drop `1e999` from the
  parametrize and the docstring's list — their slack.com/api
  measurement of 2026-10-10 shows real reads it as 1999 and answers a
  window, so the PR must not pin an answer real does not give; it
  belongs beside `1e19` in "Not in this PR", and the body sentence that
  reasoned from `float()` should cite the measurement instead;
  (2) one test, not two — fold the spellings into
  `test_slack_history_rejects_a_malformed_timestamp` as parametrize rows
  (exact code supplied); (3) the docstrings must not narrate the 500
  they fix (exact replacement docstring supplied). Optional: (4) use
  `import math` / `math.isfinite` like the two other modules; (5) PR
  body "a 500 is what an SDK retries" → "a client that retries a 5xx".
  They also verified the fix themselves (14 cases fail with the guard
  reverted; full suite on this branch merged with today's main: 6196
  passed, 1 skipped) and filed a separate issue on
  `invalid_cursor`/`invalid_ts` precedence, explicitly not for this PR.
- **Addressed at `ab32213`**, all five items, with the regression replay
  and full-suite rerun above; PR body corrected (test description,
  "Not in this PR" with the measurement, retry sentence, commit pin).
  Reply comment:
  https://github.com/brekkylab/backlot/pull/577#issuecomment-6097848273
- A formal review re-request is not possible for a PR author
  (`RequestReviewsByLogin` permission denied by the API); the reply's
  @mention is the notification. Awaiting re-review.

## Merge

_Not merged._

## Lessons Learned

- This repo mints pre-measured fidelity issues: the live-API
  measurement lives in the issue, so a first PR needs no vendor token —
  cite the issue's measurement and replay only the Backlot side.
- A maintainer's on-the-wire measurement outranks reasoning from a
  parser's source: `float("1e999")` is `inf`, but real Slack reads the
  string as 1999 and answers a window. When the reviewer supplies exact
  replacement text (docstring, test shape), adopt it verbatim — it is
  the acceptance criteria.
- Review response shape that worked here: one commit, every required
  and optional item applied, local replay of the reviewer's own
  verification, a single itemized reply, and the PR body corrected in
  the same pass (the body carries claims too).
- `scripts/prose_check.py` has two rules beyond ruff: no `#NNN` issue
  numbers in comments/docstrings (the number goes in the PR
  description), and a date must not appear both in a code comment and a
  test comment. Write the comment for the measured fact, not the fix
  history.
- One open PR at a time until the first merge; drafts are not reviewed
  and are closed after seven days.
