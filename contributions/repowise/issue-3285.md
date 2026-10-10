# repowise-dev/repowise — #3285

## Status

PR open and MERGEABLE, awaiting maintainer review and the first-time-contributor
CI approval gate. Not merged.

## Issue

https://github.com/repowise-dev/repowise/issues/3285
"Ternary chains count every arm as a nesting level outside TypeScript and JavaScript"
Labels: `bug`, `help wanted`

Created 2026-10-10T10:26:28Z. Unassigned at selection and still unassigned at PR
creation. Claimed by comment per `.github/CONTRIBUTING.md` ("That comment is what
reserves the issue"): https://github.com/repowise-dev/repowise/issues/3285#issuecomment-6098334087
(2026-10-10T14:08:29Z) — the issue's only comment. No competing PR at selection, at
commit, or immediately before opening ours (searched open PRs for `3285`, `ternary`,
`conditional expression`; the only hits were merged PRs #3278/#2816/#2680/#2225).

The issue is explicitly multi-language: nine grammars are listed, with the instruction
"one language per commit or per PR" and "Python is a good one to start with".

## Pull Request

[#3338 — fix(health): a Python conditional-expression chain nests like an elif dispatch](https://github.com/repowise-dev/repowise/pull/3338)

- Base branch: `main`
- Opened: 2026-10-10T16:55:51Z
- State: open, `MERGEABLE`, not a draft; 1 commit, 4 files, +76/−8
- Fork head: `ShahabAhmed01:fix/flat-ternary-python-3285-v2` @ `b8224eefeaa2`
- Related to #3285 (not "Closes") — Python only, so the issue stays open for the
  other eight grammars

## Branch

`fix/flat-ternary-python-3285-v2` from `upstream/main` @ `b010215`.

The workspace is a shallow clone (`--depth 60`), so `git rebase` has no merge-base and
resolves as a whole-tree add/add conflict. The first attempt was aborted and the commit
was **cherry-picked** onto the new main instead — use cherry-pick, not rebase, in this
workspace. `main` moved twice more during the session (`b010215` → `3289287` →
`342046f`); neither delta touched any file this branch changes, so GitHub reports
MERGEABLE and no further rebase was applied.

## Commits

- `b8224eefeaa2dba7955b54878012e66bb9d50ef7` — fix(health): a Python
  conditional-expression chain nests like an elif dispatch (4 files, +76/−8)

## Problem

`a if p else b if q else c` reported `max_nesting 3` in Python while the equivalent
`if / elif / elif / else` chain reported `max_nesting 1` — and the identical ternary
chain in TypeScript reported `1`. A flat dispatch chain, which reads as a lookup
table, pushed `max_nesting` and with it the `nested_complexity` health score, for
code that is not hard to follow.

Measured on this branch, with the flag toggled off to reproduce the pre-fix walker
(`walk_file` from `repowise.core.analysis.health.complexity`):

| snippet | ccn | nesting before | nesting after |
|---|---|---|---|
| `return 1 if a else 2 if b else 3 if c else 4` | 4 | **3** | **1** |
| `if a / elif b / elif c / else` | 4 | 1 | 1 |
| `if a: return 1 if b else 2` (a real nest) | 3 | 2 | 2 |

The chain now scores exactly what the `elif` dispatch it compiles to scores, and real
nesting is untouched.

## Root Cause

PR #3278 (merged 2026-10-10T11:14:20Z, `84f1499`) already made ternary chains flat,
by adding an opt-in `flat_ternary_kinds` field to `LanguageNodeMap` and setting it for
TypeScript and JavaScript. `_is_flat_ternary` uses it to classify a ternary as a flat
dispatch arm and hand the else-arm to the enclosing `walk_if` instead of descending.

It works only for grammars that expose the ternary's two arms as named fields.
`walk_if` reads `node.alternative` to find the else arm. Python's tree-sitter grammar
exposes no `consequence` and no `alternative` on `conditional_expression` — both arms
are bare `body` / `orelse` children. So for Python `_ternary_else_arm` would have read
an always-`None` field, and every `ifexp` fell through to the default `1 + …` branch.
Setting `flat_ternary_kinds` alone on the Python map would have flattened the arms and
lost the decision points at the same time, so the flag could not simply be copied over.

TypeScript was the only language #3278 could reach, because its grammar is the one of
the nine that does name `consequence` / `alternative`.

## Solution

Extend #3278's mechanism rather than add a second one, as the issue asks.

`LanguageNodeMap` gains `ternary_arms_positional: bool = False`, which names the second
contract difference flat kinds cannot express: the arms are positional (Python's bare
`body` / `orelse` children) rather than named. Only `_PY` sets it; every other map,
including `_TS`, is unchanged, so no other language's behaviour moves.

`_ternary_else_arm()` in `cyclomatic.py` carries the language-specific resolution: with
the flag on it takes the last `body` child that is itself a conditional expression (the
`ifexp` of `x if c1 else (y if c2 else z)`), which also makes the parenthesised form
`(y if c2 else z)` and the nested left-arm form resolve correctly; with the flag off it
reads `node.alternative`, exactly as before. `walk_if` is untouched, and the helper is
called only when the node is already known to be a flat ternary, so the extra pass over
the children costs nothing on any other node.

The cognitive-complexity side needed no change: #3278 already gives a flat ternary a
`+1` and no nesting, and that path was language-independent.

## Files Changed

- `packages/core/.../complexity/languages.py` — `ternary_arms_positional` field on
  `LanguageNodeMap`, set on `_PY` beside its existing `flat_ternary_kinds`
- `packages/core/.../complexity/cyclomatic.py` — `_ternary_else_arm()` helper;
  `_is_flat_ternary`'s call site now asks it for the else arm
- `tests/unit/health/test_jsx_ternary_nesting.py` — 5 new Python tests;
  `test_python_conditional_expression_chain_unchanged` renamed to
  `..._chain_is_flat`, because it pinned the nesting this PR removes
- `packages/core/.../complexity/README.md` — one bullet on the new map field

The file set matches #3278's exactly minus `docs/architecture/code-health.md` and
`extract_method.py` (its two unrelated edits): same walker, same map, same test file.

## Tests

- **Regression proof:** the 5 new tests fail on the unfixed walker with nesting
  3/3/2 (chain, parenthesised arm, nested left arm) before passing — TDD, written
  against the failing behaviour first.
- **Focused:** `uv run pytest tests/unit/health/test_jsx_ternary_nesting.py -q` —
  78 passed (14 tests in that file, 5 of them Python).
- **Touched-surface:** `uv run pytest tests/providers/ tests/unit/health/ -q` —
  3639 passed, 2 skipped, 2 xfailed on the pushed head `b8224ee` (1m09s).
- **Full suite:** `uv run pytest tests/unit/ -q` — 28724 passed, 20 skipped,
  6 xfailed (1h28m31s) on the pre-rebase base `bc89359`; the branch is a pure
  cherry-pick onto `b010215`, the delta is upstream-only and the changed files are
  byte-identical, and a second full run on `b8224ee` was in flight at PR time.
- **Lint / types:** `uv run ruff check .` clean; `uv run mypy` clean on both changed
  source files. `git diff --check` clean.
- **Docs:** the doc-drift gate passes — the README bullet and the `_PY` map field
  landed in the same commit.

**No golden or fixture updates were needed.** The issue asks each language to update
its health-score goldens, but #3278 — the accepted precedent for TypeScript and
JavaScript — changed no golden or fixture file either (verified against its 6 files),
and a full-suite run finds no Python golden that scores a conditional-expression
chain. `tests/unit/persistence/golden` and `tests/unit/server/golden` hold unrelated
snapshots.

## CI

- First push 2026-10-10T16:5xZ: the `CI` workflow for `b8224ee` completed with
  conclusion `action_required` — GitHub's first-time-contributor approval gate, a
  protection to be waited on, not bypassed. No check has reported yet, so
  `gh pr checks` reads "no checks reported on the branch".
- PR is `MERGEABLE`; `mergeStateStatus` is `BLOCKED` solely on the pending
  checks/review.
- The gates that will run are the ones already executed locally: `uv run pytest
  tests/providers/` then `uv run pytest tests/unit/ -n auto`, `uv run ruff check .`,
  and the documentation-drift job.

## Review

_None yet._ No comments, no reviews, no requested changes.

## Merge

_Not merged._

## Lessons Learned

- Read the blocking PR's diff before designing the fix: #3278's six files told me the
  exact seam to extend, which test file the maintainer expects the cases in, and (by
  its absence) that no golden updates are owed — three questions answered for free.
- An opt-in flag that encodes one contract difference cannot always express two.
  "Flat kinds" says *what*; Python also needed *how the arms are reached*. Naming the
  second difference as its own field keeps `_TS` and every other map untouched, which
  is what makes the diff four files instead of nine.
- A frozen dataclass map is a cheap A/B rig: `dataclasses.replace(LANGUAGE_MAPS["python"], ternary_arms_positional=False)` re-measures the pre-fix walker in the
  same process, so before/after numbers in the PR come from one interpreter with one
  variable changed.
- In a shallow clone, `git rebase` across a moved base is a whole-tree add/add
  conflict; `git cherry-pick <sha>` onto a fresh branch from the new base is the
  operation that works.
- This repo is fast: `main` moved three times in one session. Checking whether the
  new commits touch your files is cheaper than rebasing, and keeps the PR head
  stable for reviewers.
- `walk_file(path, language, source_bytes)` — the source is bytes and the path is
  positional first; the returned functions expose `ccn`, not
  `cyclomatic_complexity`.
