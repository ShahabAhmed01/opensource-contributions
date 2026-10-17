# brekkylab/backlot — #779

## Status

**PR #806 OPENED, CI fully green** — opened 2026-10-17T18:19:47Z, ready
for review (not draft), base `main` @ `e9b9d72` (still the tip). All 9
check-runs completed by 2026-10-17T18:24:59Z: `gate`, `lint`, `scan` and
the test (3.11)–(3.15) matrix all success; the bare `test` job is the
workflow's skipped shape. `mergeable_state` moved from `blocked` to
`clean` at ~18:25Z. Copilot left a COMMENTED bot review (quota note,
recorded as a bot, not a human review). Per policy, no pings. Not merged
as of 2026-10-17T18:30Z.

## Issue

https://github.com/brekkylab/backlot/issues/779
"slack: conversations.history serves a message at latest without
inclusive, where real leaves it out"

OPEN, unassigned, 0 comments, created 2026-10-16T14:27:35Z by `nuriyoo`
(their Slack fidelity series), labels `good first issue`, `help wanted`,
`fidelity`, `hacktoberfest`. Filed while reviewing the merged #767, which
rewrote the same `oldest`/`latest` comparison to microsecond integers —
the `latest` boundary survived that rewrite, so the gap is live on
`main` at `e9b9d72`.

## Pull Request

[#806 — slack: a message at latest is left out unless inclusive is sent,
as one at oldest is](https://github.com/brekkylab/backlot/pull/806)

- Base branch: `main` @ `e9b9d723869e6afb01f67f92184897ce59a11827`
  (verified current at PR creation)
- Opened: 2026-10-17T18:19:47Z · State: open, MERGEABLE, not draft
- Fork head: `ShahabAhmed01:backlot/slack-history-latest-exclusive` @
  `8b042783e3`
- Closes #779 (`Closes #779.` first line of the body)
- Size: 2 files, +83/−2

## Branch

`slack-history-latest-exclusive`, cut from `upstream/main` @ `e9b9d72`.
Workspace: `~/opensource-work/backlot` (remotes: `origin` =
ShahabAhmed01/backlot — fork —, `upstream` = brekkylab/backlot). Commit
`8b042783e3b872d97ff212a9735a7071401bc6df`; branch pushed to the fork and
verified by API (branch head SHA matches) before the PR was opened.

## Commits

- `8b042783e3b872d97ff212a9735a7071401bc6df` — slack: a message at latest
  is left out unless inclusive is sent, as one at oldest is (2 files,
  +83/−2)

## Problem

`GET /slack/api/conversations.history?channel=<id>&latest=<a message's
ts>` served that message, where real Slack leaves it out unless
`inclusive` is sent; `oldest` at the same boundary was already exclusive.
The page carried one message more than real lists, so a client walking a
channel a day at a time re-read the boundary message on the next day's
page when it asked for the previous page's last `ts`.

## Root Cause

`_in_window` in `backlot/routers/slack.py` (the only window filter in the
file) read the two bounds differently: `oldest` excluded equality unless
`inclusive`, while `latest` excluded only `ts > hi`, keeping `ts == hi`.
Its comment recorded the wrong reading ("latest is inclusive"), which the
2026-10-16 measurement in the issue contradicts.

## Solution

- `ts_us > hi_us` → `ts_us > hi_us if inclusive else ts_us >= hi_us`: the
  `latest` bound is now exclusive by default and opens with `inclusive`,
  in the same shape the `oldest` line already uses. One expression, no new
  parameters, no change to the SQL pre-narrowing (`hi_sec = floor(hi)+1`
  still over-admits and the Python window decides).
- The comment beside it now records the measurement instead of the
  disproven claim.

## Files Changed

- `backlot/routers/slack.py` — the `latest` comparison in `_in_window`
  and its comment (+5/−2)
- `tests/test_slack.py` — one parametrized regression test with the
  issue's nine measured rows over HTTP, plus two module-level helpers
  (`_us_of`/`_ts_at`) that name a bound one microsecond either side of the
  middle message's ts (+78/−0)

## Tests

- **Regression proof run:** with `backlot/routers/slack.py` restored to
  its base revision and the new test in the tree, the `latest=T` row fails
  (`assert ts not in page` — `1772442000.823397` is served) and the other
  eight rows pass on both revisions; with the fix, 9/9 pass. Rows 1–3
  (`oldest`, both spellings of `inclusive`), 6, 7 and 9 are controls that
  pass either way; the single changed row is the one the issue reports.
- **Full suite:** `PYTHONWARNDEFAULTENCODING=1 pytest` on
  `uv pip install -e ".[dev]"` (Python 3.14.8, xdist): **7865 passed,
  38 skipped, exit 0** in 2:14. The 38 skips are the extra-gated surfaces
  CONTRIBUTING maps (`test_s3.py`, `test_sdk.py`, `test_mcp.py`,
  `test_llamaindex.py`, gated parts of `test_integrations.py`); none
  touches the Slack window, and `tests/test_slack.py` is dev-covered and
  ran whole.
- **Lint:** `ruff check .` clean; `ruff format --check .` — 159 files
  already formatted; `ruff check --preview --select PLW1514 .` clean.
- **Prose gate:** `python scripts/prose_check.py upstream/main` clean —
  the measurement date lives in the router comment only; the test points
  at it.
- **Diff hygiene:** `git diff --check` clean; independent read-only
  review (row-by-row predicate check against all nine measured rows, a
  repo-wide search for a second window implementation, the SQL
  pre-narrowing, style and compatibility) found no defect; its two prose
  nits were applied before the commit.

## Runtime Validation

No live Slack call made from this environment (no token). The measurement
is the issue reporter's slack.com/api matrix of 2026-10-16, transcribed
into the router comment; the reproduction runs over the bundled corpus via
Starlette's TestClient, so every claim in the PR body is
locally-verifiable.

## CI (live at 2026-10-17T18:25Z)

- gate: success (18:20:00Z) · lint: success (18:20:01Z) · scan: success
  (18:20:21Z)
- test (3.11): success (18:24:29Z) · test (3.12): success (18:23:15Z) ·
  test (3.13): success (18:24:27Z) · test (3.14): success (18:24:10Z) ·
  test (3.15): success (18:24:59Z)
- bare `test`: skipped (workflow shape)
- Copilot (bot) COMMENTED — not a human review.

## Review

None yet — awaiting maintainer review (`nuriyoo`/`khj809` by history). The
only reviewer on the PR is the copilot-pull-request-reviewer bot.

## Merge

Not merged. Open, MERGEABLE, `mergeable_state: clean` (all 9 check-runs
resolved, none failing) as of 2026-10-17T18:25Z. Awaiting the first human
review.

## Lessons Learned

- The issue's own measurement table is the acceptance contract here: nine
  rows, two of them about a bound on both sides. Encoding all nine (not
  just the failing one) is what made the "alone"/"empty" wording
  testable.
- Two allocations in the same file can carry the same bug and only one be
  reported: #767 had already replaced the float comparison in this helper,
  and the inclusive-latest reading rode through that rewrite. Read the
  neighbouring branch of a fixed comparison before assuming the fix
  covered both.
- `-q` in the command stacks with the `-q` already in pytest's `addopts`
  to `-qq`, which suppresses the summary line; the suite counts above come
  from a plain `pytest -rs` run.
