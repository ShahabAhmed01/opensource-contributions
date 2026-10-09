# odysseus-dev/odysseus — #6314

## Status

In review

## Issue

https://github.com/odysseus-dev/odysseus/issues/6314
"Agent prematurely stops during multi-step tool-call tasks"

## Pull Request

[#6476 — fix(agent): sanitize tool message predecessors to prevent provider errors (fixes #6314)](https://github.com/odysseus-dev/odysseus/pull/6476)

- Base branch: `dev`
- Opened: 2026-10-03
- State: open, mergeable
- Fork head: `ShahabAhmed01:fix/agent-premature-stop-6314`

## Branch

`fix/agent-premature-stop-6314`

## Commits

- `a3cce1b0c0998b909747b8978b33343a52544614` — fix(agent): sanitize tool message predecessors to prevent provider errors (fixes #6314)

## Problem

Context compaction can leave an assistant message carrying `tool_calls`
directly after a `system` message, another assistant message, or at the start
of the history. Strict providers reject that shape:

> Gemini: "Please ensure that function call turn comes immediately after a
> user turn or after a function response turn."

## Solution

`_sanitize_tool_messages()` in `src/context_compactor.py` gained a leading
pass that treats `user` and `tool` as the only valid predecessors of an
assistant `tool_calls` message. When the predecessor is invalid, the
`tool_calls` are stripped (the message text is preserved) and an empty
message is dropped; orphaned `tool` messages are still removed by the
following passes.

## Files Changed

- `src/context_compactor.py` — predecessor validation pass
- `tests/test_context_compactor.py` — `TestSanitizeToolMessagesPredecessor`
  (6 tests: valid predecessors keep `tool_calls`, invalid ones strip them,
  content preservation, orphaned tool-message removal)

## Tests

- Focused: `tests/test_context_compactor.py::TestSanitizeToolMessagesPredecessor`
- Existing context_compactor (29) and agent_loop (54) tests pass
- Syntax: `compileall` clean
- Runtime gap: the live Gemini scenario was not reproduced end-to-end; the
  PR description states this explicitly

## CI

PR checks passing (description, Conventional Commits, unmergeable). The
`CI`/`CodeQL`/scan workflows are `action_required` pending maintainer approval
for a first-time contributor — an expected gate, not a failure.

## Review

No maintainer review yet.

## Merge

Not merged.

## Related Work

[PR #6506](https://github.com/odysseus-dev/odysseus/pull/6506) (opened
2026-10-05 by another contributor) targets the same issue with a broader
root-cause change: Gemini context-window mapping in `src/model_context.py`,
active-user-prompt preservation in `trim_for_context()`, and a synthetic user
turn instead of stripping `tool_calls`. It currently conflicts with `dev`.
Both PRs touch `_sanitize_tool_messages()`, so they are recorded here for the
maintainer to sequence.

## Notes

Reconciled against live GitHub state 2026-10-09.
