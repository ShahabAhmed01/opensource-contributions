# Kludex/starlette — discussion #2738

## Status

**PR #3682 OPENED, 11/11 CHECK-RUNS GREEN** — opened 2026-10-19T13:17:51Z,
ready for review (not draft), base `main` @ `dc20b21` (verified current at
PR creation). On head `9fb4097` every check completed: `check`, `zizmor`
(x2), Python 3.11–3.15, `Run benchmarks` and the cubic AI reviewer all
success, `Docs preview (Cloudflare)` skipped (workflow shape);
`mergeable_state` `clean` as of 2026-10-19T13:44:48Z. Copilot was
quota-limited (posted no content), cubic left one P2 which was fixed in
`9fb4097` with a threaded reply; no human review yet. Not merged as of
2026-10-19T13:44:48Z.

## Issue

None — this contribution starts from a discussion, not an issue (the
repo's issue queue was deliberately not used; only six issues are open and
the maintainer's workflow routes bug reports through discussions first):

https://github.com/Kludex/starlette/discussions/2738
"Allow header returns the first route method it encounters"

Opened 2024-10-25T12:12:04Z by `ccrims0n` in category *Potential Issue*,
with the same repro this PR fixes: three `Route`s on `/user/{user_id}`
(GET, PUT, DELETE) answer `PATCH` with `Allow: GET` where
`Allow: GET, PUT, DELETE` is correct. `Kludex` replied **"Seems valid."**
two minutes later (2024-10-25T12:13:30Z). It stayed unfixed for two years,
with no PR ever referencing it (corpus grep for `2738`, `discussions/2738`,
`first route`, `GET, PUT, DELETE`: 0 hits among 3007 issues/PRs).

## Pull Request

[#3682 — Include all matching routes in the `Allow` header of `405`
responses](https://github.com/Kludex/starlette/pull/3682)

- Base branch: `main` @ `dc20b216f065af3a487722141da9a29dcac388d1`
  (verified current at PR creation)
- Opened: 2026-10-19T13:17:51Z · State: open, mergeable, `clean`, not
  draft
- Fork head: `ShahabAhmed01:fix/405-allow-multiple-routes` @
  `9fb409771097e7eed3fb1cebddad9694b34808b2` (2 commits, pushed and
  verified before the PR was opened and again after the review fix)
- No auto-close reference (there is no issue); the body links discussion
  #2738 as the prior discussion the PR template demands
- Size: 3 files, +93/−9

## Branch

`fix/405-allow-multiple-routes`, cut from `origin/main` @ `dc20b21` in
the isolated `~/opensource-work/starlette` clone. Pushed to the
`ShahabAhmed01/starlette` fork (created this session via
`POST /repos/Kludex/starlette/forks`) with a `GIT_ASKPASS` helper so the
token never entered argv or any output.

## Commits

- `f53602fbb848b57c8ccdb52173c04ac5841cb295` — Include all matching
  routes in the `Allow` header of `405` responses (3 files, +67/−8)
- `9fb409771097e7eed3fb1cebddad9694b34808b2` — Keep custom route 405
  handling when methods cannot be inferred (review fix)

## Problem

`Router(routes=[Route("/x", get, methods=["GET"]),
Route("/x", post, methods=["POST"])])` answers `PUT /x` with
`405 Allow: HEAD, GET` — `POST` missing. Reproduced on `main` @
`dc20b21` in three shapes (bare `Router`, `Starlette` app, two distinct
patterns `/items` + `/{name}` resolving to one path), all returning
`'HEAD, GET'`. [RFC 9110 §10.2.1](https://datatracker.ietf.org/doc/html/rfc9110#section-10.2.1)
requires the `Allow` header to list the methods supported by the target
resource (405 semantics: RFC 9110 §15.5.17).

## Root Cause

`Router.app` recorded only the first route returning `Match.PARTIAL`
(`elif match == Match.PARTIAL and partial is None`) and handed the request
to it alone, so `Route.handle` built `Allow` from that one route's
`self.methods`. Separately, that join was over a raw `set`, so the header
order varied between processes.

## Solution

- `Router.app` collects **every** partially matching route. When more than
  one route matches the path, it renders the `405` itself with the union of
  their methods, sorted (`Allow: GET, HEAD, POST`), via `HTTPException` when
  `"app" in scope` and `PlainTextResponse` otherwise (the pattern already
  used three times in the codebase).
- The union is only built when **every** partial match exposes a non-empty
  `methods` (true for all built-in route types). A custom `BaseRoute` that
  advertises its methods differently falls back to the previous behaviour —
  the first match dispatches through its own `handle()`. This guard is the
  fix for cubic's P2 review finding.
- The first partial match still provides `scope["route"]`; single-partial
  requests dispatch exactly as before.
- `Route.handle` now joins `sorted(self.methods)` for a deterministic
  header; `HTTPEndpoint` and `StaticFiles` already produced ordered output.

## Files Changed

- `starlette/routing.py` — partial-route collection, union `405` render
  with the inferability guard, `sorted()` in `Route.handle` (+29/−16 across
  both commits)
- `tests/test_routing.py` — two union tests (bare `Router` and `Starlette`
  app), one custom-route fallback test, tightened exact `Allow` assertion
  (+28/−1)
- `docs/routing.md` — paragraph documenting the multi-route `Allow`
  behaviour with an RFC 9110 link (+13/−0)

## Tests

- `test_router_405_allow_lists_all_matching_routes` — bare `Router`:
  `PUT /func` (the fixture already has GET and POST routes on `/func`) →
  405, `Allow: GET, HEAD, POST` through the plain-ASGI response path.
- `test_router_405_allow_lists_all_matching_routes_within_application` —
  `Starlette` app with two different patterns on one path → 405,
  `Allow: GET, HEAD, POST` through the `HTTPException` path.
- `test_router_405_keeps_custom_route_handling` — a custom `BaseRoute`
  with no `methods` attribute partial-matches first; the router must not
  take over: its own `handle()` still answers `Allow: PATCH` (and a
  non-matching path still 404s, covering `Match.NONE`).
- Existing `test_router` assertion tightened from `set(...)` to the exact
  `GET, HEAD`.
- **Full suite:** `uv run coverage run -m pytest -q` → **1400 passed,
  2 skipped, 2 xfailed** (baseline 1394 passed / 2 skipped / 2 xfailed).
- **Coverage:** `scripts/coverage` → **100% branch**, 0 missed of 1362
  branches (`fail-under=100`).
- **Static checks:** `scripts/check` clean (ruff format, mypy strict,
  ruff check over `starlette tests benchmarks`).

## Documentation

`docs/routing.md` "Handling HTTP methods" now states that a method no
matching route handles returns 405 whose `Allow` lists the methods of
every route matching the path, with a worked example and the RFC 9110
link. `docs/release-notes.md` was left alone on purpose: its "Releasing"
section in `docs/contributing.md` is maintainer-owned, and merged
precedents #3585/#3640 did not edit it either. `uv run zensical build
--clean` → "No issues found" (the docs CI command).

## CI (live at 2026-10-19T13:44:48Z)

- check: success · zizmor: success (x2) · Run benchmarks: success ·
  cubic · AI code reviewer: success
- Python 3.11 / 3.12 / 3.13 / 3.14 / 3.15: all success
- Docs preview (Cloudflare): skipped (workflow shape)
- 11/11 check-runs completed, none failing; `mergeable_state: clean`.
- codspeed bot comment: "Merging this PR will **not alter performance**".

## Review

No human review yet. `copilot-pull-request-reviewer[bot]` was
quota-limited and posted no content; `cubic-dev-ai[bot]` left one P2
(custom `BaseRoute` partials without `methods` would be bypassed) — valid,
reproduced in the test suite, fixed in `9fb4097`, answered in-thread
(comment `4314473754`). My own threaded reply is recorded by the API as a
`COMMENTED` review by `ShahabAhmed01`; it is a reply, not a review.
`Kludex` is the historical reviewer/merger of this repo's external PRs
(#3542, #3585, #3622, #3631, #3654). Per policy, no pings; the PR is the
reply.

## Merge

Not merged. Open, mergeable, `mergeable_state: clean` as of
2026-10-19T13:44:48Z, awaiting the first human review.

## Lessons Learned

- The AI policy's "search discussions too" rule paid for itself twice:
  it surfaced discussion #2738 — a maintainer-acknowledged ("Seems valid.")
  two-year-old report of exactly this bug — turning the PR-template
  checkbox from a risk into evidence, and it kept the PR from being
  opened blind.
- Automate the duplicate hunt against the *whole* corpus (titles **and**
  bodies, closed PRs included) before writing code: five previously
  attractive bugs (#3604 byte ranges, #3495 Accept-Encoding, #3638 IPv6,
  the query-param and authority swarms) turned out to be closed-unmerged
  duplicates, which on this repo means a likely ban rather than a review.
- The first green run is not the last word: the automated reviewer's
  custom-route finding was real (bypassing `handle()` for classes that
  advertise methods differently), and the guard plus its regression test
  made the change strictly safer than the fallback it preserved.
