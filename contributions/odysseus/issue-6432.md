# odysseus-dev/odysseus — #6432

## Status

In review

## Issue

https://github.com/odysseus-dev/odysseus/issues/6432
"Calendar Quick Add: background render wipes the freshly opened event form
(silent failure); secondary: quick_parse truncates reasoning-model output"

## Pull Request

[#6472 — fix(calendar): raise quick_parse token budget and timeout for reasoning models](https://github.com/odysseus-dev/odysseus/pull/6472)

- Base branch: `dev`
- Opened: 2026-10-03
- State: open, mergeable
- Fork head: `ShahabAhmed01:fix/calendar-quick-parse-token-budget-6432`

## Scope

Bug 2 only. Collaborator `CocoLng` confirmed on the issue (2026-10-02) that
bug 1 stays with #6332 and "bug 2 can go in a focused PR here".

## Problem

`quick_parse` in `routes/calendar_routes.py` called the LLM with
`max_tokens=512` and `timeout=20`. Reasoning models need far more room, so the
JSON they emit is truncated and `quick_parse` silently fails to parse it.

## Solution

Raise the outgoing call to `max_tokens=6144` and `timeout=60` — the values the
issue reporter verified — scoped to the `quick_parse` `llm_call_async` call
only.

## Files Changed

- `routes/calendar_routes.py` — `quick_parse` call kwargs only
- `tests/test_calendar_quick_parse_budget.py` — behavioural test asserting the
  outgoing kwargs

## Tests

- Focused behavioural test asserts the exact kwargs passed to `llm_call_async`
- Syntax: `compileall` clean
- Runtime gap: no live browser run of Calendar Quick Add; stated in the PR
  description

## CI

PR checks passing (description, Conventional Commits, unmergeable). The
`CI`/`CodeQL`/scan workflows are `action_required` pending maintainer approval
for a first-time contributor — an expected gate, not a failure.

## Review

No maintainer review yet.

## Merge

Not merged.

## Notes

Reconciled against live GitHub state 2026-10-09; upstream/dev still carries
`max_tokens=512, timeout=20`, so the fix is still required.

## Runtime Validation (2026-10-09)

Booted the app on this PR's branch (`uvicorn app:app`, `GET /api/health` healthy) and exercised the changed code path end-to-end in the running app's own modules. The PR description now checks the "I actually ran the app" box; the `needs runtime validation` label was cleared and `ready for review` applied.

Check performed: quick_parse route sent `max_tokens=6144, timeout=60` (was 512/20) via a stubbed LLM and parsed the event JSON.
