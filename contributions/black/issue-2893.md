# psf/black — issue #2893

## Status

**PR #5592 OPENED, MERGEABLE, AWAITING FIRST HUMAN REVIEW —
`docs/readthedocs.org:black` AND `pre-commit.ci` SUCCESS; COPILOT
COMMENTED (quota limit)** — opened 2026-10-23T11:59:34Z, ready for
review (not draft), base `main`, branch based on `main@1190eeb3`, head
`7c38420bcedcb5894a488e21f4ef28e7038de1c1` (3 commits), 5 files,
+161/−0, on the `ShahabAhmed01/black` fork. Not merged. The fix is
gated behind a new Preview flag because Black's stability policy
forbids changing stable output without a preview cycle.

## Issue

https://github.com/psf/black/issues/2893
"Line too long: Keyword argument"

Filed 2022, OPEN, labeled `T: bug` + `F: linetoolong`, no assignee.
Collaborator JelleZijlstra commented "We should fix this". When a
keyword argument's value is a bare attribute chain, Black produced a
line over the limit:

```python
func(
    long_long_long_long_long_long_long_long_long_long_long_arg=
    long_long_long_long_long_class.long_long_long_long_attr
)
```

The reporter's example stayed 118 chars (over 88). Competing sweep at
publication: the issue timeline has no cross-referenced PR, and searches
for `2893` and "keyword argument line" across open PRs found 0 competing
work.

## Root cause

Keyword-argument values (`syms.argument` nodes) get no invisible
parentheses. Assignment right-hand sides do: `visit_stmt` wraps them via
`parens=ASSIGNMENTS`, so `x = value.attr` can split as
`x = (\n    value.attr\n)`. Without those parens an unsplittable value
(a bare attribute chain, plain name, or literal) has no split point: DOT
is not a delimiter when preceded by a NAME, and `=` is not a delimiter
for arguments, so neither `right_hand_split` nor `delimiter_split` has
anything to work with and the whole argument blows past the line length.

## Fix

- `src/black/linegen.py`: a new `visit_argument` hook on `LineGenerator`
  wraps such a value in (invisible) parentheses, mirroring assignments —
  but only under three guards:
  1. the value is genuinely **unsplittable** —
     `_is_unsplittable_argument_value` returns True only when the value
     has no brackets anywhere and no top-level delimiter, decided by the
     real `is_split_before_delimiter`/`is_split_after_delimiter` from
     `black.brackets` so it stays in sync with what `delimiter_split`
     sees;
  2. the name is **≥4 chars**, so moving the value to its own line
     (`8+V` vs `5+n+V`) actually shortens the overflowing line;
  3. the shortest possible `4+len(name)+2` head **fits** the line
     length, else wrapping would just produce a still-too-long line.
- `syms.argument` added to the walrus-protection list in
  `maybe_make_parens_invisible_in_atom` so `f(x=(y := 1))` keeps its
  required parentheses (currently defensive/insurance — a walrus value
  carries brackets so guard 1 excludes it — but it prevents invalid code
  if the guards ever change).
- `src/black/mode.py`: new Preview feature
  `parenthesize_unsplittable_keyword_arguments`.
- Values that already have a split point (calls, subscripts,
  collections, binops, comparisons, string concatenation) are untouched,
  as are arguments whose name alone already overflows.

## Tests

- New data case
  `tests/data/cases/preview_parenthesize_unsplittable_keyword_arguments.py`
  (`# flags: --preview`): the attribute-chain case wraps; a binop and a
  subscript are unchanged; the over-long-name case (`name=0`) is left
  alone (guard 3). A genuine red/green regression test — verified failing
  with the feature gate temporarily disabled (`Preview...in self.mode` →
  `False`) and passing with it restored.
- Full pytest suite (excluding the network-dependent `blackd`):
  **659 passed, 2 skipped, 17 subtests** — baseline was 658 before the
  new case, so zero churn and +1 new test.
- `black --check src tests/test_*.py` clean (56 files unchanged);
  `git diff --check` clean.
- An independent fuzz review (~3000 synthetic inputs + 400 stdlib files,
  plus a baseline-vs-patched diff on ~40 targeted cases) found **no
  invalid, non-idempotent, or crashing output**; outputs are STABLE and
  idempotent across nesting depths and line lengths, and the
  `preview_cantfit_string` expectation (over-long kwarg name) is
  byte-for-byte unchanged.

## CI and review

- `docs/readthedocs.org:black`: SUCCESS.
- `pre-commit.ci - pr`: SUCCESS (a pre-commit.ci auto-fix commit
  `7c38420b` was added on top of the branch and is included in the PR).
- `copilot-pull-request-reviewer`: COMMENTED only (quota limit).
- No human review; no maintainer pinged; `reviewDecision` pending. Not
  merged.

## Notes

- Twenty-eighth tracked contribution and the first psf/black
  contribution; a prior run had declined black only because its then-open
  issues were covered by competing PRs, which no longer held for #2893.
- Black's stability policy (linked in the PR template) requires code-style
  changes to land under `--preview` first, so the behavior is gated
  behind `parenthesize_unsplittable_keyword_arguments`; stable-mode output
  is byte-for-byte unchanged and the reporter's bug is fixed under
  `--preview`/`--unstable`. The changelog entry sits under "Preview
  style" and references #5592 (the PR), per `CHANGES.md`'s convention.
- Workspace: isolated
  `~/opensource-work/runs/ossrun-20261023T093647Z-f689aac5/black`
  (clone of psf/black `main@1190eeb3`, Python 3.12 venv with editable
  black); fork `ShahabAhmed01/black` created this session; the shared
  tracker checkouts were not edited until this record (done in a clean
  `main` worktree).
- Prepared with AI assistance under the account owner's direction; every
  claim above was checked against live GitHub state or a local run.

## Next action

Watch PR #5592 for the first human review; respond on the same branch if
changes are requested. Do not open another black PR while #5592 is open.
If a maintainer moves the preview flag toward stable, re-verify the
`preview_cantfit_string` and short-name guard cases still hold.
