# Project notes — pandas-dev/pandas

Last verified: 2026-10-24

## Facts

- pandas: the reference Python data-analysis library, ~50,260 stars /
  ~20,578 forks (retrieved 2026-10-24 via GitHub API), BSD-3-Clause,
  created 2010-08-24, default branch `main`. Ecosystem-defining wide
  adoption (numpy/dateutil stack; the de-facto tabular-data API in
  Python). Maintained by the pandas core team (Pandas/core pydata
  infrastructure; NumFOCUS fiscally sponsored project).
- Very active: pushed minutes before our observation window closed
  (2026-10-23T20:11:32Z); a large merge cadence on `main` with open
  issues 2,138 (including PRs) at retrieval time.
- Outside-contributor merge evidence within 30 days (retrieved
  2026-10-24): PR #71457 "BUG: interval_range loses precision for large
  integer endpoints" (`author_association: CONTRIBUTOR`) merged
  2026-10-23T16:29:00Z; PR #71337 "DEPR: compound (structured) dtypes in
  DataFrame columns…" (14 files) merged 2026-10-22T22:10:53Z. External
  bugfix PRs with regression tests going through normal review are the
  norm; there is no issue-assignment requirement and no CLA.

## AI / automated contributions policy (contributing.rst)

- Automated tools (AI assistants) are allowed if used **responsibly**:
  (1) disclose the tool in the PR, being specific about which one and
  which model/effort (e.g. `claude opus 4.8 (xhigh)`, not just
  "claude") — say which parts of the work each tool/model was
  responsible for; (2) fully review and modify the result; (3) abide by
  all documented conventions; (4) do not use AI to speak for you in
  issues/PRs/review (quoting AI output requires `>` or a code fence).
- `AGENTS.md` additionally says a contributor's agent must not perform
  issue/PR actions on the repository "on behalf of the user"; in this
  workflow the account holder directs the work and the disclosure names
  the harness/model explicitly, so the reviewer can apply the right
  scrutiny. Reservations in the coordination ledger are our own
  discipline; pandas has no per-repo reservation mechanism.
- Maintainers may reject contributions that don't follow the policy;
  repeated violations (2+) can lead to a contribution ban. Honor it
  strictly: disclosure block in every pandas PR body.

## Development environment (as used in this workflow)

- Project-official tooling is conda (`environment.yml`) or pixi
  (`pixi.toml`, what pandas CI uses); we validated with a plain
  `uv venv` + editable meson build, which works on this box (gcc 16,
  32 threads):
  - `uv venv --python 3.12 .venv`
  - build deps per `pyproject.toml [build-system]`:
    `meson-python>=0.19,<1`, `meson>=1.2.3,<2`, `wheel`, `Cython>3.1,<4`,
    `numpy>=2.0,!=2.5.0,<3`, `versioneer[toml]`, `ninja`, plus runtime+
    test deps `python-dateutil pytz tzdata pytest pytest-xdist pytest-cov
    pytest-cython hypothesis pytest-localserver`
  - `uv pip install -e . --no-build-isolation` (about 2-3 min, 32-core)
  - note: pandas is NOT on the `pull_request_creation_policy:
    collaborators-only` list; plain fork PRs are fine.

## Testing facts

- Targeted suites used for the tz-parsing change:
  `pandas/tests/tslibs`, `pandas/tests/tools`,
  `pandas/tests/scalar/timestamp` (pytest, `-n 12`).
- **Pin `python-dateutil==2.9.0.post0`** exactly as pandas CI does (CI
  pinned `dateutil<3` on 2026-10-22, #71461): dateutil 3.0.0 changes
  baseline tz behavior and produces ~12 environment pre-existing
  failures in tz-heavy suites (verified here with and without a local
  change; identical failure set).

## CI / PR mechanics for outside PRs

- ~40 Actions workflows run per PR (unit tests across platforms/Python
  versions, docbuild, doctests, type checking, ASAN/UBSAN, musl,
  32-bit, locales, freethreading, nightly numpy/pyarrow…). First-time
  contributor forks go through the usual first-time-contribution
  workflow approval for some Anthropic-/repo-configured workflows when
  configured.
- **pre-commit.ci runs on the PR with autofix disabled**
  (`autofix_prs: False`) — the list of hooks is long (ruff, cython-lint,
  codespell, sphinx-lint, isort, local validation hooks…); the
  `sort-whatsnew-items` hook orders whatsnew lines lexically, so the
  entries for ONE fix should sit in lexical order among the section
  (newest issue number last inside a block, tie → line-text lexical).
  If it fails, re-run the same hook locally
  (`python -m scripts.sort_whatsnew_note doc/source/whatsnew/v3.2.0.rst`)
  and push; do not wait for the bot to autofix (it can't).
- whatsnew: one entry per user-visible effect under the right section
  (`doc/source/whatsnew/v3.2.0.rst` for this time window), referencing
  the issue number, e.g. `(:issue:`71273`)`.

## Timezone/offset semantics (relevant to #71273)

- Polar pairs: dateutil applies the POSIX (sign-inverted) reading for
  zone-name+numeric-offset strings ("UTC+0300" → −3h), while
  `strptime('%z')` applies the nominal sign (+3h) — so a format
  guessed from a string that dateutil parsed POSIX-style can make
  `pd.to_datetime` disagree by the full offset with
  `pd.Timestamp`/`format="mixed"` (which parse with dateutil).
- `guess_datetime_format` (Cython, `pandas/_libs/tslibs/parsing.pyx`)
  normalizes offset tokens via `parsed_datetime.strftime("%z")` —
  that path accepts the rewritten token against the *rebuilt* string,
  which made the guessed format self-consistent but WRONG for the
  original string (GH#71273).
- Zero offsets are unaffected (all paths agree; GH#66827 context):
  `"UTC+0000"` keeps a guess.

## Acceptance record

- Issue #71273 (2026-10-17, filed by `digit50`, `Needs Triage`, open,
  unassigned, zero comments at selection) and PR #71508 were worked
  2026-10-24 (coordinated run ossrun-20261024T065401Z-adb75e71,
  reclaiming a prior run's unpublished implementation after live-state
  verification: no commits or PRs referenced the issue). At the time of
  writing the PR is open, non-draft, `main@c4d25081`-based, 4 files
  +105/−0 with a red/green regression proof, targeted suites green
  (dateutil pinned to 2.9.0.post0), all applicable pre-commit hooks
  clean locally, awaiting first human review and full CI.
