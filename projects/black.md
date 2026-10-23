# Project notes — psf/black

Last verified: 2026-10-23

## Facts

- The reference Python code formatter: ~42k stars, MIT license, pure
  Python (no native build), installable offline via a venv with an
  editable install. Default branch `main`; PRs target `main`.
- `pull_request_creation_policy: all` — external contributors may open
  PRs (no collaborators-only gate). No CLA, no assignment gate, no
  AI-contribution block, no commit-trailer bot; nothing here rejects
  agent-authored work out of hand.
- Test suite is self-contained and offline: `python -m pytest tests/ -q
  -n auto --ignore=tests/test_blackd.py` (blackd needs a running
  server/HTTP and is skipped). Data-driven cases live in
  `tests/data/cases/*.py`; a case with `# flags: --preview` (or
  `--unstable`) opts into preview mode, and the harness also re-runs each
  case at `line_length=1` in both preview and non-preview modes purely to
  catch stability (idempotency) bugs — it does not compare those runs to
  the expected output.
- `tests/data/` is `extend-exclude`d in `pyproject.toml`, so data cases
  are not black-formatted by the self-check; `black --check src
  tests/test_*.py` is the clean self-format gate (56 files).
- Every `Preview` enum member not in `UNSTABLE_FEATURES` must be
  documented in `docs/the_black_code_style/future_style.md`; the
  `test_feature_lists_are_up_to_date` test fails otherwise. `--preview`
  and `--unstable` enable all such members; only `string_processing` and
  `hug_parens_with_braces_and_square_brackets` are in `UNSTABLE_FEATURES`
  (opt-in via `--enable-unstable-feature`).
- **Stability policy:** code-style changes are only allowed under the
  `--preview` flag until maintainers move them to stable in the next
  calendar year (stated in the PR template checklist). Output-changing
  fixes must therefore land gated behind a new `Preview` flag; stable-mode
  output stays byte-for-byte unchanged. `CHANGES.md` has a "Preview
  style" section for these, and entries reference the **PR number, not
  the issue number**.
- Contribution policy: follow the PR template (Description +
  Checklist); familiarize yourself with the stability policy; all
  user-facing changes need a `CHANGES.md` entry; tests are required for
  all bugfixes and new features; documentation changes are needed for
  most formatting changes. `docs/contributing/reference/contributor_
  guidance.md` is the detail reference. No requirement to comment "please
  review" — maintainers review when ready.
- CI on a first-time fork PR: `pre-commit.ci - pr` and
  `docs/readthedocs.org:black` run; there is no `action_required`
  workflow-approval gate like some other repos, and no CLA bot. Copilot
  review may come back quota-limited (COMMENTED only).

## Line-too-long mechanics (relevant to #2893)

- Assignment right-hand sides get invisible parentheses via
  `visit_stmt(parens=ASSIGNMENTS)`, so `x = value.attr` can split as
  `x = (\n    value.attr\n)`. Keyword-argument values (`syms.argument`)
  had no equivalent, so an unsplittable value had no split point (DOT is
  not a delimiter when preceded by a NAME; `=` is not a delimiter for
  arguments) and the line stayed over the limit (#2893).
- `visit_argument` (added by PR #5592) mirrors the assignment behavior
  for keyword arguments, gated behind the Preview flag
  `parenthesize_unsplittable_keyword_arguments`, and only when the value
  is genuinely unsplittable and wrapping can actually help (head fits,
  name ≥4 chars). Precedent Preview flags in the same family:
  `avoid_parens_for_unbreakable_rhs_in_assignments`,
  `wrap_long_dict_values_in_parens`, `parenthesize_expressions_with_
  comments`.

## Acceptance record

- Issue #2893 (2022, `T: bug` + `F: linetoolong`, unassigned;
  collaborator JelleZijlstra: "We should fix this") and PR #5592 were
  worked 2026-10-23. At the time of writing, PR #5592 is open, MERGEABLE,
  not draft, `docs/readthedocs.org:black` and `pre-commit.ci` SUCCESS,
  Copilot COMMENTED, with no human review (`reviewDecision` pending). The
  fix is 5 files, +161/−0, with a red/green regression test, a clean
  659-pass full suite, and an independent fuzz review showing no invalid
  or unstable output.
