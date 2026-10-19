# Project notes — Kludex/starlette

Last verified: 2026-10-19

## Facts

- ASGI framework (routing, middleware, requests/responses, websockets,
  test client). BSD-3-Clause. Python `>=3.11`.
- 12,674 stars / 1,381 forks (live 2026-10-19); `main` is the only branch
  PRs target, last pushed 2026-10-18 (`dc20b21` was the tip when this
  contribution was cut).
- Release cadence: `1.9.0` shipped 2026-10-18; `docs/release-notes.md`
  collects per-release bullet lists **with PR links, edited by
  maintainers at release time** (its process lives under "Releasing" in
  `docs/contributing.md`, "targeted at Starlette maintainers" — merged
  fixes #3585/#3640 did not touch it). Do not edit the changelog in a
  normal PR.
- `AI_POLICY.md` **permits AI contributions** with one hard rule: before
  opening a PR, search open *and closed* PRs, issues **and discussions**;
  a duplicate PR gets the contributor banned from the project.
- PR template: Summary heading, then three checkboxes — prior discussion
  (does not apply to typos), a test per change / single atomic change,
  documentation updated. The maintainer closes PRs that lack prior
  discussion (batch closes on 2026-10-04/06/09/11/13/17/18; #3577 was
  answered "Do you need this? Are you a human that needs this?").
- Bug reports often arrive as **discussions** in the *Potential Issue*
  category (e.g. #2738, #3634, #3668–#3681), then get fixed by PR — the
  issue queue stays tiny (six open issues on 2026-10-19), so issue-driven
  targeting does not work here; discussions are the live signal.
- Acceptance record measured 2026-10-19: owner merged external PRs #3542
  (host case-insensitivity), #3585 (`HEAD` in `HTTPEndpoint` Allow),
  #3622 (memoryview byte length), #3631 (GZip start), #3654/#3674
  (docs), and shipped his own #3675/#3679 on 13–18 October. The merged
  shape is crisp HTTP-spec correctness with regression tests.
- Open PR queue is long-lived (33 open on 2026-10-19, some from 2024)
  and two in-flight PRs touch `Router.app`'s match loop: #3665 (two-line
  `==`→`is`) and owner PR #3339 (segment-trie rewrite, keeps
  first-partial dispatch) — expect rebase requests if they land first.
- House vocabulary: `Match.FULL` / `Match.PARTIAL` (path matched, method
  did not — this is what produces a 405), `scope["route"]`, the `Allow`
  header, routes registered on one path (sibling routes).

## Development / validation commands

```bash
uv sync --frozen                    # exact lockfile environment (done in-session)
uv run coverage run -m pytest -q    # tests as CI runs them (coverage on)
scripts/coverage                    # gate: branch coverage fail-under=100
scripts/check                       # sync-version + ruff format --check + mypy --strict + ruff check
scripts/lint                        # ruff format + ruff check --fix
scripts/test                        # check + coverage run + coverage gate (local wrapper)
uv run zensical build --clean       # docs CI command — scripts/docs is a dev server, not a build
```

- Coverage is configured with `branch = true` and
  `source_pkgs = ["starlette", "tests"]` — **test files count**, so an
  unexercised branch in a new test fails the gate too.
- Baseline at `dc20b21`: 1394 passed, 2 skipped, 2 xfailed (the skips
  are `<3.14`-only response tests).
- `mypy` runs `--strict` over `starlette tests benchmarks`; beware the
  shared-variable trap (a new `PlainTextResponse` local later assigned a
  `RedirectResponse` fails mypy).

## Contribution history

- Track 020 (2026-10-19): PR #3682 — `Allow` header of a `405` now lists
  every route matching the path (RFC 9110 §10.2.1), anchored on discussion
  #2738 ("Seems valid." — @Kludex, 2024-10-25, never fixed). First
  starlette contribution; see `contributions/starlette/discussion-2738.md`.
