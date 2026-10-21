# Project notes — pypa/pipx

Last verified: 2026-10-21

## Facts

- PyPA's tool for installing and running Python applications in
  isolated virtual environments, with a `pipx run` path for one-off
  execution and `pipx install` for persistent apps. MIT; 12,983 stars /
  625 forks (live 2026-10-21); 13 open issues+PRs; active pushes (last
  2026-10-21T17:41:51Z). Python >=3.11.
- Default branch `main`; PRs target `main`. The package is
  `src/pipx/`; tests are in `tests/`; test data is in `testdata/`.
- Test setup: `uv sync --frozen --group test` creates a virtualenv with
  the test group. The suite is pytest-based. The conftest runs
  `scripts/list_test_packages.py` to build a package cache, so a `pip`
  executable must be on `PATH` in the test environment; a bare
  `uv sync` environment does not install pip. Python 3.15 tests need
  `uv python install 3.15` and a separate environment
  (`UV_PROJECT_ENVIRONMENT=.venv315 uv sync --frozen --python 3.15
  --group test`) plus `uv pip install --python .venv315/bin/python pip`.
- Lint/format: pre-commit hooks pin ruff 0.17.0, flake8-lazy, codespell,
  mdformat (with the MkDocs/GFM plugins), yamlfmt, and the standard
  pre-commit-hooks. `default_language_version.python` is `python3.15`,
  so pre-commit needs a Python 3.15 executable on `PATH`.
- Changelog: towncrier fragments in `changelog.d/`, named
  `<number>.(feature|bugfix|performance|doc|removal).md`; the
  pre-commit hook enforces the naming. `docs/contributing.rst` asks for
  a fragment and a PR that references an open issue.
- PR template: run the linter, add tests, add a news fragment, update
  docs if needed, run tests on Python 3.11 and 3.15, keep the PR in
  draft until CI passes.
- First-time-contributor PRs: the GitHub Actions `🧪 tests` and `zizmor`
  workflows sit at `action_required` until a maintainer approves the
  run. This is a platform protection, not a failing check; do not try to
  bypass it and do not ping.
- Maintainer activity: `gaborbernat` is active and merges external
  PRs; recent examples are #2160 (`XXXXXQ-0206`), #2157 (`AryanRG`), and
  #2150 (`srijan2607`), all merged 2026-10-15..17.
- No AI-specific contribution policy was found in
  `docs/contributing.rst` or `.github/CONTRIBUTING.md`; the standard PSF
  Code of Conduct applies.

## Package-specifier facts

- `src/pipx/package_specifier.py` parses a package spec into a PEP 508
  requirement, a URL, or a local path. `ARCHIVE_EXTENSIONS` controls
  which bare filenames are treated as local archives; it previously held
  only `.whl`, `.tar.gz`, and `.zip`.
- Pip's `ARCHIVE_EXTENSIONS` (`pip._internal.utils.filetypes`) is
  `.zip`, `.whl`, `.tar.gz`, `.tgz`, `.tar`, `.tar.bz2`, `.tbz`,
  `.tar.xz`, `.txz`, `.tlz`, `.tar.lz`, `.tar.lzma`; pip's
  `is_archive_file()` lowercases the name before matching.
- A bare archive filename is a valid PEP 508 requirement name, so
  `valid_pypi_name()` can short-circuit local-path resolution unless the
  suffix is recognized. Prefixing with `./` forces the local-path
  branch. `parse_specifier_for_install()`,
  `parse_specifier_for_metadata()`, and `parse_specifier_for_upgrade()`
  all go through `_parse_specifier()`.
- Concurrent lanes to avoid duplicating: #2173 (extras on bare local
  archives; PRs #2174/#2175), #2171 (inline-metadata delimiter; PR
  #2172), and #2165 (`runpip` value-taking options; PR #2166).

## Acceptance record

- Issue #2176 and PR #2177 were opened 2026-10-21. At the time of
  writing, the PR had `pre-commit.ci` and Read the Docs green, the
  GitHub Actions test matrix awaiting maintainer approval, Copilot
  quota-limited, and no human review. The fix is 3 files, +62/−4, with
  regression tests for every pip-supported archive extension and mixed
  case.
