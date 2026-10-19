# Project notes — Kludex/uvicorn

Last verified: 2026-10-19

## Facts

- The de-facto ASGI server: HTTP/1.1 (`h11`, `httptools`, `zttp`), optional
  HTTP/2 through `zttp`, WebSockets (`wsproto` / `websockets`), a CLI,
  `--reload`, `--workers` and a gunicorn worker. BSD-3-Clause.
  Python `>=3.11`.
- 11,017 stars / 1,064 forks / 95 watchers (live 2026-10-19); `main` is the
  only branch PRs target, last pushed 2026-10-19T09:48Z (`cc6fea5` was the
  tip when this contribution was cut). Last pushes on the day of the
  contribution: `#3214` merged 2026-10-19.
- Release cadence: `0.54.0` (2026-09-24), `0.53.0` (2026-09-14), `0.52.4`
  (2026-08-18). `docs/release-notes.md` is a symlink target of `CHANGELOG.md`
  and is written **by the maintainer at release time** — the "Releasing"
  section of `docs/contributing.md` says so explicitly. Do not touch it in a
  normal PR.
- `AI_POLICY.md` is short and strict: AI tools are permitted, you remain
  responsible, and before opening a PR you **must** search the open *and
  closed* pull requests, issues **and discussions**. "Contributors who submit
  duplicate pull requests will be banned from the project."
- `docs/contributing.md` requires contributions to start from a discussion.
  Bug reports go up as *Potential Issue* discussions, feature requests as
  *Ideas*; maintainers then decide whether to escalate to an issue or accept
  a PR. Discussions are therefore the live signal, not the issue queue.
- PR template (`# Summary` + `# Checklist`, three boxes): prior discussion
  (does not apply to typos), a test for each change / a single atomic
  change, documentation updated.
- Acceptance record measured 2026-10-19: external merges `#3209` (README
  logo, 2026-10-18), `#3195` (`raw_path` in access logs), `#3092` (negative
  `--limit-max-requests-jitter`) and `#3184` (reload startup speed), all
  2026-10-11, plus earlier `#3103`/`#3107`/`#3119`; the owner shipped
  `#3194`/`#3196`/`#3197`/`#3198`/`#3199`/`#3200` (2026-10-10/11) and
  `#3214` (2026-10-19). 91 PRs were open on 2026-10-19 and most fresh issues
  and discussions are claimed within hours, so issue-first targeting is a
  swarm here.
- Duplicate enforcement is harsh: roughly fifteen duplicate `IPPROTO_TCP`
  PRs were batch-closed on 2026-10-11 and the owner fixed `#3149` himself in
  `#3199`. Always re-run the corpus + discussion sweep before writing code.
- House vocabulary: `H11Protocol` / `HttpToolsProtocol` / `ZttpProtocol`,
  `RequestResponseCycle`, `Server.shutdown()`'s
  `for connection in list(self.server_state.connections)` loop,
  `server_state.connections`, and h11's `our_state` / `their_state` with the
  `ERROR` sentinel. `connection_lost()` and `shutdown()` are the two places
  that send `h11.ConnectionClosed()`.
- Automation on every PR: `copilot-pull-request-reviewer[bot]` (frequently
  quota-limited, posts no content), `cubic-dev-ai[bot]` (per-commit review,
  P-labelled findings in a "Prompt for AI agents" block, expects a threaded
  reply), `codspeed[bot]` ("Merging this PR will not alter performance"),
  and `CodeRabbit`, which reports as a **commit status**, not a check-run —
  while it reviews, `mergeable_state` reads `unstable` even with every
  check-run green.

## Development / validation commands

```bash
uv sync                        # dev + docs groups are the default
./scripts/test                 # scripts/check + coverage run -m pytest + coverage gate
./scripts/lint                 # ruff format + ruff check --fix
./scripts/check                # sync-version + ruff format --check + mypy + ruff check
./scripts/coverage             # coverage combine + report (the 100% gate)
uv run zensical build --clean  # docs build (CI runs `uv run zensical build`)
```

- Coverage is **line** coverage with `fail_under = 100` and
  `source_pkgs = ["uvicorn", "tests"]` — **test files count**. An unreachable
  `except: pass` added to the fix *or* to a new test breaks the gate; verify
  that every new line is actually executed.
- `pyproject.toml` sets `filterwarnings = ["error"]`. A real-socket test that
  leaves an `asyncio.StreamWriter` unclosed fails with
  `PytestUnraisableExceptionWarning` — close the writers and `await
  writer.wait_closed()`.
- pytest runs with `-n 8` (xdist) and `faulthandler_timeout = 60`.
- `docs-preview` runs only when the head branch lives in the same repo
  (`github.event.pull_request.head.repo.full_name == github.repository`), so
  fork PRs never get a docs build in CI — build docs locally if you touch
  `docs/`.
- `mypy` runs over `uvicorn tests` without `--strict`; test functions with no
  annotations at all are not type-checked, so an `# type: ignore` inside one
  is reported as unused (`warn_unused_ignores = true`). Annotate the test
  (`-> None` or a typed parameter) if you need those ignores.

## Contribution history

- Track 021 (2026-10-19): PR #3215 — `H11Protocol.shutdown()` skips the
  `h11.ConnectionClosed()` handshake for a connection whose local h11 state
  already failed and closes its transport anyway, so one connection in
  `ERROR` no longer raises `LocalProtocolError` out of `Server.shutdown()`'s
  loop and strands the rest. Anchored on discussion #3108 ("Potential Issue",
  2026-08-29, `kazuki-ma`, never fixed, never PR'd). First uvicorn
  contribution; see `contributions/uvicorn/discussion-3108.md`.
