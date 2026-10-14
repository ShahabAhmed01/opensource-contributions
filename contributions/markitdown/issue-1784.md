# microsoft/markitdown — #1784

## Status

**CLOSED-UNMERGED (duplicate)** — PR #2699 was opened 2026-10-14T15:25:04Z and
closed by us at 2026-10-14T17:10:55Z after a deeper cross-reference sweep found
PR #2675 (languor-daiduode, opened 2026-10-08T14:47:38Z, still open) fixing the
same root cause six days earlier, with regression tests and a full PR body.
No maintainer ever reviewed #2699 (only a Copilot COMMENTED review;
license/cla passed). Issue #1784 remains OPEN. The branch
`contrib/issue-1784-csv-empty-warning` (commit `de494313`) is preserved on the
fork and can be reopened with tests if #2675 closes unmerged.

## Issue

https://github.com/microsoft/markitdown/issues/1784
"A one-byte document is generated with no error output"

OPEN, unlabeled, unassigned, created 2026-04-15, last updated 2026-09-09. The
body is a one-line symptom report with no reproduction, no file type, and no
maintainer response ever. The only human comment (doitgo, CONTRIBUTOR,
2026-09-09) identified the silent `if not rows: return ""` path in
`CsvConverter.convert()` and asked the reporter four clarifying questions that
were never answered — so even the assumption that the input is CSV is
unconfirmed. The previous session's "acceptance criteria" were inferred, not
maintainer-confirmed; that weakness was recorded here after the fact.

## Pull Request

[#2699 — fix(csv): emit UserWarning when input is empty (fixes #1784)](https://github.com/microsoft/markitdown/pull/2699)

- Base branch: `main` @ `4cc9fa1` (never advanced during the PR's life)
- Opened: 2026-10-14T15:25:04Z · Closed: 2026-10-14T17:10:55Z (self-closed)
- Fork head: `ShahabAhmed01:contrib/issue-1784-csv-empty-warning` @ `de494313`
- Size: 1 file, +6 (warning + import in `_csv_converter.py`); **no regression
  test** — the weakest point of the patch
- The PR body was the title only

## Duplicate Discovery

The previous session's availability check claimed "0 cross-references" for
#1784; that was wrong. The authoritative check is the issue timeline:

```
gh api repos/microsoft/markitdown/issues/1784/timeline \
  --jq '.[] | select(.event=="cross-referenced") | .source.issue'
```

which returns #2675 (open) and #2699 (ours). PR #2675 touches the same
`if not rows:` branch of `packages/markitdown/src/markitdown/converters/_csv_converter.py`,
adds `pytest.warns` regression tests for `b""` and `b"\n\n\n"` input in
`tests/test_csv.py`, documents verification (41 passed + black), and passed
license/cla on 2026-10-08. It strictly dominated #2699 (same behavior change,
plus tests, plus a real PR body, six days earlier).

## Resolution

Closed our PR with a courteous comment admitting the oversight and noting the
branch is preserved; no maintainer was pinged, no issue comment was posted,
and nothing was merged. Hard gate applied: "the task is already implemented or
materially duplicated" → contribution rejected after publication, correction
recorded here and in the ledger (status `closed-unmerged`).

## Lessons Learned

- The only reliable duplicate check is the issue's cross-referenced TIMELINE
  plus keyword PR searches — not search snippets, and not a single query.
  An earlier session's "0 cross-references" claim failed because it was not
  re-verified against the timeline immediately before publication.
- A symptom-only issue with no maintainer confirmation of acceptance criteria
  is weaker than it looks; ask which part is maintainer-confirmed.
- A patch without a regression test is dominated by one with tests, even
  when both change the same lines.
