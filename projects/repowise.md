# Project notes — repowise-dev/repowise

Last verified: 2026-10-10

## Facts

- "Codebase intelligence for AI and humans: code health scores, auto-generated
  docs, git analytics, dead code detection, and architectural decisions via MCP."
  AGPL-3.0. ~7438 stars. Created 2026-03-23; very active (`main` moved three
  times in a single working session on 2026-10-10).
- Python (a `uv` workspace under `packages/`, ~3000 files) plus a TypeScript /
  React frontend in `packages/ui`. Default and only development branch: `main`.
- The health layer this track touches lives at
  `packages/core/src/repowise/core/analysis/health/complexity/` — a tree-sitter
  walker (`walker.py`), a per-language node map (`languages.py`, frozen
  dataclasses keyed by language name), and the cyclomatic/cognitive pass
  (`cyclomatic.py`).
- Contribution guide is `.github/CONTRIBUTING.md`, not a root `CONTRIBUTING.md`.
  PR template is `.github/PULL_REQUEST_TEMPLATE.md` (Summary 1–3 bullets,
  Related Issues, Test Plan with checkboxes, Checklist) — `gh pr create` does
  not load it, pass `--body-file`.
- One of the repo's own CI checks enforces Conventional Commits on the PR title
  ("Check PR title (Conventional Commits)").
- The repo keeps a self-hosted, always-fresh public index of itself at
  `repowise.dev/repo/repowise-dev/repowise`, and a `doc-drift` CLI gate that
  fails a PR whose docs no longer match the code it documents.

## Development / validation commands

```bash
uv sync --all-packages            # the whole uv workspace
npm install && npm run build      # the frontend (n/a for core-only changes)
uv run repowise --version         # sanity check

uv run pytest tests/providers/ tests/unit/     # what CI runs on every PR
uv run pytest tests/unit/health/test_<file>.py -q   # one file
uv run pytest tests/providers/ tests/unit/health/ -q  # touched surface, ~1m

uv run ruff check .               # NOT ruff format — format is not a gate
uv run mypy <changed files>       # types, not run repo-wide by CI
uv run repowise doc-drift --check --baseline .github/doc-drift-baseline.json --format github
git diff --check                  # whitespace
```

- CI (`ci.yml`) jobs: `test-python` (providers, then unit with `-n auto`),
  `test-tree-sitter-floor` (pins tree-sitter to the declared floor and compiles
  every query), `lint-python` (ruff), `doc-drift`, and `test-integration`
  (push to `main` only).
- Full `tests/unit/` takes ~1h28m locally on this machine (28724 tests);
  `tests/providers/` + `tests/unit/health/` is the ~1 minute touched-surface
  set. The `--timeout` pytest flag is unavailable (plugin not installed).

## Contribution policy (`.github/CONTRIBUTING.md`)

- **Claim by comment.** "That comment is what reserves the issue, from the
  moment you post it." A maintainer assigns later; an empty assignee field does
  not make a claimed issue available again. Only the claimant should open a PR —
  a PR over somebody's claim "will be held, not merged, however good it is".
- A claim expires after **two weeks of silence**; a one-line comment unclaims.
  Asking about scope is not claiming.
- Tests are expected for bug fixes, and the guide points at the repo's own
  health layer as the way to learn how Repowise thinks.
- First-time contributors hit GitHub's `action_required` gate: the fork's
  workflows do not run until a maintainer approves them. Wait for it; do not
  try to route around it.

## Why this project was selected (2026-10-10 research)

- The issue is a genuine, maintainer-authored defect with a measured before/after
  table and a prescribed approach ("extend #3278's mechanism, one language per
  commit or per PR") — the acceptance criteria are written down.
- The blocking PR (#3278) had merged the same morning, so the work was unblocked
  and the precedent for exactly which files to touch was visible in public.
- Human maintainers do review: `RaghavChamadiya` (author of 89 of the last 100
  merged PRs, running the project's own agent loop as well) and `swati510`.
- External merges are real but a minority: **11 of the last 100 merged PRs came
  from outside authors**, one each, from 11 distinct accounts (rishu685,
  Aman-goel-04, Nehant14, Pushpak731, SatvikMishra08, abhinavrastogi2627,
  inchang-ing, kudala-bharani, limitcool, tecsmurf, sloemo01). Recorded
  honestly: this is a maintainer-driven repo, so acceptance here is slower and
  less certain than on backlot — the value is that the issue was scoped, the
  precedent existed, and the fix was verifiable end to end.
- The codebase is large but the change surface is tiny and well-tested, and the
  repo publishes its own index, so the surrounding design was cheap to check.

## Pitfalls learned

- **Shallow clone (`--depth 60`): `git rebase` across a moved base has no
  merge-base and becomes a whole-tree add/add conflict.** Use
  `git cherry-pick <sha>` onto a new branch cut from the new base instead.
- **Grammars differ in what they expose.** TypeScript's ternary names
  `consequence`/`alternative`; Python's `conditional_expression` names neither —
  both arms are bare `body`/`orelse` children. Any walker logic that reads a
  named field must ask the language map how to reach the arms.
- A `LanguageNodeMap` is a frozen dataclass; `dataclasses.replace()` on the
  entry in `LANGUAGE_MAPS` is a one-variable A/B rig for measuring the
  pre-fix walker in the same process.
- `walk_file(path, language, source_bytes)` — path first, source as **bytes** —
  and the returned `FunctionComplexity` exposes `ccn`, not
  `cyclomatic_complexity`.
- `main` moves fast here. Before rebasing, check whether the new commits touch
  your files; if not, leave the PR head stable.
- The issue text asks each language to update its health-score goldens, but
  #3278 — the accepted precedent — updated none, and no Python golden scores a
  conditional-expression chain. State that explicitly in the PR rather than
  silently omitting the goldens.

## Contribution history

### #3285 — Python ternary chains (PR #3338 open, 2026-10-10)

- Branch: `fix/flat-ternary-python-3285-v2`; PR:
  https://github.com/repowise-dev/repowise/pull/3338 (base `main`), related to
  https://github.com/repowise-dev/repowise/issues/3285 (Python half of a
  nine-grammar issue, so the issue stays open).
- Fix: `LanguageNodeMap.ternary_arms_positional` (set only on `_PY`) plus a
  `_ternary_else_arm()` helper, so `a if p else b if q else c` reports one `if`
  decision instead of one per `ifexp` — `max_nesting` 3 → 1, matching the
  `elif` dispatch it compiles to. `walk_if` and every other map untouched.
- Validation: 5 new tests fail on the unfixed walker (nesting 3/3/2) before
  passing; focused file 78 passed; touched surface (providers + health) 3639
  passed on the pushed head; full `tests/unit/` 28724 passed on the pre-rebase
  base; ruff, mypy, doc-drift and `git diff --check` all clean.
- Opened 2026-10-10T16:55:51Z, MERGEABLE, awaiting the first-time-contributor
  CI approval gate and maintainer review. Full detail in
  `contributions/repowise/issue-3285.md`.
