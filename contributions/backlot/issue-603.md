# brekkylab/backlot — #603

## Status

**PR #633 OPENED 2026-10-12T09:23:04Z** — ready for review (never draft).
**CI 7/7 green on the first push** (gate, lint, scan, test 3.11/3.12/3.13/3.14),
verified 2026-10-12T09:28:02Z. PR OPEN and MERGEABLE. Awaiting first human
review from `nuriyoo`/`khj809`. Not merged.

## Issue

https://github.com/brekkylab/backlot/issues/603
"slack: a `token` query parameter authenticates and a bearer header outranks a `token` form field, where real refuses the first and reads the form field first"
Labels: `bug`, `fidelity`

Unassigned, 0 comments, no cross-referenced PR at selection (2026-10-12T08:28Z
and again at the pre-creation gate 09:22Z). No claim comment needed — an open
PR is what marks an issue taken (maintainer's rule on #577).

## Pull Request

[#633 — slack: a token query parameter is refused as invalid_auth, and a token form field outranks the bearer header](https://github.com/brekkylab/backlot/pull/633)

- Base branch: `main` (the repo's only development branch)
- Opened: 2026-10-12T09:23:04Z
- State: **open**, MERGEABLE, 7/7 checks green (mergeStateStatus BEHIND —
  upstream main moved to `c641b07` after the rebase; no conflicts)
- Fork head: `ShahabAhmed01:contrib/issue-603-query-token-form-precedence`
- Closes: #603 (`Closes #603` on the body's first line; GitHub confirms the link)

## Branch

`contrib/issue-603-query-token-form-precedence` (from `upstream/main` @ `94e79a07bfe`)

## Commits

- `5aaea3b4ac98fd79e0a7f4ea8ea510e5da579fb0` — slack: a token in the query string is refused as invalid_auth, and the token form field is read ahead of the bearer header (fixes #603) (4 files, +164/−13)

## Problem

Two silent divergences in Slack auth, both measured in the issue against
slack.com/api on 2026-10-11 (user token of an app created 2026-09-17, scopes
`channels:history`, `channels:read`, `search:read`, `users:read`, one request
per row with a cache-busting parameter, every answer `200`):

1. A non-empty `token` query parameter authenticates (`ok:true`), where real
   answers `invalid_auth` on every row — over GET and POST and on four
   methods, with or without a bearer header or a form token beside it. Slack's
   changelog "No more tokens in querystrings for newly created apps"
   (docs.slack.dev, November 1, 2020) closed that channel for apps created
   after February 24, 2021, and Backlot is such an app.
2. A bearer header is read before a `token` form field, where real reads the
   form field first: `Bearer <bogus>` + `token=<valid>` answers `ok` as the
   form's caller on real but `invalid_auth` here; `Bearer <valid>` +
   `token=<bogus>` answers `invalid_auth` on real but `ok` here.

## Root Cause

`auth.slack_token` was `bearer or query or form` — the first non-empty of the
three, header first — so the query parameter was a live credential and the
form field ranked last. `_caller_or_error` had no refusal to check before
resolution, and `docs/auth.md` named the query parameter as an accepted place
for the token.

## Solution

- `auth.slack_token` (backlot/auth.py): reads the `token` form field ahead of
  the `Authorization: Bearer` header — real's order — and no longer reads the
  query parameter at all.
- New `auth.slack_query_token_refused`: a non-empty `token` query parameter is
  refused whatever else the request carries; an empty one beside a bearer
  header is refused too; an empty `token=` alone stays no credential
  (`not_authed`). Case stays exact (`?TOKEN=` is not a credential, as live).
- `_caller_or_error` (backlot/routers/slack.py): answers the refusal with
  `invalid_auth` **before** `auth.slack_token` is read, so the refused channel
  preempts even a valid credential elsewhere.
- The `_caller_or_error` docstring table and the Slack paragraph of
  `docs/auth.md` move with the rule.

Deliberately not pinned (real unmeasured): `token=` empty beside a form field
with no bearer header (this branch lets the form field authenticate), and a
request with multiple `token` parameters (first value read). Disclosed under
"Not in this PR." in the PR body.

## Files Changed

- `backlot/auth.py` — +30/−4 (`slack_token` reorder, new refusal helper)
- `backlot/routers/slack.py` — +15/−5 (refusal check + docstring table)
- `docs/auth.md` — +5/−2 (Slack paragraph)
- `tests/test_slack.py` — +114/−2 (two new tests, stale "three ways" comment fixed)

## Tests

- **Two new tests:** `test_slack_refuses_a_token_query_parameter` (13 refusal
  rows over auth.test GET+POST, conversations.list, users.list,
  search.messages) and `test_slack_reads_a_form_token_ahead_of_the_bearer_header`
  (8 precedence rows with the admin and person tokens in opposite places).
- **TDD proof:** both failed on unmodified main; pass with the fix.
  **Revert-proof on the final base `94e79a0`:** `backlot/auth.py` and
  `backlot/routers/slack.py` put back to `main`'s → `2 failed`, restored →
  clean tree, all pass.
- **Full suite (2026-10-12):** `pytest` on this venv's `.[dev,official-sdk,
  llamaindex]` install, Python 3.11.17 — **6877 passed, 10 skipped** (junit:
  6887 events, 0 failures, 0 errors). The 10 skips are import-gated, none on
  the Slack surface: `mcp` (1), `mirage` (2), `gdrive_fsspec` (6),
  `llama_index.readers.hubspot` (1). `tests/test_slack.py` ran whole (495, 0
  skipped); `tests/test_sdk.py` ran whole (5 — the official `slack_sdk`
  driving `backlot.serve()` over a live port included); `tests/test_s3.py`
  ran (boto3 1.43.106).
- **Lint:** `ruff check . && ruff format --check .` — `All checks passed!`,
  `152 files already formatted`.
- **Prose check:** `python scripts/prose_check.py --github HEAD^1` (CI's exact
  invocation) — no findings, exit 0. With the script's default base (the
  fork's `origin/main`, which is behind upstream) the change-range wrongly
  swallows upstream's commits and reports main's pre-existing
  `tests/test_google.py:6355` / `tests/test_s3.py:338` findings — verified
  pre-existing by running the checker on a clean `94e79a0` worktree; not
  caused by this change.

## Runtime Validation

The issue's 19 rows replayed over `backlot.serve()` with the bundled corpus
(first user token from `/_meta/users` as `<valid>`), main at `94e79a0` before
the change and this branch after:

```
request                                          real (2026-10-11)   main at 94e79a0   this branch
GET  auth.test?token=<valid>                     invalid_auth        ok                invalid_auth
POST auth.test?token=<valid>, no body            invalid_auth        ok                invalid_auth
POST auth.test?token=<valid>, form x=1           invalid_auth        ok                invalid_auth
GET  conversations.list?token=<valid>&limit=1    invalid_auth        ok                invalid_auth
GET  users.list?token=<valid>&limit=1            invalid_auth        ok                invalid_auth
GET  search.messages?token=<valid>&query=a       invalid_auth        ok                invalid_auth
GET  auth.test?token=<valid>, Bearer <valid>     invalid_auth        ok                invalid_auth
GET  auth.test?token=<bogus>, Bearer <valid>     invalid_auth        ok                invalid_auth
GET  auth.test?token=, Bearer <valid>            invalid_auth        ok                invalid_auth
POST auth.test, Bearer <bogus>, form token=<v>   ok                  invalid_auth      ok
POST auth.test, Bearer <valid>, form token=<b>   invalid_auth        ok                invalid_auth
```

The other eight rows matched on main and still do. Totals: **main 11 of 19
diverging, this branch 0 of 19.**

## CI

- First push (2026-10-12T09:23Z): **7/7 green** — `gate` (6s), `lint` (11s),
  `scan` (29s), `test (3.11)` (3m33s), `test (3.12)` (2m49s), `test (3.13)`
  (3m44s), `test (3.14)` (3m19s); verified 09:28:02Z. No
  first-time-contributor gate (PR #577 lifted it).

## Review

None yet. No reviews, no comments as of 2026-10-12T09:28Z. Awaiting first
human review; do not ping.

## Merge

**Not merged.** GitHub confirms PR #633 is OPEN and MERGEABLE with 7/7 checks
green and no review yet.

## Lessons Learned

- Re-verify the issue and the PR capacity **immediately before** creating the
  PR: upstream moved 11 commits mid-session (including our own #614 merging,
  which freed a slot) and the issue stayed claim-clean throughout.
- prose_check's default base is `origin/main`; when the fork's main trails
  upstream, run it as CI does (`--github HEAD^1`) or the change-range picks up
  other people's merged dates. A clean-worktree run of the checker on the
  base commit separates pre-existing findings from yours.
- pytest-xdist (`-n auto --dist loadfile` in addopts) makes `--collect-only`
  report one fewer item than a real run (6886 vs 6887); a `--junitxml` pass is
  the authoritative count to quote.
- Matching the maintainer's precision in prose pays: the refusal is two
  sentences (non-empty refused; empty refused only beside a bearer header)
  because "refused whatever its value" would have been false for `?token=`
  alone, which stays `not_authed`.
