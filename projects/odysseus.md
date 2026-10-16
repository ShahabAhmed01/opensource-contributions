# Project notes — odysseus-dev/odysseus

Last verified: 2026-10-09

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
- Throwaway runs: `ODYSSEUS_DATA_DIR=/tmp/<dir>` isolates every persisted file
  (auth.json, sqlite dbs, uploads); first run needs `POST /api/auth/setup`
  `{username, password}` then `/api/auth/login` (cookie `odysseus_session`).
  Session tokens persist on disk, so a restart keeps the login.
- Outbound mail to loopback/LAN is blocked by `_mail_private_blocked` unless
  the run sets `EMAIL_ALLOW_PRIVATE_IPS=true` (admins are trusted, but the
  env var is what allows it) — otherwise sends die with
  "private/shared/loopback address blocked".
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

- The test suite is large; CI runs all of it. Run locally before pushing. The
  suite carries ~70 environmental failures (Playwright binaries, bubblewrap-
  hidden venvs, model downloads) that are identical on unmodified dev: compare
  focused tests before/after and state the real baseline; never claim a fully
  green suite.
- JS-syntax checks in tests must avoid `!~` (`not (string in container)`):
  Python reads it as `(!string) ~ container`, so a file can be valid JS and
  fail pytest's parse step anyway (hit in tests/test_compose_send_account_resolution_js.py
  during #1912). Write `not (... in ...)` explicitly.
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

### #1912 — deleted active compose account (PR #6648 open, 2026-10-09)

- Branch: `fix/compose-send-stale-account-1912`; PR:
  https://github.com/odysseus-dev/odysseus/pull/6648 (base `dev`).
- Fix lives entirely in `_resolveComposeSendAccountId` (`static/js/document.js`);
  tests in `tests/test_compose_send_account_resolution_js.py` reuse
  `tests/helpers/document_source.function_body` and run the real function source
  under `node --input-type=module`.
- Validation: full suite 13762 passed / 70 failed / 67 skipped (the 70 are the
  environmental set); end-to-end app run with local SMTP (2525) + IMAP (2143)
  sinks so compose can save a recovery draft and deliver.
- UI evidence: the PR-description gate needs a screenshot for any `static/`
  path. There is no upload API, so screenshots live on an orphan fork branch
  (`evidence/issue-1912`) and are linked through `raw.githubusercontent.com` —
  accepted by the gate and durable.
- Headless UI driving: no playwright/chromium here; `selenium` 4.x with
  Selenium Manager (auto-downloads geckodriver) + system Firefox `-headless`
  works. Deep links `#document-<id>` open a document directly; a compose doc is
  `POST /api/document {title:"New Email", content:"To: \nSubject: \n---\n",
  language:"email"}`.

## Mergeability audit addendum 2026-10-17 (Tracks 001–007, all open)

- All seven open odysseus PRs re-verified by API: every fork branch tip
  byte-matches the live PR head; every linked issue still open; no record
  has an unanswered human review or comment.
- **#6475 (Track 004) and #6476 (Track 005)**: the long-recorded
  `ci-failed` was a tracker artifact — our sync resolved duplicate check
  names to the OLDEST run while GitHub lists check-runs newest-first, and
  the repo's own description check had re-run green on 2026-10-03
  (post-label event) and again after the 2026-10-09 description updates.
  The checker's current rules were re-derived from
  `.github/scripts/check-pr-description.js` `dev` and simulated locally;
  both bodies pass every rule (Summary ≥20, `#NNN`-linked Linked Issue,
  checked Type-of-Change box, checked duplicate-search box, How-to-Test
  ≥30, and the runtime attestation box for `src/` classification). A
  factual "Re-verification (2026-10-17)" body section was appended; the
  `edited` event re-ran the check: success 2026-10-16T21:17:36Z
  (#6475) / 21:17:40Z (#6476), `ready for review` labels present.
- **#6473 (Track 003)**: the one genuine failure left in the fleet is
  gitleaks, on upstream content — the workflow scans the full merge-ref
  history (`gitleaks git .`) and flags 4 findings inside upstream commit
  `dab660543b5b` ("chore(publication): close pre-integration release
  blockers", `alteixeira20`, 2026-10-05). Our PR has a single commit
  (`35e3b298d8f8`); no branch operation on our side can remove an upstream
  history object, and a scope-limited bugfix PR must not grow a
  `.gitleaks.toml` allowlist change. Every our-side check passes.
- **Tracker tooling**: `scripts/update_tracker.py` now resolves each
  check name to its newest run (highest check-run id; the `gh` shim emits
  ids). Without this, re-runs made a passing check read as `fail`
  indefinitely.
- The repo's external-contributor approval gate (`mergeable_state`
  unstable with no failing run; PR-level workflows run via
  `pull_request_target` regardless) still holds for first human review.
