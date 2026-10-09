# Contribution Handoff

Last updated: 2026-10-09T10:07:00Z

## Portfolio Summary

Active Contributions: 0
Monitoring Contributions: 6
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
Branch: fix/sanitize-tool-messages-contract-6314
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

## Blockers

None. All five open PRs sit behind GitHub's first-time-contributor
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
