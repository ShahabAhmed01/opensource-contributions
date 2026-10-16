# brekkylab/backlot — #775

## Status

**PR #786 OPENED and CI GREEN** — opened 2026-10-16T20:48:05Z, ready for
review (not draft), base `main` @ `41199cf`. All 8 checks green at
2026-10-16T20:52:53Z: gate, scan, lint and the test (3.11)–(3.15) matrix
(each completed success); the bare `test` job is the workflow's skipped
shape and answers the checks-all-pass assertion only as a skip, not a
run. Copilot left a COMMENTED bot review (recorded as a bot, not a human
review). Per policy, no pings. Not merged as of 2026-10-16T21:05Z.

## Issue

https://github.com/brekkylab/backlot/issues/775
"jira: a comment read trims orderBy as Python does, so a no-break space is
served and %01 is refused"

OPEN, unassigned, 0 comments, created 2026-10-16 by `nuriyoo` (their Jira
Cloud fidelity series), labels `good first issue`, `help wanted`,
`fidelity`, `hacktoberfest`. Availability verified by API at
2026-10-16T20:20Z, 20:40Z and again immediately before PR creation. Five
same-day good-first-issue tasks were screened; #778/#776/#774 were already
claimed by open PRs #781/#783/#785, leaving #775 and #763 free; #775
selected on acceptance clarity.

## Pull Request

