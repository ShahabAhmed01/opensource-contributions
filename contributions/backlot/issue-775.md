# brekkylab/backlot — #775

## Status

**PR #786 REWORKED PER THE HUMAN REVIEW, CI GREEN, AWAITING RE-REVIEW** —
`nuriyoo`'s four-point review of 2026-10-17T10:47:21Z was applied in full
(commit `27e8922f`, their three code suggestions verbatim) and the branch
was rebased onto `main` @ `e9b9d72` while there (commits `e1a0f3a3` +
`27e8922f`; the original `166bb7a` was rewritten by the rebase). The PR
was renamed to "jira: a comment read reads orderBy as Java reads it, so a
no-break space is refused and U+0001 is served" — both of the title's
examples still hold under the new reading. All 9 check-runs green on the
reworked head by 2026-10-17T20:21:55Z (gate, lint, scan, test
3.11–3.15; bare `test` the workflow's skipped shape);
`mergeable_state: clean`. Reply comment `6240438402` posted 20:22:46Z
answering all four points. Per policy, no pings. Not merged as of
2026-10-17T20:35Z.

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

[#786 — jira: a comment read reads orderBy as Java reads it, so a
no-break space is refused and U+0001 is served](https://github.com/brekkylab/backlot/pull/786)

- Base branch: `main` @ `e9b9d723869e` (verified current at the rework)
- Opened: 2026-10-16T20:48:05Z · State: open, MERGEABLE (`clean`), not
  draft
- Fork head: `ShahabAhmed01:backlot/jira-comment-orderby-java-trim`
  @ `27e8922f62f6`
- Closes #775 (`Closes #775.` first line of the body)
- Size: 2 files, +49/−9

## Branch

`jira-comment-orderby-java-trim`, rebased onto `upstream/main` @
`e9b9d72` for the review response. Workspace: `~/opensource-work/backlot`
(remotes: `origin` = ShahabAhmed01/backlot — fork —, `upstream` =
brekkylab/backlot). Force-pushed with lease (`166bb7a` → `27e8922`).

## Commits

- `e1a0f3a31b094047fe3d61daac63e268450ce924` — jira: a comment read trims
  orderBy as Java's trim does, so a no-break space is refused and U+0001
  is served (the original commit, rebased onto `e9b9d72`)
- `27e8922f62f6345948c563db2dc8d75f980b3215` — jira: a comment read reads
  orderBy as Java reads it, so a control char stays behind the sigil and
  one line terminator at the end goes (the review response)

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

## Solution (as reworked 2026-10-17)

The first cut of this PR applied `_JAVA_TRIMMED` twice — outer trim, sigil,
inner trim — matching `project/search`'s order. `nuriyoo`'s 65-spelling
measurement of 2026-10-17 disproved the inner trim: after the sigil real
does **not** trim again, it *reads* the value as Java reads
`^([+-]?)\s*(.*)$` under `find` — `\s` is the six ASCII spaces, `.` stops
at a line terminator, `$` matches at the end or before one final
terminator. What the rework does:

- The outer `String.trim` stays (`raw.strip(_JAVA_TRIMMED)`).
- The sigil+field parse is now `_JIRA_ORDER.match(field)` where
  `_JIRA_ORDER` is the reviewer's pattern pasted below `_JIRA_ORDER_FIELD`
  (`.match`, so `^` holds only at the start). A control char after the
  sigil stays in the refused field (`-%01created` names U+0001 and
  `created`); `%20`, `%09`, `%0A`, `%0B`, `%0C` and `%0D` after the sigil
  go; one line terminator at the end is served (`created%C2%85` is 200);
  one anywhere else matches nothing, so the 400 names the value whole,
  sigil and all (`-%C2%85created` names `-\x85created`, `-cre%0Aated`
  names `-cre\nated`).
- If the pattern matches, the direction comes from the sigil and the field
  from group 2; if it does not, the field is the trimmed value whole (it
  always 400s, since a value with an interior terminator cannot be
  `created`).
- The 400 text stays Backlot's own sentence (real localises that message —
  documented decision in the existing docstring).

## Files Changed

- `backlot/routers/atlassian.py` — `_JIRA_ORDER` beside
  `_JIRA_ORDER_FIELD`, `_jira_order_desc` reading it, docstring paragraph
  with the measured matrix and dates (+18/−8 across both commits)
- `tests/test_atlassian.py` — `takes` now carries 7 measured rows
  (the original `%01created`, `created%01`, `%0Bcreated` plus
  `%01-created`, `-%0Bcreated`, `-%0D%0Acreated`, `created%C2%85`); the
  `refuses` test is the reviewer's 12-row table and **asserts the field
  real's 400 named** on every row (+31/−1)

## Tests

- **Rework verification:** the extracted `_JIRA_ORDER` was run over every
  row of the reviewer's table before the commit (15 taking spellings read
  `created`; all 12 refused spellings name exactly the field their table
  names, including the two whole-value rows). Full suite on the rebased
  branch: **7872 passed, 38 skipped, exit 0** (Python 3.14.8 venv,
  `PYTHONWARNDEFAULTENCODING=1`, 1:38). Collect-only deltas confirm the
  PR's contribution exactly: +16 tests vs the base (7 takes + 9 refuses
  rows); the base gained +176 upstream tests in the #782 rebase.
