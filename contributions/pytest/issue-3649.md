# pytest-dev/pytest — issue #3649

## Status

**PR #15239 OPENED, CI RUNNING, AWAITING FIRST HUMAN REVIEW** — opened
2026-10-21T20:53:14Z, ready for review (not draft), base `main` @
`c9bf1ed` (the upstream tip, re-verified at publication). Head
`28d81d9` (two commits, +28/−1 across four files). `Changelog entry`
and `package` are green, the `build` matrix is still running, and
`pre-commit.ci - pr` and `docs/readthedocs.org:pytest` are the two
commit statuses. `mergeable: true`, `mergeable_state: blocked`
(pytest's fork-PR protection gate), as of 2026-10-21T21:05Z. One bot
review so far (`copilot-pull-request-reviewer` COMMENTED, no content).
Per policy, no pings. Not merged.

## Issue

https://github.com/pytest-dev/pytest/issues/3649
"pytest syntax_error.py --pdb should not drop into pdb?"

OPEN, unassigned, 6 comments, labeled `type: bug`, `topic: collection`,
`plugin: debugging`, created 2018-07-02T15:46:47Z, last updated
2021-10-14T22:21:25Z.

The reporter's own transcript is the acceptance contract: with
`pytest t.py --pdb` on a file containing `syntax error`, pytest prints the
traceback and then drops into pdb on
`_pytest/python.py::_importtestmodule()` — the `raise self.CollectError(...)`
line — so the debugger shows where the error is *re-raised* rather than
the syntax error itself. The issue asks whether that is desirable.

The discussion pins the intended behaviour. `Zac-HD` (2018-10-19) noted
the detailed traceback is desirable but that skipping the debugger for
syntax errors "would have to write a lot of new code"; `asottile`
replied in the same thread: "no no, this is definitely worth fixing";
`Tadaboody` (2019-01-08) added "in general, debugger should not be
launched in the collection phase". The issue has been open since 2018
with no linked and no competing pull request at publication.

## Pull Request

[#15239 — fix: don't enter the debugger for a syntax error](https://github.com/pytest-dev/pytest/pull/15239)

- Base branch: `main` @ `c9bf1edf9e0d388f3e7bebc88576e608ffbc40a4`
  (verified the upstream tip at publication and again after the second
  push)
- Opened: 2026-10-21T20:53:14Z · State: open, mergeable, not draft ·
  `mergeable_state: blocked` (fork-PR protection gate)
- Fork head: `ShahabAhmed01:fix/3649-pdb-syntax-error` @ `28d81d9`
  (verified by `ls-remote`/API after the push; unchanged since)
- `Closes #3649` is in the body's summary section
- Size: 4 files, +28/−1
- Body: summary, changelog note, the filled pull-request checklist, the
  testing plan, and an **AI assistance disclosure** section, per
  `CONTRIBUTING.rst`'s "AI/LLM-Assisted Contributions Policy". The body
  was revised once post-publication (a body edit only, the head did not
  move): it now records that this account is not allowed to comment on
  other users' issues in the repository, so the root-cause analysis
  lives in the PR description instead of an issue comment.

## Branch

`fix/3649-pdb-syntax-error`, cut from `upstream/main` @ `c9bf1ed` in an
isolated sparse clone in the run workspace
(`~/opensource-work/runs/ossrun-20261020T143705Z-bd8fbd7f/projects/pytest`).
The user's master checkout was untouched. A shallow checkout cannot
date-setuptools-scm, so local runs need
`SETUPTOOLS_SCM_PRETEND_VERSION=9.0.0`.

## Commits

- `8d93f324680092dccfc92d52614bafb43a4b071b` — fix: don't enter the
  debugger for a syntax error
- `28d81d949d91da5e40e9160eb7e482307bd1f237` — fix: drop the
  unreachable branch from `is_syntax_error`

## Problem

Reproduced on `c9bf1ed` before writing any code: `pytest --pdb` on a
file whose only line is `syntax error` prints the traceback and then
enters pdb, with the prompt sitting on
`src/_pytest/python.py:528 in importtestmodule` — the `raise` statement.

## Root Cause

`src/_pytest/python.py::importtestmodule` re-raises a `SyntaxError` as a
`CollectError` carrying the formatted traceback:

```python
    except SyntaxError as e:
        raise nodes.Collector.CollectError(
            ExceptionInfo.from_current().getrepr(style="short")
        ) from e
```

`CollectError` is not a control-flow exception, so
`src/_pytest/runner.py::collect_one_node` classifies it as an
interactive exception (`check_interactive_exception` only excludes
`Skipped`, `BdbQuit` and `unittest.SkipTest`) and calls
`pytest_exception_interact` — which enters pdb on the frame of the
`raise`, not on the syntax error.

## Solution

- The `CollectError` keeps the original `SyntaxError` as its
  `__cause__`, so `runner.py` can recognise exactly this case: a new
  `is_syntax_error(exc)` helper checks the exception and its cause.
- `collect_one_node` skips `pytest_exception_interact` for a syntax
  error. The error is still reported exactly as before, with its full
  traceback; only the debugger is not entered.
- Nothing else changes: every other collection error still opens the
  debugger, so `test_pdb_interaction_on_collection_issue181` (a
  `NameError` at import) and `test_pdb_collection_failure_is_shown`
  still pass unchanged, and a `SyntaxError` raised *inside* a test
  still opens the debugger (that path is the runtest phase, not
  collection).

## Files Changed

- `src/_pytest/runner.py` — the `is_syntax_error` helper and the guard
  in `collect_one_node` (+18/−1)
- `testing/test_debugging.py` — one new regression test (+11/−0)
- `changelog/3649.bugfix.rst` — changelog entry (+1/−0), named for the
  issue and typed `bugfix` (the changelog-naming hook requires
  `####.<type>` on `changelog/`)
- `AUTHORS` — one line for `Shahab Ahmed` (+1/−0)

## Tests

One new test in `testing/test_debugging.py`:

- `TestPDB::test_pdb_not_entered_on_syntax_error` — a file containing
  `syntax error` run with `--pdb` reports `E   SyntaxError: invalid
  syntax` and never prints `entering PDB`.

Local runs (Python 3.12.15, Linux, the run workspace venv at
`9.0.0`):

```
testing/                     4698 passed, 47 skipped, 13 xfailed, 7 xpassed
testing/test_debugging.py      54 passed, 1 skipped, 6 xpassed
ruff check      src/_pytest/runner.py testing/test_debugging.py   -> All checks passed
ruff format     src/_pytest/runner.py testing/test_debugging.py   -> 2 files already formatted
mypy            src/_pytest/runner.py                            -> Success: no issues found in 1 source file
```

- The new test fails without the change (the debugger is entered and the
  run reports `Enter: Quitting debugger`).
- The full `testing/` run is green before and after the change. The one
  error in a first run was `testing/test_legacypath.py::test_cache_makedir`,
  which comes from invoking pytest with `-p no:cacheprovider` (that
  plugin provides the `cache` fixture) and passes without the flag.
- **Coverage:** a local `coverage run -m pytest` with the repository's
  own configuration (`patch = ["subprocess"]`, `branch = true`) shows
  every added line executed — the subprocess coverage is what covers
  the new helper, since the syntax-error path only runs in the child
  process. This is what `codecov/patch`'s 100% patch target needs.
- ruff 0.17.1 and mypy 2.4.0 are the versions the pre-commit pins.

## CI (live at 2026-10-21T21:05Z)

- `Changelog entry` success, `package` success, the `build` matrix in
  progress, `pre-commit.ci - pr` success, `docs/readthedocs.org:pytest`
  pending.
- `codecov/patch` on the opening commit concluded **failure** at
  "57.14% of diff hit (target 100.00%)" two minutes after the PR was
  opened, i.e. before the build matrix had uploaded any coverage — the
  same mid-rollup artifact seen on Track 022. The local coverage run
  also found one genuinely uncovered line (the helper's unreachable
  "did not raise" branch), which was removed in the second commit
  before anything else landed.
- `mergeable: true`, `mergeable_state: blocked` — pytest requires the
  protection gate to clear for merging, not for review.

## Review

No human review yet. `copilot-pull-request-reviewer[bot]` COMMENTED and
posted no review content. pytest-core reviews and merges external fixes
routinely; no pings were sent — the PR is the reply.

## Merge

Not merged. Open, mergeable, `blocked` protection gate, awaiting first
human review as of 2026-10-21T21:05Z.

## Lessons Learned

- A `CollectError` that chains its cause is enough to tell "the user
  made a syntax error" from "the collection failed" without touching
  the exception type: `exc.__cause__` carries the original
  `SyntaxError`, so no new plumbing was needed.
- pytest's `codecov.yml` sets a **100% patch target**, so a helper
  whose guard branch cannot be reached fails CI even when the code is
  correct. The local `coverage run -m pytest` with the repo's own
  config — including `patch = ["subprocess"]`, without which the
  subprocess coverage that exercises the new path is invisible — is
  the cheap way to find that before CI does.
- A shallow clone cannot date-setuptools-scm: `SETUPTOOLS_SCM_PRETEND_VERSION`
  is needed for local runs, and pytest's `pyproject.toml` `minversion`
  check rejects the resulting `0.1.dev1` version outright.
- The account is blocked from commenting on other users' issues in
  pytest-dev/pytest (the API answers "User is blocked"), though it can
  comment on its own pull requests. The root-cause analysis therefore
  went into the PR description, and the PR body was revised to say so.
