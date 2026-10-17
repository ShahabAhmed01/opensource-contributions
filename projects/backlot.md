# Project notes — brekkylab/backlot

Last verified: 2026-10-17
## Facts

- Serves 11 real SaaS APIs — Slack, Gmail, Google Drive, GitHub, Jira,
  Confluence, Notion, S3, HubSpot, Linear, Fireflies — with the smallest
  possible gap from the real thing, so clients built against the real
  APIs work unchanged. The corpus is supplied by the user (a bundled
  `hello.jsonl` covers every source).
- Python 3.11+ / FastAPI / SQLite. MIT license. 288 stars / 58 forks
  (live 2026-10-17; the earlier "~424" reading could not be reproduced
  and is superseded). Created 2026-07-02; very active (commits merged to
  `main` daily; `main` head `e9b9d72` on 2026-10-17T11:56Z).
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

## Fidelity evidence refreshed 2026-10-16/17 (research addendum, Track 017)

- **External merge cadence (live re-verification):** 50 outside-contributor
  PRs merged in the last 30 days alone (since 2026-09-16) — the deepest
  external-merge pipeline among the portfolio's six projects;
  isomorphic-git 11 since 2026-09-26, repowise 28+, libredb-studio 27
  (their best review lane is now heavily self-claimed by senior
  contributors within hours).
