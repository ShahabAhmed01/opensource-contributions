# Project notes — odysseus-dev/odysseus

Last verified: 2026-10-02

## Facts

- Self-hosted AI workspace. Python 3.11+ / FastAPI monolith. Frontend is plain JS
  under `static/` (no bundler). SQLite by default via SQLAlchemy; optional Postgres.
- License: AGPL-3.0-or-later. Very active: ~88k stars, ~1,300 open issues.
- **Default and development branch is `dev`; PRs target `dev`.** `main` is curated
  at release time. Do not open PRs against `main`.
- LLM-agent policy (CONTRIBUTING.md): open/use an issue describing the problem
  first instead of opening a PR directly. Bulk unscoped agent PRs are closed.
- One focused change per PR; no formatting-only or drive-by churn.
- Conventional Commits: `type(scope): summary`.
- Do not hardcode filesystem paths (`src/constants.py` has named constants,
  e.g. `DATA_DIR`, `AUTH_FILE`). Do not hardcode `http://localhost:7000`;
  use `internal_api_base()` from `src.constants`.
- No Unicode emoji in UI or code. UI changes need real screenshots and must match
  the existing visual language.

## Repository layout (high level)

- `app.py` — FastAPI application entrypoint (also run via `uvicorn app:app`)
- `routes/` — HTTP route modules, domain subpackages for larger areas
- `services/` — service layer (memory, search, research, docs, tts, ...)
- `src/` — core helpers/models; `src/constants.py` is the single source of truth
- `core/` — database, auth, middleware, models; `core/constants.py` re-exports
- `static/` — frontend JS/HTML/CSS; `static/app.js` orchestrates modules
- `tests/` — ~816 test files, pytest with `asyncio_mode = "auto"` and an
  `area_*` / `sub_*` taxonomy added by `tests/conftest.py`
- `docker/`, `docker-compose*.yml`, `Dockerfile` — Docker path (recommended in docs)
- `mcp_servers/`, `integrations/`, `website/`, `companion/`, `swift/`

## Development / validation commands

- Native: `python3 -m venv venv && pip install -r requirements.txt`
  then `python -m uvicorn app:app --host 127.0.0.1 --port 7000`
- Tests: `python -m pytest -q` (CI installs requirements, `mkdir -p data` first)
- Syntax: `python -m compileall -q app.py core routes src services scripts tests`
- JS syntax: `node --check static/app.js static/js/**/*.js`
- Docker: `docker compose config && docker compose up -d --build`
  (`docker compose logs --tail=120 odysseus`)

## Automated gates that judge issues and PRs

- `.github/workflows/pr-description-check.yml` + `.github/scripts/check-pr-description.js`:
  requires `## Summary` >= 20 chars, a `## Linked Issue` with `#NNN`,
  at least one checked `## Type of Change` box, the `- [x] I searched` checklist
  item, and `## How to Test` >= 30 chars. Backend/runtime/UI paths additionally
  need truthful runtime attestation (`- [x] I actually ran the app...`), and
  UI-sensitive paths need a checked screenshot box + real attachment. PR title
  must match Conventional Commits.
- `.github/workflows/issue-description-check.yml` + `.github/scripts/check-issue-description.js`:
  `bug`-labeled issues must have `## Odysseus Revision` as `12-hex-sha (YYYY-MM-DD)`,
  `## Install Method`, `## Operating System`, `## Steps to Reproduce`,
  `## Expected Behaviour`, `## Actual Behaviour`, and no `-- Please Select --`
  placeholders. `enhancement` issues have their own required sections.
- CI (`ci.yml`): compileall, node --check, full pytest. PR description check runs
  on `pull_request_target` and labels PRs (`ready for review`, `needs work`, ...).

## Pitfalls learned

- The test suite is large; CI runs all of it. Run locally before pushing.
- Do not blindly reformat; diffs must stay minimal.
- Many issues are already claimed by open PRs — always search PRs before picking
  an issue. Two closed PRs exist for the current issue (#2740): #2734 and #3241.
- `tests/conftest.py` and many individual test files pre-stub SQLAlchemy modules
  in `sys.modules` for environments where it is not installed. After the
  SQLAlchemy import migration, the `sqlalchemy.ext.declarative` stub entries are
  stale and must be deleted (not replaced with `sqlalchemy.orm`, which is already
  listed — substitution creates duplicates).

## Contribution history

### #2740 — SQLAlchemy deprecation warning (PR #6453 open, 2026-10-02)

- Maintainer vdmkenny on #2734: core change "exactly right"; redo as fresh small
  PR allowed with attribution; delete stale stub entries.
- Branch: `fix/sqlalchemy-declarative-import-2740`; PR:
  https://github.com/odysseus-dev/odysseus/pull/6453 (base `dev`).
- Validation: full suite 5952 passed / 4 skipped; app run healthy; zero
  `MovedIn20Warning` lines.
