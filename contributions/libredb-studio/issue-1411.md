# libredb/libredb-studio — #1411

## Status

In review — PR open, rebased onto current `main` (MERGEABLE again),
scanners green, repo CI at the first-time-contributor gate

## Issue

https://github.com/libredb/libredb-studio/issues/1411
"Test Connection: Couchbase reports success for a bucket that does not exist, and Trino for a missing catalog"

Unassigned, 0 competing PRs, only the maintainers' description at selection
time; the issue had been assigned once before (2026-10-04) and returned to
the pool. Claimed by comment (repo policy: comment before code, one issue
at a time), then re-verified unassigned / no other comment / no competing
PR immediately before opening the PR (2026-10-09T20:4xZ).

Claim comment:
https://github.com/libredb/libredb-studio/issues/1411#issuecomment-6087957686

## Pull Request

[#1628 — fix(test-connection): a missing Couchbase bucket refuses, a missing Trino catalog warns (#1411)](https://github.com/libredb/libredb-studio/pull/1628)

- Base branch: `main` (protected; required checks "Lint, Typecheck and
  Build", "Unit & Integration Tests", "Secret Scan")
- Opened: 2026-10-09T20:50:15Z
- State: open, not a draft
- Fork head: `ShahabAhmed01:fix/test-connection-bucket-catalog-1411`
- Closes: #1411 (`Closes #1411` in the body)
- Size: 8 files, +182/−10
- Mergeable: first CONFLICTING on 2026-10-10 when `main` moved +13
  commits; MERGEABLE again after the rebase below

## Branch

`fix/test-connection-bucket-catalog-1411`, rebased 2026-10-10 onto
`upstream/main` @ `aad0c73abad2c123d89189d839b614cdf9b00c7e` (original
base `4ebc78761380`). Force-pushed with lease (`53145e4` → `6005817`).

## Commits

- `600581711d04cda4b5a948cff174eec44ffd9436` — fix(db): refuse a missing
  Couchbase bucket and name a missing Trino catalog at Test Connection
  (#1411) (8 files, +182/−10; rebased, conflict resolution inside)
- superseded: `53145e4311324bff3cbda856c95b3b9895699c04` (same subject,
  pre-rebase)

## Problem

`POST /api/db/test-connection` answered a plain "Connected successfully"
for two configurations the server does not have. Couchbase `connect()`
proved only that the cluster answers `/pools/default`; a saved wrong
bucket name connected, showed the cluster's real buckets in the tree and
never said the configured one was wrong (measured E2E by the maintainer
in the issue on `couchbase/server:community` 8.0.2). Trino `connect()`
sent only `SELECT 1`, which needs no catalog by design, so a pinned
catalog the cluster lacks was accepted silently (measured on Trino 483).

## Root Cause

- Couchbase: `connect()` in `src/lib/db/providers/document/couchbase/
  index.ts` read only `POOLS_PATH`; the bucket — the scope of every
  monitoring read — was never asked about.
- Trino: `CONNECT_PROBE_SQL = "SELECT 1"` in
  `src/lib/db/providers/sql/trino/index.ts` is deliberately catalog-free;
  nothing checked the pinned catalog, and nothing produced a
  `connectWarnings()` entry for the test-connection channel.

## Solution

Exactly the issue's prescription, through seams the repo already had:

- Couchbase: `assertBucketExists()` runs after the pools read and asks
  the bucket's own path (existing `bucketPath()` helper). A 404 — the
  cluster itself saying the bucket is not there — becomes a
  `DatabaseConfigError` naming the bucket, passed through unchanged by
  `describeConnectFailure`. Only a 404 refuses: any other failure (403
  for a role that may not read bucket settings, a network fault) keeps
  the connect the pools read already proved, so no working connection
  regresses.
- Trino: after the probe succeeds, `probePinnedCatalog()` checks the
  pinned catalog (`config.database`) against the provider's existing
  catalog read `TRINO_CATALOG_LIST_SQL` (`system.metadata.catalogs` —
  the issue says SHOW CATALOGS; `introspect.ts` documents why the
  provider reads the same set through this statement). An absent catalog
  becomes one `QueryWarning` naming it, exposed by `connectWarnings()` —
  the exact channel `POST /api/db/test-connection` already carries to the
  connection dialog since #1401 (no route or client change was needed;
  the route's warning tests already cover the carry). Comparison is
  case-insensitive (the coordinator folds the catalog header identifier).
  No pinned catalog → no extra read; a refused listing → silent connect,
  because the probe already proved it.
- Docs `§2.4` of both provider guides rewritten in lockstep (triad rule);
  the citations test's pinned member lists gained `connectWarnings` and
  `assertBucketExists` in declaration order; the two trino line
  citations in `src/lib/api/object-route.ts` were re-measured after the
  insertions (a test enforces them).

## Files Changed

- `src/lib/db/providers/document/couchbase/index.ts` — `HTTP_NOT_FOUND`
  constant, `assertBucketExists()` + docstring, called from `connect()`
- `src/lib/db/providers/sql/trino/index.ts` — `connectCaution` field,
  probe call in `connect()`, `connectWarnings()`, `probePinnedCatalog()`
- `docs/providers/couchbase.md`, `docs/providers/trino.md` — §2.4
  lifecycle paragraphs
- `tests/integration/db/couchbase-provider.test.ts` — 2 new tests
- `tests/integration/db/trino-provider.test.ts` — 6 new tests; 3
  existing statement-sequence tests adapted to the extra connect read
  (baseline capture, harness id shift, exact two-statement assertion)
- `tests/unit/provider-docs-monitoring-citations.test.ts` — pinned lists
- `src/lib/api/object-route.ts` — two re-measured trino citations (and,
  at rebase, upstream's postgres renumbering kept alongside them)

## Tests

- **Regression proof (TDD):** every new behaviour test was written first
  and shown failing on unmodified `main` (couchbase: the 404-refusal
  test; trino: all six — `connectWarnings` did not exist). The fix then
  turned them green.
- **Focused:** `bun tests/run-tests.ts` over the affected files —
  post-rebase (2026-10-10) 741/741 across six files: test-connection 23,
  couchbase-provider 151, trino-provider 219,
  provider-docs-monitoring-citations 140, object-route-edit 19,
  migration-generator 189 (the last two are what enforce the pinned
  citations; upstream's added tests explain the growth from the first
  run's 552).
- **Full suite with coverage:** every file passes except
  `tests/unit/test-runner-cli.test.ts` (2 SIGINT tests), which fails
  **identically on the unmodified base** (proven by stashing the whole
  diff and re-running: same 2 failures). It exercises the test runner's
  own signal handling and imports none of the touched code. Because the
  runner by design never merges lcov on a red run,
  `coverage:check` could not complete locally; the 100% gate runs in
  CI's "Unit & Integration Tests" job. Every new line is exercised by
  the new tests (both `assertBucketExists` branches; all four
  `probePinnedCatalog` outcomes). Re-run after the rebase: same result —
  green except the known pair.
- **Gates:** `bun run format`, `lint` (0 errors; 323 pre-existing
  warnings, none in changed lines), `typecheck`, `knip`, `chart:check`,
  `channels:showcase:check`, `readme:check`, `security:check`,
  `distribution:check` (gate added upstream during the rebase),
  `build` — all pass, re-run after the rebase.
- **Independent review:** a separate read-only review pass approved the
  diff with two prose fixes applied before commit (replaced an
  unmeasured "another bucket's data" claim with the issue's measured
  wording; reflowed the couchbase doc paragraph).

## Rebase (2026-10-10)

`main` advanced 13 commits (`4ebc787` → `aad0c73`) and GitHub reported
the PR CONFLICTING. One conflict, in `src/lib/api/object-route.ts`'s
docblock of `path:line` citations (both sides had renumbered): resolved
by keeping upstream's postgres pins (`4046`, `4203` — from #1626's
insertions; upstream never touched trino or redis) and this branch's
trino pins (`1340`, `1534` — upstream never touched trino). Verified by
the docblock's own enforcing test (`object-route-edit`, 19 pass) rather
than by eye. All gates, the focused set and the full suite re-run after
the rebase; force-pushed with lease; GitHub recomputed MERGEABLE.

## Runtime Validation

None — no live Couchbase or Trino engine in this environment. Both
providers' tests drive the repo's own fetch-harness transport doubles,
as the issue's Tests section prescribes; the 404 shape matches
ns_server's own behaviour (plain-text "Object Not Found" →
`httpError(404)`), verified by reading ns_server's route table.

## CI

- 2026-10-09T21:0xZ: third-party scanners ran on first push and all
  pass — Socket Security (Project Report, Pull Request Alerts),
  GitGuardian, semgrep. The repo's OWN workflows (CI, CodeQL Advanced,
  Security Scan, Platform Integration Check) triggered but completed as
  `action_required` — GitHub's first-time-contributor approval gate,
  exactly like the odysseus fleet; a maintainer must approve the run, and
  the gate must not be bypassed. So the required checks ("Lint, Typecheck
  and Build", "Unit & Integration Tests") have not executed yet and no
  green-CI claim is made.
- 2026-10-10T13:2xZ (after the rebase): all four scanners re-ran on
  `6005817` and pass; the own-workflows gate state is unchanged
  (maintainer-side, not bypassed).

## Review

None yet — no human review, only the Copilot quota-limit non-review.
Awaiting maintainer review; maintainers `kaya-abdullah` and `cevheri`
respond to claims within minutes–hours per the selection research.

## Merge

_Not merged._

## Lessons Learned

- `connectWarnings()` (added for Materialize #1401) is the house channel
  for "a connect that succeeded is not what was asked for"; a second
  engine needed only to produce a warning to inherit the whole
  route+dialog pipeline, zero client changes.
- Provider changes drag line-number citations: `object-route.ts` pins
  trino line anchors and a test enforces them; re-measure every cited
  file after inserting lines above the anchors.
- A rebase conflict in a pinned-citation docblock is resolved by
  file-ownership, not by picking a side: the two sides pinned DIFFERENT
  files (upstream moved postgres, this branch moved trino), so the merge
  keeps both sets, and the enforcing test — not the eye — checks the
  result.
- Docs cite code by NAME (`provider-docs-monitoring-citations.test.ts`):
  a new member cited in prose must be added to the test's pinned list in
  declaration order, same PR.
- `test-runner-cli.test.ts` SIGINT tests are environment-dependent on
  this machine (CachyOS); reproduce-on-base via stash is the clean way
  to prove a failure is not yours.
