# Kludex/uvicorn — discussion #3108

## Status

**PR #3215 OPENED, 26/27 CHECK-RUNS GREEN (1 SKIPPED), ONE BOT APPROVAL** —
opened 2026-10-19T17:24:52Z, ready for review (not draft), base `main` @
`cc6fea5` (verified current at publication). On head `c8eb28c` every check
completed: `check`, `zizmor` (x2), `Run benchmarks`, `CodSpeed Performance
Analysis`, `cubic · AI code reviewer` and Python 3.11–3.15 plus free-threaded
3.14t/3.15t across ubuntu/macos/windows all success (26 runs), `docs-preview`
skipped (workflow only builds docs for same-repo branches); commit status
`CodeRabbit` success at 17:51:48Z; `mergeable_state` `clean` as of
2026-10-19T20:38:44Z. `coderabbitai[bot]` left the only `APPROVED` review
(17:51:44Z) — that is a **bot** approval, not a maintainer's: no human has
reviewed yet, and the PR is **open, not merged**, as of 2026-10-19T20:38:44Z.

## Issue

None — this contribution starts from a discussion, not an issue (uvicorn's
`docs/contributing.md` requires contributions to begin with a discussion; bug
reports go up as *Potential Issue* discussions):

https://github.com/Kludex/uvicorn/discussions/3108
"Graceful shutdown aborts when one connection is left in h11 ERROR state"

Opened 2026-08-29T13:25:39Z by `kazuki-ma` (author association
*CONTRIBUTOR*) in category *Potential Issue*, with a full working repro: a
server whose app declares `content-length: 10` and then sends a shorter body
gets `our_state = ERROR` while still registered in
`server_state.connections` and with its transport open; calling
`connection.shutdown()` then raises
`h11._util.LocalProtocolError: Can't send data when our state is ERROR`.
The reporter traces the blast radius to `Server.shutdown()`'s bare
`for connection in list(self.server_state.connections): connection.shutdown()`
loop, so one broken connection means every connection after it is never asked
to shut down. `amasen02` confirmed the diagnosis on 2026-09-05T00:31:11Z and
proposed the fix (mirror `connection_lost()`'s guard, optionally plus a
`try/except` around the loop). No PR ever referenced the discussion: the
corpus sweep before implementation found zero open or closed PRs touching
`H11Protocol.shutdown()`'s `ConnectionClosed` path.

## Pull Request