[#786 — jira: a comment read trims orderBy as Java's trim does, so a
no-break space is refused and U+0001 is served](https://github.com/brekkylab/backlot/pull/786)

- Base branch: `main` @ `41199cfbc3` (verified current at PR creation)
- Opened: 2026-10-16T20:48:05Z · State: open, MERGEABLE, not draft
- Fork head: `ShahabAhmed01:backlot/jira-comment-orderby-java-trim`
- Closes #775 (`Closes #775.` first line of the body)
- Size: 2 files, +33/−4

## Branch

`jira-comment-orderby-java-trim`, cut from `upstream/main` @ `41199cf`.
Workspace: `~/opensource-work/backlot` (remotes: `origin` =
ShahabAhmed01/backlot — fork —, `upstream` = brekkylab/backlot). Commit
`166bb7affd2ec4d54c8af1605ab026d51692975b`; branch pushed to the fork and
verified by ls-remote before the PR was opened.

## Commits

- `166bb7affd2ec4d54c8af1605ab026d51692975b` — jira: a comment read trims
  orderBy as Java's trim does, so a no-break space is refused and U+0001
  is served (2 files, +33/−4)

## Problem

`GET /rest/api/3/issue/{key}/comment?orderBy=…` was trimmed with Python's
`str.strip()`, which strips what Python counts as whitespace: a no-break
space (`U+00A0`) or em space (`U+2003`) goes and `U+0001` stays. Real Jira
Cloud, measured on the comment read (2026-10-16, the issue's matrix), does
the opposite: Java's `String.trim` removes every character up to U+0020 at
either end and nothing past it, so `%01created` and `created%01` are 200
where Backlot refused them, and `%C2%A0created`/`%E2%80%83created` are the
400 naming " created" where Backlot served them.

## Root Cause

`_jira_order_desc` in `backlot/routers/atlassian.py` (the only call site:
the comment-read endpoint at :1040) applied `str.strip()` before the
direction sigil and again after it. The merged `_jira_project_order`
(`project/search`, PR #762 — the very PR whose review surfaced this issue)
already implements the correct trim with the module's `_JAVA_TRIMMED`
helpers; the comment path simply had not been aligned to it.

## Solution

- `raw.strip()` → `raw.strip(_JAVA_TRIMMED)` and
  `field[1:].strip()` → `field[1:].strip(_JAVA_TRIMMED)`: the trim is now
  Java's, the same bytes #762 keeps at module level, applied in the same
  trim → single sigil → trim order as `project/search`.
- Docstring paragraph added with the measured matrix and its date.
- The 400 text stays Backlot's own sentence (real localises that message —
  documented decision in the existing docstring); only the trim shape
  changed, everything else about the parameter reads as before.

## Files Changed

- `backlot/routers/atlassian.py` — the two trim calls + docstring
  paragraph (+10/−2)
- `tests/test_atlassian.py` — three new `takes` rows
  (`%01created`, `created%01`, `%0Bcreated`), two new `refuses` rows
  (`%C2%A0created`, `%E2%80%83created`), and docstring updates pointing at
  the router's dating (+23/−2)

## Tests

- **Regression proof run:** with the router change removed from the tree,
  the four new spellings fail exactly as the issue measures (`%01created`/
  `created%01` → 400 instead of 200; NBSP/em space → 200 instead of 400);
  with the fix restored, all pass. `%0Bcreated` is the boundary case both
  trims answer 200 on, kept pinned.
- **Full suite:** `PYTHONWARNDEFAULTENCODING=1 pytest` on
  `uv pip install -e ".[dev]"` (Python 3.14.8, xdist 32 workers,
  2026-10-16): **7685 passed, 38 skipped, exit 0** in 2:12. The 38 skips
  are the extra-gated surfaces CONTRIBUTING maps (`test_s3.py`,
  `test_sdk.py`, `test_mcp.py`, `test_llamaindex.py`, gated parts of
  `test_integrations.py` — 35 collected: 37 skipped, 1 passes); none
  touches the Jira path; `tests/test_atlassian.py` is dev-covered and ran
  whole.
- **Lint:** `ruff check .` clean; `ruff format --check .` — 159 files
  already formatted; `ruff check --preview --select PLW1514 .` clean.
- **Prose gate:** `python scripts/prose_check.py upstream/main` clean
  after moving the second dated mention out of the tests (`prose_check`
  itself flagged the re-dating: the check works); `prose_check.py`
  (default base) clean after fork `main` sync.
- **Diff hygiene:** `git diff --check` clean; independent read-only
  review (verification of trim semantics per every discriminating class,
  call-site audit, decoding audit) passed all points.

## Runtime Validation

No live Jira call made from this environment (no credentials; the
measurement is the issue reporter's Jira Cloud matrix of 2026-10-16 and is
external-corroboration-consistent with the merged #762 reading). Route
tests run over the bundled corpus via Starlette's TestClient; all claims
in the PR body are local-verifiable.

## CI (live at 2026-10-16T20:52:53Z)

- gate: success (20:48:19Z) · scan: success (20:48:34Z) · lint: success
  (20:48:24Z)
- test (3.11)/(3.12)/(3.13)/(3.14)/(3.15): all success
  (completed 20:52:18–20:52:53Z)
- bare `test`: skipped (workflow shape at 20:48:10Z)
- Copilot (bot) COMMENTED — not a human review.

## Review

None yet — awaiting maintainer review (`nuriyoo`/`khj809` by history). No
human review, no approval, no merge. The GitHub records the only
reviewer as the copilot-pull-request-reviewer bot.

## Merge

Not merged. Open, MERGEABLE, awaiting review as of 2026-10-16T21:05Z.

## Lessons Learned

- The issue queue moves in same-day batches: three of five same-day
  `good first issue` issues were claimed by PRs before research completed.
  Check `closedByPullRequestsReferences`-equivalent and open-PR text
  search right before choosing, then again before publishing.
- prose_check enforces "date once, reference elsewhere" — the measurement
  date lives in the code comment (the attribution home), and tests point
  at it; my first draft was flagged and the fix was to reference, not
  re-date.
- pytest's ini `addopts` already carries `-q`; adding `-q` again stacks to
  `-qq`, which eats the summary line — the suite's 7685/38 counts came
  from a plain `pytest` run, and the earlier `-qq` runs (identical
  progress, no failures) were re-run only to capture the counts honestly.
- The tracker's `scripts/update_tracker.py` needs `gh`; with no gh CLI on
  this machine, a REST shim (~/bin/gh) reproduces the two calls it makes
  byte-for-byte in semantics (uppercase states, check names → pass/pending
  mapping, review author objects). Its sync also caught live drift in the
  unrelated odysseus entries (#6475/#6476 now fail their PR-description
  check upstream) — recorded, not hidden.
