# isomorphic-git/isomorphic-git — #2286

## Status

**MERGED 2026-10-12T07:52:12Z** — `jcubic` merged #2456 directly (squash
commit `c5916f4ce474c4305ec51c3cd9237f04e1027cd9`, title `feat(log): add
author filter`) with no formal approval review. Opened 2026-10-11T18:58:36Z,
ready for review (never a draft). CodeRabbit commented and Copilot posted a
COMMENTED review; both were answered with evidence before the merge.

## Issue

https://github.com/isomorphic-git/isomorphic-git/issues/2286
"Support `--author` flag on `log` command"

Filed 2026-02-14, 4 comments. OPEN, unassigned, zero competing PRs at
selection (searched PRs for `2286`, "author flag", and the issue's
cross-reference timeline = 0); re-verified open / unassigned /
0 cross-references immediately before `gh pr create`. The reporter asks
for basic author filtering on `log` "since it aims to be fully compatible
with Git". No maintainer commitment exists — the PR is the proposal.

## Pull Request

[#2456 — feat(log): add author filter](https://github.com/isomorphic-git/isomorphic-git/pull/2456)

- Base branch: `main` (base commit `909b97b1617be7d5c1b550759a35f5a8068dc058`)
- Fork head: `ShahabAhmed01:feat/log-author-filter`
- Closes: #2286 (`Fixes #2286` in the body)
- Opened: 2026-10-11T18:58:36Z
- Size: 5 files, +216/−9
  (`src/commands/log.js`, `src/api/log.js`, `__tests__/test-log.js`,
  plus the CONTRIBUTING first-time step `.all-contributorsrc` + `README.md`)
- Mergeable: MERGEABLE on open

## Semantics

- `author` is a case-insensitive JavaScript regular expression, tested
  against the author's `` `Name <email>` `` string — the same string
  `git log --author` matches.
- Applied **before** `depth` is counted, so `{ author, depth: n }` returns
  the `n` newest *matching* commits (like `git log --author --max-count`).
- Combines with `filepath`: non-matching commits are skipped in the
  output, but history traversal (file tracking, depth accounting) is
  unchanged.
- Filters on the **author** only, not the committer (the issue thread
  conflates the two; a dedicated test pins this).
- An invalid regular expression rejects with a `SyntaxError`.
- One deliberate divergence from git, stated in the JSDoc and PR body:
  git's `--author` is case-sensitive and uses basic regular expressions;
  this uses a JS RegExp with the `i` flag (friendlier for a JS library).

## Implementation

- `src/commands/log.js`: `authorRegex` compiled once per call;
  `matchesAuthor` helper; all seven commit-emission sites already route
  through the single `pushCommit` point, so one guard covers every exit
  path (merge commits, shallow boundaries, `filepath`-mode flushes).
- `src/api/log.js`: documented `author` param, passed through.
- `__tests__/test-log.js`: four new tests — filter by name/email +
  case-insensitivity + regex metacharacters + no-match → `[]` + invalid
  regex rejects; `depth` counts matching commits; combines with
  `filepath`; author ≠ committer.

## Verification (Node 22.22.0 toolchain)

System Node 26 breaks the repo's `@zenfs/core` fixtures (all test files,
including untouched ones), so a downloaded Node 22.22.0 was used.

- `jest __tests__/test-log.js` — 14/14 pass
- TDD regression proof: stashing `src/` makes the new tests fail
- `jest --ci` full suite — 1433 passed / 2 failed; both failures are the
  pre-existing `clone › clone with noTags` 30s-timeout flake
  (`test-clone.js` + `test-clone-in-submodule.js`), reproduced
  identically with and without the patch (27–28s pass, 30s fail)
- `npx eslint src __tests__` — clean
- `npx tsc -p tsconfig.json` — clean (after `rollup -c --no-treeshake` +
  `tsc -p declaration.tsconfig.json`); generated `index.d.ts` includes
  the new `author` param

## Review cycle

Independent read-only subagent review returned **approve-with-nits**;
applied before commit:

1. Reworded the JSDoc to stop claiming exact git parity (reviewer
   verified git's `--author` is case-sensitive BRE).
2. Switched to the repo-wide `@param {string} [args.author]` style.
3. `author: null` now means "no filter" (was `new RegExp(null, 'i')`,
   silently matching nothing).
4. `matchesAuthor` returns an explicit boolean.
5. Blank line + wording fix on the traversal comment ("history is still
   traversed" — the tree is only walked in `filepath` mode).
6. Tightened the invalid-regex assertion to `/Invalid regular expression/`.
7. Added the author-vs-committer test the reviewer flagged as the most
   valuable missing case.

## Deliberate omission

`__tests__/test-log-in-submodule.js` (CONTRIBUTING Appendix A) was **not**
mirrored: that file is behind main (missing e.g. the `includeChanges`
tests) and recent feature PRs #2385/#2413 skipped it too. The PR body
offers to add the mirror if the maintainer prefers.
