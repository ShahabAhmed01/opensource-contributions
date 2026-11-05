# Project notes — jupyter/jupyter_client

Last verified: 2026-11-05

## Facts

- Reference implementation of the Jupyter protocol plus the client and
  kernel-management APIs (and the `jupyter kernelspec` / `jupyter run`
  entry points). BSD-3-Clause. 481 stars / 327 forks, created 2015,
  default branch `main` (live 2026-11-05).
- Outside-contribution pathway: GitHub reports
  `pull_request_creation_policy: all`. Recent merged cross-repository
  PRs: #1142 (krassowski, 2026-08-28), #1140 (Yann-P, 2026-08-24),
  #1139 (MsfPablo, 2026-08-28), #1136 (aryansk, 2026-08-28).
- `CONTRIBUTING.md` delegates to the IPython contributing guide. That
  guide explicitly allows agents; it requires two robot emojis (🤖🤖)
  in both the commit message and the PR text, plus a clear statement
  that the work was agent-assisted.
- CI: `.github/workflows/main.yml` runs the test matrix on
  ubuntu/windows/macos with Python 3.10 and 3.14 (plus windows 3.12,
  ubuntu pypy-3.11, and other includes), and the repo also relies on
  `pre-commit.ci - pr` and `docs/readthedocs.org` statuses. On a
  first-time fork PR the Actions workflows land in `action_required`
  until a maintainer approves the run (verified on PR #1155).
- Windows launch path: `launcher.launch_kernel` creates a Win32
  interrupt event (`JPY_INTERRUPT_EVENT`) and an inheritable duplicate
  of the parent process handle (`JPY_PARENT_PID`). The event is stored
  as `proc.win32_interrupt_event` and set by
  `LocalProvisioner.send_signal`; the child uses only its inherited
  copies, so both handles are the launcher process's to close.
- Layout: `jupyter_client/` package, tests in `tests/`, Sphinx docs in
  `docs/`, hatch environments in `pyproject.toml`.

## Development / validation commands

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]" psutil
$env:PYTEST_ADDOPTS = '-W default'   # Python 3.14 deprecates WindowsSelectorEventLoopPolicy
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check jupyter_client tests
.\.venv\Scripts\ruff.exe format --check jupyter_client tests
.\.venv\Scripts\mypy.exe jupyter_client
```

- Pin lint tools to `.pre-commit-config.yaml` (at the time: ruff
  0.15.12, mypy 1.20.2); newer ruff releases add rules that flag
  untouched code.
- Pre-existing Windows failure:
  `tests/test_kernelmanager.py::TestParallel` signalkernel tests time
  out identically on unmodified upstream. Deselect that class to get a
  clean local signal.
- `mypy jupyter_client` reports ~23 pre-existing errors on a Windows
  host (the `_winapi` / `_subprocess` import branches). Diff the
  changed-file output against a stashed baseline instead of expecting
  zero.
