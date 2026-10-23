# Project notes — python/mypy

Last verified: 2026-10-23

## Facts

- The static type checker for Python. Base commit when this contribution
  was cut: `8fdf437` (`Fix false positive on generic NamedTuple
  `__new__` (#22258)`), local version string `2.5.0+dev.8fdf437`
  (`compiled: no` in a source venv).
- Native parser (Rust based, `ast-serialize` byte serialization) **is the
  default since 2.4** (`mypy/options.py: self.native_parser = True`;
  2.3.1 still defaulted to `False`). The native path is also
  multi-threaded (`BuildManager.parse_all` with a thread pool when
  `can_start_threads()`).
- `ast-serialize` is a separate repo `mypyc/ast_serialize` released on
  PyPI (pin `>=0.13.1,<1.0.0` in `mypy-requirements.txt`; 0.13.1 is the
  latest as of 2026-10-17). Its `parse()` has no way to collect imports
  from skipped function bodies, and it **self-strips function bodies
  when a module file carries an inline `# mypy: ignore-errors=True`
  comment** — mypy's own `test_nativeparse.py` mirrors that semantics
  (`skip_function_bodies = "# mypy: ignore-errors=True" in source`), so
  treat inline-comment stripping as intended; config-file driven
  `ignore_errors` is where mypy must keep imports reachable.
- Legacy parser parity nuance: `fastparse.py` visits statements of a
  method body before discarding the body (slow-strip path), so method
  level lazy imports are recorded in `tree.imports` there; the fast
  strip path (plain top-level function bodies) does drop them. A
  restored set including top-level-function imports is a deliberate, safe
  superset of the pre-regression behavior.
- Result record for a Config-file repro (verified both ways in-run):
  2.3.1 reports `pkg/b.py:1: error: Incompatible types in assignment
  (expression has type "str", variable has type "int")  [assignment]`
  while 2.4.0+/master reported "Success: no issues found" — issue #22280.
- maintainer house context around #22280: @ilevkivskyi (commented
  2026-10-22, asked whether the direction needs a design debate before a
  fix), reporter @jorenham (numba; confirmed the immediate concrete
  impact is stubtest on numba), @hauntsaninja and @A5rocks added labels.
  No explicit AI-code policy in CONTRIBUTING.md; disclosure of assistance
  is good practice here and was included in the PR body.
- PR template is minimal (no checklist gates beyond the block comment);
  CI is heavyweight: 23+ checks — test matrix py310–py315 (ubuntu, some
  mypyc-compiled, t-branch, windows), mypyc runtime (macos/ubuntu), 32-bit
  suite, parallel tests, **mypy_primer (6 matrix shards)** on downstream
  projects (slowest, can take over an hour), plus three fast checks
  (type-check own code x2, Black + ruff). Non-draft PRs run all of it;
  nothing is exclusive to maintainers.

## Development / validation commands

```bash
python3 -m venv venv && . venv/bin/activate
pip install -r dev-requirements.txt   # pulls librt + ast-serialize
pip install -e .
python -m pytest mypy/test/testcheck.py::TypeCheckSuite::check-inline-config.test::testIgnoreErrorsMethodImportFollowed -q
python -m pytest mypy/test/testcheck.py -q                      # bigger suites
python -m mypy --config-file mypy_self_check.ini -p mypy        # self-check (CI gate)
```

- Data-driven checker tests live in `test-data/unit/*.test`; a case is
  `[case Name]` plus `[file pkg/a.py]` sections (packages supported).
  Per-case flags go on a `# flags: ...` line; the harness sets
  `hide_error_codes = True` unless the flags include
  `--show-error-codes`, and paths in expected output get a `tmp/`
  prefix when a case uses `--config-file tmp/mypy.ini` (see
  `testInlineErrorCodesOverrideConfigSmall*` for the pattern).
- RED/GREEN pair for Track 021 verified 2026-10-23: expected
  `tmp/pkg/b.py:1: error: ...` line passes with the fix, fails with
  empty Actual without it.

## Contribution history

- Track 021 (2026-10-23): PR #22285 — `Follow modules imported inside
  skipped function bodies in the native parser`, fixing #22280 (2.4
  regression; modules imported inside method bodies of an
  `ignore_errors` module stopped being followed when the native parser
  became the default). First mypy contribution.
