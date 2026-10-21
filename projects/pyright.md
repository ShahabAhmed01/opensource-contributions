# Project notes — microsoft/pyright

Last verified: 2026-10-21

## Facts

- Static type checker for Python (and the `pyright` CLI / language server
  that VS Code's Pylance builds on). Developed by Microsoft; the repo is
  the OSS home of the engine behind Pylance. License: MIT for the code
  (repo `license` field reads `NOASSERTION` because of bundled typeshed
  and third-party notices).
- 15,692 stars / 1,836 forks (live 2026-10-21); `main` is the only branch
  PRs target; active pushes (last 2026-10-21T18:57:25Z).
- Monorepo under `packages/`: `pyright` (CLI bundle), `pyright-internal`
  (the engine + the entire test suite), `pyright-language-server`,
  `pyright-analysis`. Contributor work happens in `pyright-internal`.
- Test suite: jest, run from `packages/pyright-internal`
  (`pnpm exec jest`). The type-evaluator suites are split across
  `typeEvaluator1..8.test.ts`; each test registers a Python sample from
  `src/tests/samples/` and asserts an expected error count at marked
  positions. Rule: a sample's `# EXPECTED` comments must fail on the
  unmodified base and pass with the fix (TDD, replayed by stash/re-run).
- Build: `pnpm -C packages/pyright build` produces the CLI bundle at
  `packages/pyright/dist/pyright.js` (run it with `node`, NOT
  `pyright-internal.js`). In dev builds the typeshed fallback must be
  passed explicitly (`--typeshedpath packages/pyright-internal/typeshed-fallback`)
  or imports resolve to Unknown.
- `CONTRIBUTING.md`: standard Microsoft CLA applies; no AI-disclosure
  requirement and no AI-hostility policy in force (the repo ships
  `.github/copilot-instructions.md`, i.e. AI tooling is accepted).
  External contributors need a maintainer to approve workflows for the
  Azure pipeline checks (`mypy_primer`, `Type checker benchmark`) —
  `mypy_primer` diffs pyright against a corpus of real projects, so
  behavior changes get surfaced there.
- Acceptance record measured 2026-10-21: external PRs merge — #11894
  (external Azure pipeline migration, merged 2026-10-19), #11864 and
  #11616 (type-evaluation fixes, merged mid-October). No claim-comment
  protocol; issues are free to take; the issue queue carries `bug`
  labels with minimal chatter (most issues have 0 comments).
- Release cadence is fast (1.1.414 was current on 2026-10-21), so
  unmerged PRs periodically need rebase onto a moving `main`.

## Engine facts (for future tracks)

- The `functools.partial` handling lives in
  `packages/pyright-internal/src/analyzer/constructorTransform.ts`
  (`hasConstructorTransform` / `applyConstructorTransform` /
  `applyPartialTransform(ToFunction)`); typeshed's `partial.__new__`
  takes `*args: Any` (no ParamSpec), so creation-time diagnostics come
  only from this transform.
- `applySolvedTypeVars` unpacks solved TypeVarTuple parameters into
  individual synthesized positional parameters — the reason a fully
  bound variadic prints as `(str, int) -> int`.
- Solved constraint solutions are keyed by `nameWithScope`; a synthesized
  TypeVar needs a distinct name (e.g. `${name}2`) and
  `TypeVarType.createInstance` (instance form) + `cloneForUnpacked` +
  `cloneForScopeId` to behave at call time.
- `_pendingTypeVarTransformations` guards recursive replacement; the
  constructor transform runs exactly once per partial creation.