[#3215 — Don't raise on shutdown when a connection is in h11 ERROR
state](https://github.com/Kludex/uvicorn/pull/3215)

- Base branch: `main` @ `cc6fea5b40ad559f7ca358a24b1a521451232281`
  (verified current at PR creation)
- Opened: 2026-10-19T17:24:52Z · State: open, mergeable, `clean`, not draft
- Fork head: `ShahabAhmed01:fix/shutdown-h11-error-state` @
  `c8eb28cdaaf78c74cdf987736bbdb262aa4aa4d2` (3 commits, pushed and
  verified before the PR was opened and again after the docs review fix)
- No auto-close reference (there is no issue); the body links discussion
  #3108 as the prior discussion the PR template demands, records the
  duplicate search required by `AI_POLICY.md`, and discloses AI assistance
- Size: 3 files, +94/−2

## Branch

`fix/shutdown-h11-error-state`, cut from `origin/main` @ `cc6fea5` in the
isolated `~/opensource-work/uvicorn` clone. Pushed to the
`ShahabAhmed01/uvicorn` fork (created this session via
`POST /repos/Kludex/uvicorn/forks`) with a `GIT_ASKPASS` helper so the token
never entered argv or any output.

## Commits

- `c78d1c3066e4bc6d052d7738d0cd472c46976c17` — Don't raise on shutdown when
  a connection is in h11 ERROR state (2 files, +92/−2)
- `1a0a5637ac77bd4e8761735a18e8115566eec518` — Document shutdown of
  connections whose HTTP state already failed (docs, +2/−0)
- `c8eb28cdaaf78c74cdf987736bbdb262aa4aa4d2` — Qualify the shutdown docs for
  in-progress responses (docs, +1/−1; the two `cubic` P3 findings)

## Problem

Reproduced on `main` @ `cc6fea5` before any code was written: a real-socket
server whose app sends a short body under a larger `content-length` leaves
the connection registered with `our_state = ERROR` and `transport.is_closing()
False`, and `Server.shutdown()` then dies with
`LocalProtocolError: Can't send data when our state is ERROR` out of its
connection loop. Connections further down the list are never told to stop,
`cycle.keep_alive` is not cleared, and the process falls back to waiting out
`timeout_graceful_shutdown`.

## Root Cause

`H11Protocol.connection_lost()` guards the identical call twice —
`if self.conn.our_state != h11.ERROR:` plus `try/except
h11.LocalProtocolError` — while `H11Protocol.shutdown()` sent
`h11.ConnectionClosed()` unguarded. h11 raises only when `our_state is ERROR`,
so the guard is what distinguishes the two paths, and the asymmetry in
`shutdown()` is the bug the discussion reports.

## Solution

- `H11Protocol.shutdown()` skips the `h11.ConnectionClosed()` handshake when
  `self.conn.our_state == h11.ERROR` and still calls `self.transport.close()`,
  so the broken connection is closed **and** `Server.shutdown()`'s loop
  reaches every remaining connection.
- Deliberately **no** `try/except` (the form `amasen02` proposed): after the
  guard, h11 cannot raise from that `send`, so an `except` branch would be
  unreachable — and uvicorn measures **line** coverage over `uvicorn` *and*
  `tests` with `fail_under = 100`, so dead lines fail the gate. The guard is
  the coverage-safe expression of the same intent, and it mirrors
  `connection_lost()` exactly.
- The second half of the commenter's proposal (a `try/except` around
  `Server.shutdown()`'s loop) was **not** taken: it would swallow genuinely
  unexpected exceptions server-side, changing shutdown semantics for every
  protocol, and is not needed once the h11 state is checked.

## Files Changed

- `uvicorn/protocols/http/h11_impl.py` — `our_state` guard plus a three-line
  comment explaining why raising there would abort the server's shutdown loop
  (+6/−2)
- `tests/protocols/test_http.py` — two regression tests (+86/−0)
- `docs/server-behavior.md` — one sentence in "Graceful Process Shutdown"
  (+2/−0, then +1/−1 for the review wording fix)

## Tests

- `test_shutdown_after_h11_enters_error_state` — drives one connection into
  `h11.ERROR` (declare `content-length: 10`, send a shorter body, swallow the
  app-side `LocalProtocolError`), then asserts `shutdown()` closes the
  transport instead of raising.
- `test_server_shutdown_closes_every_connection_left_in_h11_error_state` —
  real-socket integration through `Server.shutdown()` with a broken connection
  **before** healthy ones in `server_state.connections`, asserting every
  connection is closed.
- Repro discipline: both tests fail on `main` (`2 failed, 6 passed` for the
  touched file) and pass with the fix (`8 passed`).
- **Full suite:** `./scripts/test` → **1378 passed, 13 skipped** (the two new
  tests included; `filterwarnings = ["error"]`, so writers are closed with
  `await writer.wait_closed()`).
- **Coverage:** `./scripts/coverage` → **100.00%**, 0 missed of 8774
  statements (`fail_under = 100`, test files count as source).
- **Static checks:** `./scripts/check` clean (ruff format, mypy over 84
  files, ruff check).

## Documentation

`docs/server-behavior.md`'s "Graceful Process Shutdown" section now states
that a connection whose local HTTP state machine already failed is closed
directly instead of raising, that a connection still sending a response is
allowed to finish first, and that one broken connection cannot interrupt the
shutdown of the others. That is what lets the PR template's "documentation
updated" box be ticked truthfully. `CHANGELOG.md` / `docs/release-notes.md`
were left alone on purpose: uvicorn's release notes are written by the
maintainer at release time (`docs/contributing.md`, "Releasing").
`uv run zensical build --clean` → "No issues found" (the docs CI command —
the `docs-preview` job never runs for fork PRs).

## CI (live at 2026-10-19T20:38:44Z)

- check: success · zizmor: success (x2) · Run benchmarks: success · CodSpeed
  Performance Analysis: success · cubic · AI code reviewer: success
- Python 3.11 / 3.12 / 3.13 / 3.14 / 3.15 and free-threaded 3.14t / 3.15t
  on ubuntu-latest, macos-latest and windows-latest: all success
- docs-preview: skipped (workflow only builds docs when the head branch lives
  in the same repository)
- 27 check-runs completed, 26 success + 1 skipped, none failing; commit
  status `CodeRabbit` success (17:51:48Z); `mergeable_state: clean`.
- codspeed bot comment: "Merging this PR will **not alter performance**".

## Review

No human review yet. `copilot-pull-request-reviewer[bot]` was quota-limited
and posted no content (17:25:02Z); `cubic-dev-ai[bot]` found nothing in the
fix commit (17:27:11Z), then raised two P3s on the new docs sentence at
17:38:28Z — that the close was stated for in-flight responses too, and that
"closing handshake" implied a peer exchange `h11.ConnectionClosed()` never
performs. Both were valid, both fixed in `c8eb28c`, and both were answered
in-thread (replies `4316934181`, `4316934555`, 17:42Z), after which cubic
dropped the first finding from its summary. `coderabbitai[bot]` posted a
walk-through issue comment (17:45:57Z) and then `APPROVED` (17:51:44Z) —
the ledger's derived status "ready-to-merge" therefore means *automated
approval plus green CI*, **not** maintainer sign-off. `Kludex` is the
historical reviewer/merger of uvicorn's external PRs (#3184, #3195, #3092,
#3209). Per policy, no pings; the PR is the reply.

## Merge

Not merged. Open, mergeable, `mergeable_state: clean` as of
2026-10-19T20:38:44Z, awaiting the first human review.

## Lessons Learned

- uvicorn's `AI_POLICY.md` bans duplicate PRs outright, so the sweep has to
  include discussions, not just issues and PRs: discussion #3108 is the only
  place this bug was ever reported, and it is also the "prior discussion" the
  PR template demands — one artifact satisfies both the policy and the
  checklist.
- A proposed patch in a discussion comment is a starting point, not a spec.
  The commenter's `try/except` layer would have been unreachable code under
  `fail_under = 100` line coverage over test files; taking the guard alone
  kept the change minimal *and* verifiable. Say so explicitly in the PR body
  so the deviation reads as reasoning, not omission.
- Adding one honest docs sentence was what made the template's documentation
  checkbox tickable — and it was also where the automated reviewers had
  findings, so the docs commit got the same scrutiny as the code.
- Green CI plus a bot `APPROVED` is a state, not a milestone: record it as
  such, keep watching the PR, and never describe it as maintainer approval.
