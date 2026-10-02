# odysseus-dev/odysseus — #2740

## Status

In progress — implementation

## Issue

https://github.com/odysseus-dev/odysseus/issues/2740
"Resolve SQLAlchemy 2.0 deprecation warnings in core/database.py"
Labels: `bug`, `ready for review`, `p3`

Claimed: https://github.com/odysseus-dev/odysseus/issues/2740#issuecomment-5959844524

## Pull Request

[#6453 — fix(core): import declarative_base and declared_attr from sqlalchemy.orm](https://github.com/odysseus-dev/odysseus/pull/6453)

- Base branch: `dev` (correct target)
- Opened: 2026-10-02
- State: open, mergeable
- Fork head: `ShahabAhmed01:fix/sqlalchemy-declarative-import-2740`

## Branch

`fix/sqlalchemy-declarative-import-2740` (from `upstream/dev` @ `2992bf6d368a`)

## Commits

- `45d372b2481ae4f46b0134572304a9075c70cc0f` — fix(core): import declarative_base and declared_attr from sqlalchemy.orm (22 files, +22/−23)

## Problem

`core/database.py` imports `declarative_base` and `declared_attr` from
`sqlalchemy.ext.declarative`, the SQLAlchemy 1.x location that emits
`MovedIn20Warning` under SQLAlchemy 2.x. The warning is emitted on every test
run and on app import.

## Root Cause

The import predates SQLAlchemy 2.0. SQLAlchemy 2.x moved the canonical
`declarative_base` / `declared_attr` into `sqlalchemy.orm` and deprecated the
`sqlalchemy.ext.declarative` re-export.

## Solution

- Import `declarative_base` and `declared_attr` from `sqlalchemy.orm`.
- Remove the now-stale `"sqlalchemy.ext.declarative"` entries from the test stub
  lists (`tests/conftest.py` and the per-test stubs), without substitution.

Based on maintainer review of closed PR #2734, which invited a fresh small PR
with attribution (#3241 was closed as its duplicate).

## Files Changed

- `core/database.py` — import `declarative_base`, `declared_attr` from `sqlalchemy.orm`
- 21 test files — deleted the stale `"sqlalchemy.ext.declarative"` module-stub entry
  (`tests/conftest.py`, `test_agent_loop.py`, `test_compact_truncate_tool_call_args.py`,
  `test_compaction_summary_failure.py`, `test_context_compactor.py`,
  `test_fenced_inline_args.py`, `test_fenced_invoke_no_raw_xml.py`,
  `test_function_call_non_object_args.py`, `test_llm_core_reasoning_content_fallback.py`,
  `test_llm_core_sanitize_tool_calls.py`, `test_loop_breaker_runaway.py`,
  `test_prompt_injection_audit.py`, `test_sanitize_preserves_reasoning.py`,
  `test_skill_index_prompt_injection.py`, `test_skill_index_toolset_gating.py`,
  `test_skills_manager_owner_isolation.py`, `test_skills_tag_token_match.py`,
  `test_tool_output_prompt_injection.py`, `test_unknown_tool_calls.py`,
  `test_web_search_raw_json_tool_call.py`, `test_web_search_time_filter.py`)

## Tests

- **Reproduction (before):** `python -W always::DeprecationWarning -c "import core.database"`
  → `MovedIn20Warning: The declarative_base() function is now available as
  sqlalchemy.orm.declarative_base()`
- **After:** same command prints nothing.
- **Focused:** 20 touched test files — `178 passed in 1.76s`
- **Full suite:** `python -m pytest -q` → `5952 passed, 4 skipped, 4 warnings in 219.32s`
  (zero `MovedIn20Warning` lines)
- **Syntax:** `python -m compileall -q app.py core routes src services scripts tests` → clean

## Runtime Validation

- Environment: Python 3.11.17 (uv venv), SQLAlchemy 2.1.2
- App: `venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 7000`
- `GET /api/health` → HTTP 200 `{"status":"healthy",...}`
- `GET /api/version` → HTTP 200 `{"version":"1.0.3"}`
- `init_db()` created the SQLite tables via the new import (verified in `data/app.db`)
- Zero `MovedIn20Warning` lines in the startup log
- Unrelated degraded notices (ChromaDB unreachable, no python-magic) — environment
  services not running, not caused by this change.

## CI

_Not started._

## Review

_Not opened._

## Merge

_Not merged._

## Lessons Learned

- The maintainer treats stale test stub entries as duplicates rather than
  harmless leftovers; delete rather than substitute.
- Always search closed PRs as well as open ones before picking an issue.
