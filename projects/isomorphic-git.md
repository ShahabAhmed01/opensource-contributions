# Project notes — isomorphic-git/isomorphic-git

Last verified: 2026-10-11

## Facts

- Pure-JavaScript implementation of git in the browser AND in Node
  (UMD/ESM/CJS builds, no native deps). MIT license. ~9.6k stars, ~8 years
  old, still actively merged: 10 substantive merges by outside
  contributors in the two weeks before selection (incl. the analogous
  `feat(log)` #2385), plus routine `fix:` merges to main.
- Plain JavaScript (no transpile as a rule of thumb), layered
  architecture: `src/api` (public, JSDoc-typed) → `src/commands` →
  models/managers/utils. JSDoc is the type source: `tsc` generates
  `index.d.ts` from it, so a new param must be documented in **both**
  `src/api/X.js` and `src/commands/X.js`.
- Default and only development branch: `main` (not protected in the
  GitHub sense; squash merges by the maintainer). No required-check gate
  on forks; CI is an informational matrix (`isomorphic-git-PR`).
- Releases are `semantic-release`-driven: the squash-merge title IS the
  release note, so PR titles must be `feat(scope): …` / `fix(scope): …`.
- Two bot layers on every PR: CodeRabbit (auto summary comment) and
  GitHub Copilot pull-request reviewer (COMMENTED reviews). Neither is a
  gate. Human review comes from maintainer `jcubic` (responsive,
  merges fast, welcoming tone) — first-timer PRs are merged on trust
  after CI, e.g. #2385 and #2449.
- Tests are jest with a custom `makeFixture` harness that fakes
  browser/Node filesystems (`@zenfs/core`). **Node 26 breaks the
  fixtures** (`@zenfs/core` throws in every test file, even untouched
  ones); use Node 22. Several suites need the local git-http-mock-server
  (:8888) and cors-proxy (:9999), started by `nps test.setup` /
  `start-git-mock-server` and stopped by `nps test.teardown`.

## Development / validation commands

```bash
npm install                        # needs Node 22.x
npx nps test.setup                 # start mock servers on :8888/:9999
node --experimental-vm-modules node_modules/jest/bin/jest.js __tests__/test-log.js
node --experimental-vm-modules node_modules/jest/bin/jest.js --ci   # full
npx eslint src __tests__
npx nps lint                       # lint + typecheck
npx rollup -c --no-treeshake && npx tsc -p declaration.tsconfig.json  # index.d.ts
```

- Known environmental flake (both with and without local patches):
  `clone › clone with noTags` in `test-clone.js` and
  `test-clone-in-submodule.js` intermittently exceeds its 30s timeout on
  this machine (27–28s pass, 30s fail). Pre-existing, not a gate.
- `nps test.teardown` (or killing the PIDs on :8888/:9999) when done —
  a leftover server pins the ports for the next run.

## Contribution policy (CONTRIBUTING.md)

- **No claim protocol.** No CLA, no assign-bot, no "comment before you
  code". Fork → branch from `main` → open a PR. The only hard gate is
  the maintainer's merge click; fork workflows sit at a first-time
  `action_required` approval until then (the `isomorphic-git-PR` check
  starts QUEUED and `mergeStateStatus` reads BLOCKED — normal).
- Feature checklist (CONTRIBUTING "New feature checklists"): add the
  param to `src/api/X.js` + `src/commands/X.js`; document it in the
  JSDoc of both; add a test in `__tests__/test-X.js`; first-time
  contributors run `npm run add-contributor` (auto-commits
  `.all-contributorsrc` + `README.md` — merged PRs #2449 and #2385 ship
  exactly these two files alongside the feature); squash-merge title
  `feat(X): …`.
- Appendix A asks for a test mirror in `__tests__/test-X-in-submodule.js`
  when the feature touches command plumbing — but that file is behind
  main and recent feature PRs (#2385 `includeChanges`, #2413) skipped
  it, so it is applied leniently. State the omission in the PR body and
  offer to add it.

## Why this project was selected (2026-10-11 research)

- Screened ~34 discovered repos (GitHub search, goodfirstissue.dev,
  awesome-for-beginners), deep-verified ~12 finalists by merged-PR
  sampling, responsiveness, backlog shape and policy. isomorphic-git
  scored highest: pure JS (user preference), zero-friction policy,
  fast external merges, an open unclaimed issue with a clear ask.
- Issue #2286 chosen over alternatives: OPEN, unassigned, 0 competing
  PRs (PR search + cross-reference timeline both empty), self-contained
  (one command file + API doc), and locally testable without network.
  Eliminated: eslint `accepted`-label bugs (assigned), icalendar /
  cve-bin-tool / fastify / less / scrapy issues (claimed with open PRs),
  express #7350 (hostile thread), refined-github #8711 (needs a real
  extension build to validate), mypy (policy discourages LLM PRs from
  new contributors), cli/cli (PR template demands a human decision; no
  `help wanted` on candidates).

## Pitfalls learned

- System Node 26 silently breaks the whole jest harness via
  `@zenfs/core` — a red suite on Node 26 means nothing about a patch.
  Keep the Node 22 toolchain pinned and re-run before concluding
  anything.
- `log` has seven commit-emission sites but only one `commits.push`;
  filtering belongs in that single choke point (`pushCommit`), never at
  individual sites, or merge/shallow/filepath paths leak.
- The `filepath` + `depth` path has a pre-existing off-by-one at the
  depth boundary (`endCommit` flush can return `depth+1`); do not claim
  "`depth` limits matching commits" holds for `filepath` mode, and do
  not fix it inside an unrelated feature PR.
- JSDoc style: the repo-wide convention is `@param {type} [args.name]`
  (420 uses) not `{type=} args.name` (1 use, the adjacent `filepath`
  line) — follow the majority even when copying a neighbor.
- The all-contributors commit looks like noise in `git log` but is a
  stated CONTRIBUTING requirement for first-timers and appears in merged
  PRs; keep it as its own commit on the branch.

## Contribution history

### #2286 — Support `--author` flag on `log` command (**PR #2456 OPEN**)

- Branch: `feat/log-author-filter`; PR:
  https://github.com/isomorphic-git/isomorphic-git/pull/2456 (base
  `main`), closes #2286. Opened 2026-10-11T18:58:36Z, 5 files
  +216/−9, MERGEABLE.
- Adds `author` (case-insensitive JS RegExp over the author's
  `Name <email>`), applied before `depth`, composing with `filepath`,
  author-only, invalid regex rejects. Full detail in
  `contributions/isomorphic-git/issue-2286.md`.
- See that file for the verification ledger (14/14 focused, full suite
  1433/2 with the documented pre-existing flake, eslint + tsc clean,
  independent review approve-with-nits with 7 items applied pre-commit).
