# Contribution Handoff

Last updated: 2026-10-09T12:45:00Z

## Portfolio Summary

Active Contributions: 0
Monitoring Contributions: 7
Merged Contributions: 0
Closed/Superseded Contributions: 0

## Active Tracks

### Track 001
Project: odysseus-dev/odysseus
Issue: #2740
PR: #6453
Branch: fix/sqlalchemy-declarative-import-2740
Status: MONITORING
CI: RE-RUNNING (action_required gate)
Review: AWAITING_REVIEW
Notes: Rebased 2026-10-09 onto upstream/dev@a8c147b238db (backup tag
backup/2740-pre-rebase-20261009). Upstream had already deleted five of the
stub blocks we edited, so the diff shrank from 22 to 17 files (+17/-18).
Pushed with --force-with-lease; PR is MERGEABLE. Full suite after rebase:
13759 passed, 71 skipped, 3 deselected (env-dependent browser/namespace
cases that fail identically on unmodified dev). PR body updated with the
rebase note and current numbers.
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 002
Project: odysseus-dev/odysseus
Issue: #6432
PR: #6472
Branch: fix/calendar-quick-parse-token-budget-6432
Status: MONITORING
CI: PASSING (action_required gate)
Review: AWAITING_REVIEW
Notes: Target code still unfixed upstream (quick_parse still 512/20). 438
commits behind upstream but GitHub reports MERGEABLE (no conflicts); no
force-push churn applied.
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 003
Project: odysseus-dev/odysseus
Issue: #5049
PR: #6473
Branch: fix/scheduler-research-settings-guard-5049
Status: MONITORING
CI: PASSING (action_required gate)
Review: AWAITING_REVIEW
Notes: Target code still unfixed upstream (research_* still unguarded int()).
MERGEABLE; no rebase needed.
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 004
Project: odysseus-dev/odysseus
Issue: #6464
PR: #6475
Branch: fix/caldav-opencloud-token-spaces-6464
Status: MONITORING
CI: PASSING (action_required gate)
Review: AWAITING_REVIEW
Notes: Target code still unfixed upstream (caldav still username/password
kwargs). MERGEABLE; no rebase needed.
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 005
Project: odysseus-dev/odysseus
Issue: #6314
PR: #6476
Branch: fix/agent-premature-stop-6314
Status: MONITORING
CI: PASSING (action_required gate)
Review: AWAITING_REVIEW
Notes: Target code still unfixed upstream (_sanitize_tool_messages unchanged).
Competing PR #6506 targets the same issue/function; ours kept open and a
factual "Related work" note was added to the PR body rather than closing.
MERGEABLE; no rebase needed.
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 006
Project: odysseus-dev/odysseus
Issue: #6186
PR: #6647
Branch: fix/notes-read-intent-6186
Status: MONITORING
CI: IN PROGRESS (action_required gate)
Review: AWAITING_REVIEW
Notes: Three read-only routing rows added to _ROUTING_PATTERNS in
src/action_intents.py (+11 lines) plus new tests/test_action_intents_notes.py.
Classifier snapshot diff: 20/57 phrases changed, 0 True->False regressions;
"open my notes" stays ui; definition questions stay plain chat. 1230
routing/intent/turn-contract tests pass; full suite 13783 passed (70 failures
all environmental — missing Playwright binaries, bubblewrap-hidden venv,
model downloads — and none import this module). PR #6647 opened 2026-10-09
against dev, MERGEABLE. Launched despite 5 open unreviewed PRs per the
capacity rule; candidate vetted (0 open PRs, 0 comments, no assignee).
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 007
Project: odysseus-dev/odysseus
Issue: #1912
PR: #6648
Branch: fix/compose-send-stale-account-1912
Status: MONITORING
CI: PASSING (description, Conventional Commits, unmergeable checks green; first-time-contributor workflows at action_required)
Review: AWAITING_REVIEW (automated copilot comment only)
Notes: `_resolveComposeSendAccountId` returned the stale active id precisely
when the account row was gone — `if (!activeAccount || _accountCanSend(activeAccount))
return activeAccountId;` at static/js/document.js:120. The guard is split so a
missing account resolves to null (the server then picks the default SMTP
account) and compose tells the user `Selected email account no longer exists;
using your SMTP account.`; the receive-only branch keeps its guard and message.
New tests/test_compose_send_account_resolution_js.py: structural guard-order
assertion plus a node harness running the real function source over four cases
(deleted / sendable / receive-only / no active id) — both tests fail on the
unfixed source. Full suite 13762 passed, 70 failed (the documented
environmental set), 67 skipped. Runtime validation 2026-10-09 with local SMTP
+ IMAP sinks: before = `Send cancelled: Draft save failed (404)` (nothing
sent), after = fallback toast and `Email sent account=<default>` in the app
log; screenshots on fork branch `evidence/issue-1912`. Candidate vetted at
selection: 0 comments, no assignee, no open PR — only predecessors #1942 and
#1858, both closed in the 2026-07-23 repo-transfer batch. Opened 2026-10-09
12:40Z against dev, MERGEABLE, `ready for review` label applied.
Next Action: Monitor PR for maintainer review; respond on same branch.

## Post-PR triage 2026-10-09 (after opening #6648)

Re-ran the full issue-first selection loop to fill the freed slot:

- #6606 — reporter reproduced and posted the exact fix, intends to open the PR;
  no intervention, do not race.
- #6621, #6632, #6637, #6612 — already covered by open PRs #6629, #6633,
  #6638, #6614.
- #1883 — tracking issue for fixes that are already open as PRs.
- #6187 (docs: document the supported library-provider setup flow) — the only
  claim-clean candidate; deliberately NOT started. Reasons: bundled scope with
  an open maintainer question (generic-library wording vs brand names), and it
  edits `_ROUTING_PATTERNS`-adjacent guidance that touches PR #6647's area
  (unreviewed, capacity 7 open PRs). Revalidation checklist before ever
  starting it is in decisions/odysseus-landscape-triage-2026-10-09.md
  (local-only file; recreate from this summary if absent: 0 comments, no
  assignee, no open PR, #6647 merged or sequenced, then branch from fresh dev).

No fillable slot exists right now; all seven tracks stay MONITORING.

## Blockers

None. All seven open PRs sit behind GitHub's first-time-contributor
`action_required` CI gate — an expected protection that must not be bypassed.
No human review comments since 2026-10-03; maintainers merge daily.

## Environment

- GitHub account: `ShahabAhmed01` (id 192491541)
- Fork: https://github.com/ShahabAhmed01/odysseus
- Remotes: `origin` = fork, `upstream` = odysseus-dev/odysseus
- Public tracker repo: https://github.com/ShahabAhmed01/opensource-contributions
- Known env-dependent test failures (identical on unmodified dev): browser
  tests need Playwright chromium binaries; containment/workspace tests need a
  bubblewrap-visible interpreter path (venv on an external mount); wave3 local
  tests need real model downloads; test_tls_overrides_scope fails due to
  in-tree worktree clones.
