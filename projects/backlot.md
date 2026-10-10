# Project notes — brekkylab/backlot

Last verified: 2026-10-10

## Facts

- Serves 11 real SaaS APIs — Slack, Gmail, Google Drive, GitHub, Jira,
  Confluence, Notion, S3, HubSpot, Linear, Fireflies — with the smallest
  possible gap from the real thing, so clients built against the real
  APIs work unchanged. The corpus is supplied by the user (a bundled
  `hello.jsonl` covers every source).
- Python 3.11+ / FastAPI / SQLite. MIT license. ~424 stars. Created
  2026-07-02; very active (commits merged to `main` daily).
- Default and only development branch: `main`. PRs target `main`.
- Python-style: line length 100, ruff with isort (`I`), `E402` ignored.
- House vocabulary: **source** = one of the APIs Backlot serves
  (`source_type` on every record); **vendor** = the real company whose
  API a source imitates. Never interchangeable.
- A maintainer-run agent routine also opens PRs here, for issues a
  maintainer labels `agent` (see `docs/loop.md`). Human contributors
  work the unlabeled issues; nothing about the flow differs.

## Development / validation commands

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"        # pip's resolver cannot solve this graph; uv's can
backlot import backlot/data/hello.jsonl   # bundled corpus -> data/db.sqlite
backlot serve                              # http://127.0.0.1:8000
pytest                                     # no data, no network needed
pytest -rs                                 # names every skip and its reason
ruff check . && ruff format --check .      # both gate CI
python scripts/prose_check.py              # comment rules; warnings on CI, fails locally
uv sync --all-extras --locked              # what CI installs (all extras)
```

- Tests that drive things outside the package self-skip when the extra
  is absent: `.[official-sdk]` gates `test_sdk.py` + `test_s3.py` +
  the googleapiclient tests; `.[llamaindex]` gates `test_llamaindex.py`
  + reader tests; `.[mcp]`, `.[mirage]`, `.[fsspec]` similarly;
  `llama-index-readers-hubspot<0.6` is pinned outside any extra.
- A `.[dev]`-only run is quietly narrower than the suite: state which
  install produced the numbers (the PR template demands it).

## Contribution policy (CONTRIBUTING.md)

- Fork, topic branch off `main`, one logical change per PR.
- A bug fix comes with a test that fails without it.
- `pytest` and `ruff check . && ruff format --check .` must pass locally
  before opening the PR — CI's first run on a first PR waits for a
  maintainer to approve the workflow (ours ran without waiting).
- PR title: one sentence saying what Backlot does once merged, prefixed
  with the closed issue's `<source>:`; no `fix:` prefix. `Closes #N` in
  the description. Start from `.github/pull_request_template.md` —
  `gh pr create --body` does not load it.
- Until one PR here is merged, one open PR at a time (drafts included);
  after that, up to three. Drafts are not reviewed; a draft left seven
  days is closed. A PR that closes an issue an open PR already closes is
  closed — verify no competing PR before opening.
- No assignment or claim-comment step for issues: the queue is managed
  by the one-open-PR rule and issue-number search.
- Fidelity bar: a divergence from the real API is a bug even when
  Backlot's answer is reasonable. Measure against the real service
  where possible and record the measurement in the comment beside the
  fix. Response shapes are pinned by `response_model`s and endpoint
  tests, not by `backlot/schemas/` (the ingest contract).
- `scripts/prose_check.py`: no issue/PR numbers in comments or
  docstrings (they go in the PR description); a date must not appear
  in both a code comment and a test comment ("said once" — the code's
  prose is the measurement's home, the test points at it).

## Why this project was selected (2026-10-09 research)

- **External merge cadence:** 15/15 recently merged PRs examined
  (Oct 7–9, 2026) were authored by outside contributors — #532 nuriyoo,
  #528 Mr-Neutr0n, #523/#520 HarshRajSinghania, #519 AK-Lmn,
  #515/#514/#513 jnohclee-rgb, #512 paoValle, #511 stilecdaniel,
  #510/#509 Fire162 — each merged within 1–2 days of creation.
- **Human review, not bot merges:** `nuriyoo` and `khj809` run real
  review cycles — CHANGES_REQUESTED → contributor fix → APPROVED →
  merge (seen on #531, #513, #509).
- **Issue quality:** fidelity issues ship with the live measurement, a
  reproduction script, the exact real-vs-Backlot rows, and a "what a
  fix has to settle" section scoping what belongs in the PR.
- **Verification needs no network, tokens, or data:** `pytest` runs on
  the bundled corpus; ruff + prose_check are local gates.
- Scored ~97/100 on the selection rubric; the alternatives screened
  are in the session report (OpsiMate ~88 — also strong, claim-comment
  required; automatos-ai ~80; lima ~65 — chosen issue taken by a
  competing PR within hours; lightweight-charts ~55 — issue closed as
  intended behavior the same day; Sall25/folio — no license, hard
  reject; moudlajs/jinx — no external merges).

## Pitfalls learned

- The issues are minted in batches and a fast-moving pool of
  contributors picks them up same-day; re-verify the issue is
  unclaimed and search open PRs for its number immediately before
  opening yours.
- `float()` accepting `inf`/`nan` is a recurring bug class: guard
  parses with `isfinite` (or range-check against SQLite's 64-bit bind,
  which a finite-but-huge value still overflows — `oldest=1e19` is a
  500 today; filed as out of scope in PR #577's description).
- Comments and docstrings are load-bearing prose here: state what was
  measured and when, never the fix history, never `#NNN`.

## Contribution history

### #554 — non-finite `oldest`/`latest` is a 500 (**MERGED** as PR #577, 2026-10-10)

- Branch: `contrib/issue-554-non-finite-ts`; PR:
  https://github.com/brekkylab/backlot/pull/577 (base `main`), closes
  https://github.com/brekkylab/backlot/issues/554.
- Fix: one `math.isfinite` guard in `_slack_ts`; the call site's
  existing `is False` checks answer `invalid_ts_oldest`/
  `invalid_ts_latest` unchanged. One parametrised test (2 params × 7
  spellings = 14 rows: the six non-finite spellings plus `not-a-ts`) —
  the 12 non-finite rows fail without the fix, all 14 pass with it.
- Validation: 6088 passed/10 skipped on `.[dev,official-sdk,llamaindex]`
  (first run, Python 3.14); 6086 passed/10 skipped after the review
  response (workspace venv, Python 3.11); touched-surface extras in full
  (SDK suite 1371 passed); ruff and prose_check clean; all 7 remote
  checks green on the PR and again on the response commit.
- Review: nuriyoo requested changes 2026-10-10 — drop `1e999` from the
  rows and docstring list (their slack.com/api measurement: real reads
  it as 1999 and answers a window, so it belongs beside `1e19` as out of
  scope), fold the two tests into one parametrised function (exact code
  supplied), docstrings must not narrate the fixed 500 (exact text
  supplied); optional `import math`/`math.isfinite` style and "a client
  that retries a 5xx" body wording. All five applied at `ab32213` with
  the regression replay and full-suite rerun; reply posted; awaiting
  re-review (a PR author cannot formally re-request; the @mention
  notifies).
- **MERGED 2026-10-10T13:59:45Z by nuriyoo** — APPROVED 13:59:30Z, merged
  15 seconds later with no further comment, merge commit `78c06e50d256`;
  issue #554 closed COMPLETED at 13:59:47Z. 19 hours open, one human
  review cycle, seven green checks on every push. The first merge in this
  portfolio — the "human review, not bot merges" selection signal held.
  Backlot is now inside its own one-open-PR-at-a-time unlock: up to three
  open PRs here from here on.
