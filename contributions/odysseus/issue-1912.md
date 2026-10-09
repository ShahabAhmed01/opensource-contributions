# odysseus-dev/odysseus — #1912

## Status

In review

## Issue

https://github.com/odysseus-dev/odysseus/issues/1912
"Bug: _resolveComposeSendAccountId returns stale account ID when active account is deleted"

## Pull Request

[#6648 — fix(document): fall back when the active compose account was deleted](https://github.com/odysseus-dev/odysseus/pull/6648)

- Base branch: `dev`
- Opened: 2026-10-09T12:40:19Z
- State: open, MERGEABLE, `ready for review` label
- Fork head: `ShahabAhmed01:fix/compose-send-stale-account-1912`
- Commit: `6b2581698f4d17d0322b54bd47b521ffa560ccc9` on `upstream/dev@a8c147b238db`

## Scope

Compose + schedule send resolution in the document editor only. The
issue-reported condition (deleted active account) is fixed exactly as
described; the receive-only branch and every other call of the active-account
global are untouched.

## Problem

`_resolveComposeSendAccountId()` in `static/js/document.js` read

```js
if (!activeAccount || _accountCanSend(activeAccount)) return activeAccountId;
```

so the stale id was returned precisely when the account was **absent** from
`GET /api/email/accounts`. With that id, `POST /api/email/draft` fails the
ownership check (404) and `_sendEmail` cancels the send; scheduling follows
the same path. Nothing is delivered.

## Solution

Split the guard:

```js
if (!activeAccount) {
  if (uiModule) uiModule.showToast('Selected email account no longer exists; using your SMTP account.');
  return null;
}
if (_accountCanSend(activeAccount)) return activeAccountId;
if (uiModule) uiModule.showToast('Selected email account is receive-only; using your SMTP account.');
return null;
```

`null` makes the server pick the default SMTP account (the issue's Expected
Behaviour), and the toast tells the user the sender changed instead of
switching silently — the same convention the receive-only branch already
uses.

## Files Changed

- `static/js/document.js` — `_resolveComposeSendAccountId` guard only (+5/-1)
- `tests/test_compose_send_account_resolution_js.py` — new: structural
  guard-order assertion plus a node harness that executes the real
  `_resolveComposeSendAccountId` / `_accountCanSend` source across four cases

## Tests

- `python -m pytest tests/test_compose_send_account_resolution_js.py -q` → 2
  passed; both fail against the unfixed source (verified with `git stash`)
- `node --check static/js/document.js` clean
- Full suite: 13762 passed, 70 failed, 67 skipped — the same
  environment-dependent failures this machine reports on unmodified dev
  (Playwright binaries, bubblewrap-hidden interpreter, model downloads)

## Runtime Validation (2026-10-09)

Booted the app on this branch (`uvicorn app:app`, `GET /api/health` 200,
`ODYSSEUS_DATA_DIR` isolated) with local SMTP (2525) and IMAP (2143) sinks,
two seeded email accounts, and `EMAIL_ALLOW_PRIVATE_IPS=true` so loopback mail
delivery is allowed. Drive path: headless Firefox (selenium) — select the
non-default account as active, `DELETE /api/email/accounts/<id>` while the
page keeps its pointer, then Send in the document editor compose panel.

- **Before the fix:** `Send cancelled: Draft save failed (404). Could not save
  a recovery draft.` — stale id sent to `/api/email/draft`; no mail leaves the
  app.
- **After the fix:** toast `Selected email account no longer exists; using
  your SMTP account.`, draft saved to the local IMAP sink, and the app log
  shows `Email sent account=85f2… (default) via=127.0.0.1`; the SMTP sink
  received the message.

Both screenshots are attached to the PR from fork branch `evidence/issue-1912`
(`issue-1912-before.png`, `issue-1912-after.png`).

## CI

`Check PR description`, `Check PR title (Conventional Commits)` and `Flag
unmergeable PRs` all green; `ready for review` applied (no
`needs runtime validation` / `needs visual evidence`). The CodeQL / Trivy /
container-scan / CI workflows sit at `action_required` pending maintainer
approval for a first-time contributor — an expected gate, not a failure.

## Review

Automated `copilot-pull-request-reviewer` comment only; no human review yet.

## Merge

Not merged.

## Notes

Selected from the free worker slots on 2026-10-09: 0 comments, no assignee,
no open PR; only closed predecessors #1942 and #1858, both closed in the
2026-07-23 repo-transfer batch (reviewer WGlynn had confirmed the analysis on
#1942). Competing candidates rejected: claimed issues (#6337, #6339),
reporter-staged work (#6510), contended files (`email_routes.py`, `chat.js`)
and issues with existing open PRs.
