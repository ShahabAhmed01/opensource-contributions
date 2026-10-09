# odysseus-dev/odysseus — #6186

## Status

In review

## Issue

https://github.com/odysseus-dev/odysseus/issues/6186
"Chat mode: read-only notes requests do not reach manage_notes"

## Pull Request

[#6647 — fix(chat): route read-only Notes requests to manage_notes (fixes #6186)](https://github.com/odysseus-dev/odysseus/pull/6647)

- Base branch: `dev`
- Opened: 2026-10-09
- State: open, mergeable
- Fork head: `ShahabAhmed01:fix/notes-read-intent-6186`

## Branch

`fix/notes-read-intent-6186`

## Commits

- `462df8f0` — fix(chat): route read-only Notes requests to manage_notes (fixes #6186)

## Problem

`classify_tool_intent()` had no pattern for reading notes, so in Chat mode a
clear read-only request never reached `manage_notes`:

| message | before | after |
|---|---|---|
| `What are my notes?` | not promoted to tools | `notes` |
| `Read my notes` | not promoted to tools | `notes` |
| `list my notes` | not promoted to tools | `notes` |
| `Show me my notes` | `ui` (opens the panel) | `notes` |
| `open my notes` | `ui` | `ui` (unchanged) |

Because the classifier returned `needs_tools=False`, `routes/chat_routes.py`
never performed the chat→agent promotion, so the model had neither the
`manage_notes` result nor the underlying rows and could not answer.

## Solution

Three rows added to `_ROUTING_PATTERNS` in `src/action_intents.py`, inside the
existing "Notes, todos, checklists, and reminders" block (which is ordered
before the `ui` "open/show panel request" row):

- `notes read request` — read verbs (`list|show|read|get|view|fetch|search|find|pull up`) followed by a Notes noun;
- `notes read question` — `what is/are/what's/which` + **possessive** + Notes noun, so definition questions such as "What is a note?" stay plain chat;
- `notes content question` — `what/which … in|on|inside|under … notes`.

A possessive noun is required so definition questions stay plain chat, and
`open` is deliberately not a read verb, so `open my notes` still opens the
panel.

## Files Changed

- `src/action_intents.py` — three rows added to `_ROUTING_PATTERNS` (+11 lines)
- `tests/test_action_intents_notes.py` — new (14 data reads, 3 panel-navigation
  phrases, 4 definition questions, plus guards that note actions, calendar
  routes and `notes.py` code requests are unaffected)

## Tests

- Focused: `tests/test_action_intents_notes.py` (new)
- Routing suites (action_intents, chat_route_tool_policy, boundary_tool_routing,
  implicit/explicit routing, turn contract, tool routing audit, agent
  continuation): **1230 passed**
- Classifier snapshot diff: 20/57 phrases changed, **0 `True → False`
  regressions**; `open my notes` still `ui`; definition questions still plain chat
- Full suite: `13783 passed, 67 skipped`; all 70 failures are environmental
  (missing Playwright browser binaries, bubblewrap-hidden venv interpreter,
  model downloads) and **none** of the 70 failing test files import
  `src.action_intents` or reference `classify_tool_intent`/`manage_notes`
- Syntax: `compileall` clean
- Runtime gap: no live browser run of Chat → `What are my notes?` (sandbox
  lacks Playwright binaries); stated explicitly in the PR description

## CI

PR checks in progress. The `CI`/`CodeQL`/scan workflows are `action_required`
pending maintainer approval for a first-time contributor — an expected gate,
not a failure.

## Review

No maintainer review yet.

## Merge

Not merged.

## Notes

Reconciled against live GitHub state 2026-10-09. Candidate vetted before
launch: 0 open PRs, 0 comments, no assignee, reproducible. Launched despite
five open unreviewed PRs because concurrency is not decreased merely because
another PR is open.
