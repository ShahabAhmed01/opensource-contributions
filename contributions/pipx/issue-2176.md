# pypa/pipx — issue #2176

## Status

**PR #2177 OPENED, READY FOR REVIEW — 2 EXTERNAL STATUSES SUCCESS;
GITHUB ACTIONS TESTS/ZIZMOR AWAIT MAINTAINER APPROVAL (first-time
contributor), NO HUMAN REVIEW** — opened 2026-10-21T19:35:20Z as a draft,
marked ready for review shortly after opening, base `main` @
`0c4acc88fc4d62b9a85f9c0cff8c938f81c84c2b` (verified current at commit and
publication), head `83fd7a8f82cb6adc84c44adf636c8743a18cf5b2`, 2 commits,
3 files, +62/−4, on the `ShahabAhmed01/pipx` fork. Not merged.

## Issue

`pypa/pipx` issue #2176, filed by this run on 2026-10-21T19:30:20Z:
"Bare local archives with .tar.xz, .tar.bz2, .tgz, or .tar are treated as
PyPI names". OPEN, 0 comments, no assignee, no labels at publication.
The issue body carries the minimal-sdist reproduction, the bare-vs-`./`
output, the affected extensions, and the expected pip-compatible
behaviour.

## Root cause

`src/pipx/package_specifier.py` defined
`ARCHIVE_EXTENSIONS = (".whl", ".tar.gz", ".zip")`. A bare filename such
as `empty_project-0.1.0.tar.xz` is a valid PEP 508 requirement name, so
`valid_pypi_name()` returned the canonicalized name
`empty-project-0-1-0-tar-xz` and `package_name_from_spec()` skipped local
path resolution. Pipx then asked pip for the canonicalized project name,
which does not exist, instead of the file in the current directory.
Prefixing the filename with `./` made the PEP 508 parse fail, so the
local-path branch ran and the archive installed correctly.

Pip's own `ARCHIVE_EXTENSIONS` (`pip._internal.utils.filetypes`) also
contains `.tar.bz2`, `.tbz`, `.tar.xz`, `.txz`, `.tlz`, `.tar.lz`,
`.tar.lzma`, `.tgz`, and `.tar`, and `is_archive_file()` matches them
case-insensitively.

## Fix

- Aligned `ARCHIVE_EXTENSIONS` with pip's full tuple.
- Added `_is_archive_name()` and used it in `_parse_specifier()`,
  `valid_pypi_name()`, and `fix_package_name()` so the suffix match is
  case-insensitive.
- Added regression tests for every extension, mixed-case extensions, and
  missing archive paths.

The change is deliberately independent of the concurrent extras fix for
#2173 (PRs #2174/#2175), the inline-metadata delimiter fix for #2171
(PR #2172), and the `runpip` option-value fix for #2165 (PR #2166). It
touches only archive-extension recognition.

## Tests

- `python -m pytest tests/test_package_specifier.py -q` -> `166 passed`
  on Python 3.11.17.
- The same targeted suite -> `166 passed` on Python 3.15.0.
- End-to-end with a valid `.tar.xz` sdist built from pipx's
  `testdata/empty_project`: before the fix the bare filename failed with
  `Could not find a version that satisfies the requirement
  empty-project-0-1-0-tar-xz`; after the fix the bare filename and an
  uppercase `.TAR.XZ` filename both installed `empty-project 0.1.0` and
  recorded the archive's absolute path in `pipx_metadata.json`.
- `pre-commit run --files src/pipx/package_specifier.py
  tests/test_package_specifier.py changelog.d/2177.bugfix.md` passed
  (ruff, flake8-lazy, codespell, mdformat, end-of-file/trailing-space
  hooks).
- `ruff check` and `ruff format --check` pass on the changed files.

## CI and review

- `pre-commit.ci - pr`: SUCCESS.
- `docs/readthedocs.org:pipx`: SUCCESS.
- GitHub Actions `🧪 tests` and `zizmor` runs: `action_required` — the
  first-time-contributor workflow-approval gate. Not bypassed; no
  maintainer was pinged.
- Copilot review: COMMENTED, but the body says Copilot could not review
  because the requester reached the quota limit. No human review and no
  comments on the PR at the time of writing.

## Notes

- Twenty-fifth tracked contribution and the first `pypa/pipx`
  contribution. pipx is a PyPA project (MIT, 12,983 stars / 625 forks at
  2026-10-21; 13 open issues+PRs; active pushes). External PRs have
  merged recently (#2160, #2157, #2150), and no AI-specific contribution
  policy was found in `docs/contributing.rst` or
  `.github/CONTRIBUTING.md`.
- The bug was self-discovered during a read of the package-specifier
  parser, not taken from the open issue pool. Competing-work sweep:
  GitHub issue/PR searches for `tar.xz`, `tar.bz2`, `.tgz`, and
  `ARCHIVE_EXTENSIONS` found no matching issue or PR before #2176 was
  filed.
- Workspace: isolated
  `~/opensource-work/runs/ossrun-20261020T143633Z-2eff4030/upstream/pipx`
  (shallow clone of `main` @ `0c4acc8`), Python 3.11.17 via
  `uv sync --frozen --group test`, Python 3.15.0 via a separate
  `.venv315`; `pip` had to be installed in the 3.15 environment because
  the test conftest's package-cache script invokes it. Fork created this
  session. The shared tracker working tree was not used.
- Prepared with AI assistance under the account owner's direction; every
  claim above was checked against live GitHub state or a local run.

## Next action

Watch PR #2177 for the workflow-approval gate and the first human review;
respond on the same branch if changes are requested. Do not open another
pipx PR while #2177 is open, and do not duplicate #2173/#2174/#2175,
#2171/#2172, or #2165/#2166.