- **Same-day task churn, verified first-hand 2026-10-16:** of five
  `good first issue`/`help wanted` fidelity issues filed that day
  (#778/#774/#775/#776/#763), three were claimed by open PRs
  (#781/#783/#785) while research was still screening; #775 and #763
  were the free pair; #775 won on acceptance clarity. The established
  pitfall above (re-verify issue state immediately before publishing)
  was practiced and held: still unclaimed at PR-creation time.
- Issue #775 selection rationale: an exact measured real-vs-Backlot
  matrix in the issue (Jira Cloud, 2026-10-16), a root cause that leans on
  the already-merged `_JAVA_TRIMMED` reading of #762, and a test file the
  dev install fully covers — acceptance criteria were observable and
  locally verifiable end to end.
- Verification still no-network: pytest on the dev install + ruff +
  prose_check (which caught a re-dated measurement and shaped final
  comment wording). Counts: 7685 passed / 38 skipped on Python 3.14.8.

## Fidelity evidence refreshed 2026-10-17 (research addendum, Track 018)

- **External merge cadence (live re-verification, 2026-10-17):** of the
  150 most recently closed PRs, 140 are merged and **138 of those are
  outside-contributor merges since 2026-09-16** (authors with
  `author_association` in CONTRIBUTOR/NONE/FIRST_TIME_CONTRIBUTOR), from
  **41 distinct external authors** — by far the deepest external-merge
  pipeline among the portfolio's six projects. Median merge latency for
  that sample is **34.7h** (min 0.2h, max 78.4h); ours are 4 of the 138
  (all merged 2026-10-10 → 10-14).
- **Human review, live again:** `nuriyoo` ran COMMENTED → APPROVED cycles
  on #767 (comments 2026-10-16T14:28Z, approval 2026-10-17T09:47Z), #769
  (14:42Z → 09:53Z), #773 (14:57Z → 09:59Z) and #782 (09:58Z → 11:56Z);
  first substantive response lands within hours of the PR opening.
  `khj809` merges too. Nothing here is a bot merge.
- **Queue depth:** 43 open `good first issue` tickets and 91 open
  `help wanted` on 2026-10-17; 17 open PRs. The same-day claim pressure
  of 2026-10-16 continued: on the 2026-10-17 batch, #796/#794 were
  claimed by #801/#804 within hours of filing, and three contributors
  (CRYPTONIKAV, WynandVStaden, jnohclee-rgb) hold several tickets each.
  Two open PRs (#787, #802) even duplicate one issue's fix — the
  maintainers let the earlier one win and close the other, so a free
  ticket is worth re-checking to the minute before publishing.
- **Free tickets at screening (2026-10-17):** #792 (confluence
  `restriction/byOperation` expand), #763 (github unserved-operation
  401), #749 (fidelity baseline notes), #779 (slack `latest` boundary).
  #779 won: the issue carries a nine-row measured table as its acceptance
  contract, the test file is dev-covered with no extra needed, and the
  handler was already known from two merged PRs here (#577, #620) plus
  the `#767` rewrite that left the boundary behind.
- **Verification still no-network:** pytest on the `.[dev]` install + ruff
  (+ the PLW1514 preview rule) + prose_check. Counts: **7865 passed / 38
  skipped** on Python 3.14.8 the branch's base `e9b9d72`.

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
- Two allocations of the same comparison in one file can carry one bug
  and only one be reported: #767 rewrote this helper's `oldest`/`latest`
  reading to microsecond integers and the inclusive-`latest` half rode
  through that rewrite untouched. When fixing a boundary, diff the
  neighbouring branch of the same comparison.
- A `good first issue` here can be duplicated by two open PRs before a
  reviewer closes the later one (#787 vs #802, 2026-10-17). That makes
  "no open PR references it" a check to re-run to the minute, not once at
  screening.
- `pytest`'s `addopts` already carries `-q`; adding another on the command
  line stacks to `-qq` and eats the summary line, so the counts vanish
  from the log while the run is still green. Use plain `pytest -rs` when
  the numbers matter.

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

### #610 — S3 bucket path with trailing slash returns 404 instead of bucket listing (**CHANGES REQUESTED, response pushed** as PR #614, 2026-10-11)

- Branch: `contrib/issue-610-s3-bucket-slash`; PR:
  https://github.com/brekkylab/backlot/pull/614 (base `main`), closes
  https://github.com/brekkylab/backlot/issues/610.
- Fix: two route decorators added to existing handlers —
  `@router.head("/{bucket}/")` on `head_bucket` and
  `@router.get("/{bucket}/", openapi_extra={"parameters": _P_BUCKET_GET})` on `bucket_get`.
  Mirrors the `list_buckets` pattern of registering both `/s3` and `/s3/`.
- Validation: 16 GET/HEAD query pairs from the issue measured against real S3
  (2026-10-11) — all 16 pairs match on the fix branch; 11/16 differed on
  unmodified main. `pytest tests/test_s3.py` — 211 passed; full suite 6088
  passed/10 skipped on `.[dev]`; ruff and prose_check clean; all 7 remote
  checks green on first push (gate, lint, scan, test 3.11–3.14).
- No first-time-contributor `action_required` gate (previous merged PR #577
  lifted the one-PR-at-a-time limit). PR is mergeable (`clean` state).
- **Review cycle 2026-10-11:** `nuriyoo` CHANGES_REQUESTED at 08:52:43Z,
  first human review, opening with "The change is right". Four items —
  (1) a parametrised regression test over the issue's eight queries on
  GET and HEAD, exact code and placement supplied, because
  `tests/test_s3.py` was absent from the diff and the three tests that
  failed without the fix all read the schema rather than sending a
  request to `/{bucket}/`; (2) two rows for the new path in the
  ACL-scoping table; (3) a **Not in this PR.** line for the five methods
  the issue did not measure; (4) an inline wrap on
  `tests/test_openapi.py:283`. Items 1–3 pushed as `9b1aad7` at 09:06Z,
  item 4 as `7abf5b4` at 14:26Z; reply comment issuecomment-6110067054.
  The regression replay reproduced their number exactly (15/16 + the ACL
  test fail with `s3.py` at `main`); full suite 6351 passed/10 skipped
  on `.[dev,official-sdk,llamaindex]` Python 3.11; CI 7/7 green on the
  response head. One correction to our own description: the original
  **Not in this PR.** reason ("object route declared before the bucket
  routes") was disproved by declaration order (`s3.py:1069-1070` vs
  `:1763`/`:2946`) and by removing the decorators and diffing the five
  methods' answers — the true reason is that the new decorators serve
  only GET/HEAD. Awaiting re-review.

### #586 — conversations.history error order: latest, oldest, then the cursor (**PR OPEN, awaiting review** as PR #620, 2026-10-11)

- Branch: `contrib/issue-586-history-error-order`; PR:
  https://github.com/brekkylab/backlot/pull/620 (base `main`), closes
  https://github.com/brekkylab/backlot/issues/586.
- Filed by `nuriyoo` on 2026-10-10 while reviewing our merged #577 PR
  ("Found while reviewing an open pull request that answers a non-finite
  `oldest` or `latest` with these errors") — a direct continuation of the
  same handler. Full measured table against slack.com/api (2026-10-10).
- Fix: a pure reorder of the three error guards in `conversations_history`
  to real's reading order — `latest` (`invalid_ts_latest`) before `oldest`
  (`invalid_ts_oldest`), both before the cursor (`invalid_cursor`).
  `lo`/`hi` computed identically; downstream window logic untouched; one
  comment cites the measurement.
- One parametrised test `test_slack_history_names_the_first_error_real_would`
  encodes the issue's 11 measured rows (8 divergence + 3 single-argument
  controls). Regression proof: 8/11 fail on unmodified main (each answered
  `invalid_cursor` or `invalid_ts_oldest` where real answers the other),
  3 controls pass on both; all 11 pass with the fix. The non-finite rows
  became testable only because #577's `isfinite` guard is on main now.
- Validation: full suite 6346 passed/10 skipped on
  `.[dev,official-sdk,llamaindex]` Python 3.11; ruff check/format clean
  (152 files); prose_check only the pre-existing `test_google.py:6355`
  finding. CI 7/7 green on first push (gate, lint, scan, test 3.11–3.14),
  mergeStateStatus CLEAN at 16:50Z.
- Second open backlot PR (policy allows up to three after the first
  merge; #614 is the other). Opened ready for review; template's three
  headings and three checkboxes followed. Awaiting `nuriyoo`/`khj809`;
  no human review yet; not merged.

### #775 — comment read's `orderBy` trimmed as Python strips, not as Java does (**PR OPEN — awaiting author response to nuriyoo's review** as PR #786, 2026-10-16)

- Branch: `jira-comment-orderby-java-trim`; PR:
  https://github.com/brekkylab/backlot/pull/786 (base `main` @
  `41199cfbc3`), closes https://github.com/brekkylab/backlot/issues/775.
- Filed by `nuriyoo` on 2026-10-16 (found while reviewing the merged
  #762). Full record: [`contributions/backlot/issue-775.md`](../contributions/backlot/issue-775.md).
- Fix: `_jira_order_desc` trims with the module's existing `_JAVA_TRIMMED`
  (Java's `String.trim`, the same trim `_jira_project_order` applies on
  `project/search`) before the direction sigil and again after it.
- Three new `takes` rows (incl. the boundary case both trims agree on,
  `%0Bcreated`) and two new `refuses` rows (no-break space, em space);
  the four diverging rows fail with the router revert and pass with it.
- Validation: full suite **7685 passed / 38 skipped** on `.[dev]`
  (Python 3.14.8, uv venv; the 38 are the extra-gated files CONTRIBUTING
  maps, none touching Jira); ruff lint/format and the PLW1514 preview
  rule clean; `prose_check` clean both bases (it flagged a re-dated
  measurement; tests now point at the router's dating); `git diff
  --check` clean; independent read-only review passed.
- CI: all 8 checks green at 2026-10-16T20:52:53Z (gate/scan/lint +
  test 3.11–3.15; bare `test` skipped as the workflow's shape). Copilot
  bot COMMENTED; not merged.
- Review (2026-10-17T10:47:21Z): `nuriyoo` COMMENTED with four change
  requests — the strip after the direction sigil is *not* a second
  `String.trim` (a control character there stays; only the six ASCII
  spaces go), a line terminator behaves in two ways, the refused rows
  should assert the field real named, and a Java `^([+-]?)\s*(.*)$`
  pattern is offered for beside `_JIRA_ORDER_FIELD`. Not yet answered;
  the PR is now `behind` (base advanced to `e9b9d72` via #782).

### #779 — a message at `latest` is served where real leaves it out (**PR OPEN, awaiting review** as PR #806, 2026-10-17)

- Branch: `slack-history-latest-exclusive`; PR:
  https://github.com/brekkylab/backlot/pull/806 (base `main` @
  `e9b9d7238`), closes https://github.com/brekkylab/backlot/issues/779.
- Filed by `nuriyoo` on 2026-10-16 ("Found while reviewing #767") with a
  nine-row measurement against slack.com/api the same day.
- Fix: one expression in `_in_window` — `ts_us > hi_us` →
  `ts_us > hi_us if inclusive else ts_us >= hi_us` — so `latest` excludes
  a message at the bound unless `inclusive` is sent, as `oldest` already
  did; the disproven "latest is inclusive" comment is replaced by the
  measurement. No parameter, schema or SQL-narrowing change.
- One parametrized test over the issue's nine rows, driving the endpoint
  over HTTP on the `paged_slack` corpus; with the router at its base
  revision the `latest=T` row fails and the other eight pass on both
  revisions; 9/9 pass with the fix.
- Validation: full suite **7865 passed / 38 skipped** on `.[dev]`
  (Python 3.14.8) under `PYTHONWARNDEFAULTENCODING=1`; ruff lint/format
  and the PLW1514 preview rule clean; `prose_check upstream/main` clean;
  `git diff --check` clean; independent read-only review found no defect
  (its two prose nits were applied before the commit).
- Availability: AGENTS.md's two fork-lane checks run live — #779 no
  assignees, no `closedByPullRequestsReferences`, no open PR naming it —
  and my open-PR count was 1 of 3 at publication.
- CI: all 9 check-runs green by 2026-10-17T18:24:59Z (gate/lint/scan +
  test 3.11–3.15; bare `test` skipped as the workflow's shape);
  `mergeable_state` moved `blocked` → `clean` once the matrix finished.
  Copilot bot COMMENTED; no human review yet; not merged. Second open
  backlot PR (#786 is the other), which the after-first-merge limit of
  three allows.
