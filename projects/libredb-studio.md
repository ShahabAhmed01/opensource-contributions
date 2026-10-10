# Project notes — libredb/libredb-studio

Last verified: 2026-10-09

## Facts

- Web-based SQL IDE over twenty-seven external engines (plus the embedded
  LibreDB store), running two ways: a standalone Next.js app and the
  published npm package `@libredb/studio` (`npx @libredb/studio`).
  MIT license. ~1178 stars. Very active: 447 merged PRs in the prior 30
  days at selection, nearly all from external authors.
- TypeScript, Bun (`packageManager: bun@1.4.2`, Node >= 24). Two provider
  families: `src/lib/db/providers/sql/**` and `.../document/**`, each a
  four-file seam (index + transport + query dialects + introspect) with
  `fetch` confined to `*-transport.ts` (seam-guard tests enforce it).
- Default and only development branch: `main`, protected; trunk-based
  (feature branch → `main` → tag). Required checks: "Lint, Typecheck and
  Build", "Unit & Integration Tests", "Secret Scan". SonarCloud not
  required for forks.
- Maintainers `kaya-abdullah` and `cevheri` answer claims within
  minutes–hours and run real review cycles.
- `CLAUDE.md` carries agent rules: TDD (failing test before fix), the
  provider **triad rule** (code ↔ `docs/providers/<type-id>.md` ↔ tests
  move together per type-id), and the full pre-commit gate list.
- `docs/providers/*.md` cite code by NAME, never by line; the enforced
  list is `tests/unit/provider-docs-monitoring-citations.test.ts`
  (cited members must appear in declaration order). Separately,
  `src/lib/api/object-route.ts` does pin trino line anchors and a test
  re-measures them — re-run it after inserting lines.

## Development / validation commands

```bash
bun install --frozen-lockfile
bun run format            # biome, check-only
bun run lint              # oxlint && eslint && only-check
bun run typecheck         # tsc --noEmit
bun run test              # full suite; NEVER bare `bun test`
bun tests/run-tests.ts tests/unit/x.test.ts   # one file
bun run test:coverage && bun run coverage:check  # 100% line gate
bun run knip && bun run chart:check && bun run channels:showcase:check
bun run readme:check && bun run security:check
bun run build             # next build (+ copy-monaco)
```

- The runner spawns one bun process per file with coverage and merges
  lcov only on a fully green run — a red run leaves `coverage/lcov.info`
  absent by design (a stale report must not pass the gate).
- The full suite is large (~400 files) and fast (~2 min, 32 jobs). Known
  environment-dependent failures on this machine: `tests/unit/
  test-runner-cli.test.ts` (2 SIGINT/signal-delivery tests fail
  identically on unmodified base — pipe-signal timing under CachyOS);
  helm-chart tests need helm; `zip`-dependent build tests skip when the
  binary is absent.

## Contribution policy (CONTRIBUTING.md / CLAUDE.md / PR template)

- Claim an issue by one comment describing a short plan, before writing
  code; one issue at a time; re-verify the issue is unclaimed and has no
  competing PR immediately before opening the PR.
- Fork + branch from `main`; `Closes #N` in the PR body; start from
  `.github/PULL_REQUEST_TEMPLATE.md` (all caps; `gh pr create --body`
  does not load it).
- TDD: the failing test lands before the fix. Provider changes follow
  the triad rule. Local gate list above must pass before the PR;
  anything that cannot run goes in the PR's Testing section with the
  reason.
- PR titles use conventional style: `fix(scope): sentence` /
  `feat(scope): ...`; recent merged titles confirm the shape.
- CI is the merge gate; never bypass assignment/review/CI gates. First
  PRs from new accounts are not held behind an `action_required` gate
  here (observed on #1628: third-party scanners ran immediately).

## Why this project was selected (2026-10-09 research)

- Screened from ~26 discovered / ~10 deep-screened repos; highest score
  of the batch. 447 merged PRs/30d nearly all external; maintainers
  respond within minutes–hours; claim-by-comment policy rewards a good
  plan; 100% line-coverage gate means the quality bar is stated, not
  guessed.
- Issue #1411 chosen over alternatives: unassigned with 0 comments, no
  competing PRs, a maintainer-authored E2E measurement and a prescribed
  fix plan (lower ambiguity than #1412's two alternative approaches);
  #1540 was already assigned to another contributor.
- Rejected comparables: OpsiMate (~88; issues consumed same day),
  hivecommons/hive and crazy-goat/tyci-agent (bot-driven PR flow);
  backlot #577 already open (its one-open-PR rule) and the odysseus
  fleet at 7 unreviewed PRs (capacity risk).

## Pitfalls learned

- The provider docs are a minefield of cross-checks: doc-cited member
  names are pinned in a test in declaration order; `object-route.ts`
  pins trino line anchors in another test. Any insertion into a provider
  file requires re-measuring both.
- `connectWarnings()` only reports what the *provider* produces at
  connect time; the route and dialog plumbing already existed since
  #1401, so "carry it to the dialog" needed zero client changes — check
  for an existing seam before building a new one.
- Trino identifier comparisons must be case-insensitive (the
  coordinator folds the catalog header); Couchbase RBAC roles may read
  the cluster but not bucket settings, so only a 404 may refuse.
- The issue text said SHOW CATALOGS, but the codebase deliberately reads
  `system.metadata.catalogs` (same catalog set, plus connector names);
  reuse the codebase seam and state the deviation in the PR.

## Contribution history

### #1411 — Test Connection names a missing bucket/catalog (PR #1628 open, 2026-10-09)

- Branch: `fix/test-connection-bucket-catalog-1411`; PR:
  https://github.com/libredb/libredb-studio/pull/1628 (base `main`),
  closes https://github.com/libredb/libredb-studio/issues/1411.
- Fix: Couchbase `connect()` refuses a 404 on
  `/pools/default/buckets/<bucket>` with a `DatabaseConfigError` naming
  the bucket (only 404 refuses; RBAC/other failures keep the connect);
  Trino `connect()` checks the pinned catalog against
  `system.metadata.catalogs` after the probe and, when absent, carries a
  warning naming it via `connectWarnings()` — the channel the
  test-connection route and dialog already deliver.
- Validation: TDD (all new tests failing on unmodified main first);
  552/552 across the five affected files; full suite green except the
  pre-existing `test-runner-cli` SIGINT pair (proven identical on base
  by stash/re-run); all local gates pass; coverage gate runs in CI.
  Independent read-only review approved with two prose fixes applied
  before commit.
- Rebase (2026-10-10): `main` moved +13 commits (`4ebc787` → `aad0c73`)
  and the PR went CONFLICTING; single conflict in `object-route.ts`'s
  pinned-citation docblock resolved by file ownership (upstream's
  postgres pins `4046`/`4203` kept alongside this branch's trino pins
  `1340`/`1534`) and verified by that docblock's enforcing test. All
  gates re-run green including the new `distribution:check`; focused set
  741/741 across six files; full suite green except the known pair;
  force-pushed `6005817`; GitHub reports MERGEABLE; the four scanners
  re-ran green, own workflows remain at the approval gate.
