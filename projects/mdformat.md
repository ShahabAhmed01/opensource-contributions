# Project notes — hukkin/mdformat

Last verified: 2026-11-06

## Facts

- CommonMark-compliant Markdown formatter (CLI + library, commonmark-hs via
  `markdown-it-py`). MIT License. 829 stars / 67 forks, created 2020-07-11,
  default branch `master` (live 2026-11-06). Python, requires >= 3.10.
- The GitHub URL `executablebooks/mdformat` redirects to **`hukkin/mdformat`**
  (repository moved back to the author's account); issue/PR numbers are
  unchanged and old links keep working. Reserve and record under
  `hukkin/mdformat`.
- No CONTRIBUTING.md at the root; contributor docs live at
  `docs/contributors/contributing.md` (plugin development focus). No CLA/DCO
  table, no AI-assistance policy found. Issues enabled, `bug` label in use;
  issue #572 carries it.
- Test layout: plain markdown test files under `tests/data/` — a case is the
  input block, `.` lines, expected block; `--check`/style behaviors covered in
  `tests/test_style.py` etc. `test_for_profiler` formats the repository's own
  README + docs, so doc changes must be mdformat-formatted themselves.
- CI: `.github/workflows/tests.yml` (pytest matrix) plus
  `pre-commit.ci - pr` and `docs/readthedocs.org:mdformat` statuses.
- Layout: `mdformat/` package (renderer split into `mdformat/renderer/`,
  plugins under `mdformat/plugins/`), `tests/`, `docs/`, `pyproject.toml`
  with `bump2version` (the version line has a DO-NOT-EDIT marker).

## Development / validation commands

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e . pytest mypy black flake8 pre-commit
# focused style checks
.\.venv\Scripts\python.exe -m pytest tests/test_style.py tests/test_api.py tests/test_context.py tests/test_renderer_util.py -q
# the repo's own docs must stay formatted
.\.venv\Scripts\python.exe -m pytest tests/test_for_profiler.py -q
.\.venv\Scripts\python.exe -m mdformat --check README.md docs\users\style.md
# full local suite (Windows)
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\black.exe --check src\mdformat\renderer\_context.py
.\.venv\Scripts\flake8.exe src\mdformat\renderer\_context.py
.\.venv\Scripts\mypy.exe src\mdformat\renderer\_context.py
```

- Pre-existing Windows failures (identical on unmodified upstream
  `56b24ef`): `test_fmt_file__symlink`, `test_format__symlinks`,
  `test_broken_symlink` (all `OSError: [WinError 1314] A required privilege
  is not held by the client`) and `test_check__multi_fail`. Diff a full-suite
  run against the unpatched baseline before blaming your change.
- Renderer spacing decisions live in `mdformat/renderer/_context.py`
  (`make_render_children` builds the block separator; root, block_quote and
  `list_item` are the callers that matter for inter-block spacing, and list
  items care because the separator decides tight vs. loose).