- **Original regression proof (2026-10-16):** with the router change
  removed from the tree, the four then-new spellings fail exactly as the
  issue measures (`%01created`/`created%01` → 400 instead of 200; NBSP/em
  space → 200 instead of 400); with the fix restored, all pass.
- **Lint:** `ruff check .` clean; `ruff format --check .` — 159 files
  already formatted; `ruff check --preview --select PLW1514 .` clean.
- **Prose gate:** `python scripts/prose_check.py upstream/main` clean on
  the rebased branch.
- **Diff hygiene:** `git diff --check` clean.

## Runtime Validation

No live Jira call made from this environment (no credentials; the
measurement is the reviewer's Jira Cloud matrix of 2026-10-17, 65
spellings with a cache-buster each, and the issue reporter's of
2026-10-16). Route tests run over the bundled corpus via Starlette's
TestClient; all claims in the PR body are local-verifiable.

## CI (live on head `27e8922f`, all completed 2026-10-17)

- lint: success (20:17:10Z) · scan: success (20:17:28Z) · gate: success
  (20:20:54Z)
- test (3.13): 20:20:15Z · test (3.14): 20:21:00Z · test (3.11): 20:21:06Z
  · test (3.15): 20:21:26Z · test (3.12): 20:21:55Z — all success
- bare `test`: skipped (workflow shape, 20:17:00Z)
- `mergeable_state: clean`; Copilot (bot) COMMENTED — not a human review.

## Review

**`nuriyoo` COMMENTED 2026-10-17T10:47:21Z** — a four-point review with
code suggestions, from a fresh 65-spelling Jira Cloud measurement:
(1) after the sigil the strip is not a second `String.trim` (`-%01created`
is a 400 naming `\x01created`, where the inner strip served 200; the six
ASCII spaces do go); (2) a line terminator behaves two ways (at the end it
goes — `created%C2%85` is 200, which the first cut refused; anywhere else
real names the value whole, sigil and all); (3) the refused rows should
assert the field real named (12 measured rows supplied); (4) all 65
answers fit Java's `^([+-]?)\s*(.*)$` under `find`, with the pattern to
paste beside `_JIRA_ORDER_FIELD`.

**All four applied** in `27e8922f` (suggestions verbatim: the pattern, the
docstring paragraph, the code, the takes rows, the 12-row refuses table
with the named-field assertion), the branch rebased onto `e9b9d72`, the
PR renamed, and reply comment `6240438402` posted 2026-10-17T20:22:46Z
listing each point and the new CI numbers. Awaiting re-review; no approval
yet.

## Merge

Not merged. Open, MERGEABLE, `mergeable_state: clean`, awaiting
`nuriyoo`'s re-review as of 2026-10-17T20:35Z.

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
  `-qq`, which eats the summary line — the suite's counts come from a
  plain `pytest` run.
- A reviewer's cross-endpoint analogy ("as `project/search` measures it")
  is a hypothesis, not a measurement: the inner trim matched #762's order
  but not the comment read's reality. Each endpoint's `orderBy` now cites
  its own measurement date, and the two reads differ on purpose
  (`project/search` trims again after the sigil; the comment read reads
  with the pattern).
- The tracker's `scripts/update_tracker.py` needs `gh`; with no gh CLI on
  this machine, a REST shim (~/bin/gh) reproduces the two calls it makes
  byte-for-byte in semantics (uppercase states, check names → pass/pending
  mapping, review author objects). Its sync also caught live drift in the
  unrelated odysseus entries (#6475/#6476 now fail their PR-description
  check upstream) — recorded, not hidden.
