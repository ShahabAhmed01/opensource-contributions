# Contribution Handoff

Last updated: 2026-10-09T20:53:00Z

## Portfolio Summary

Active Contributions: 0
Monitoring Contributions: 9
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

### Track 008
Project: brekkylab/backlot
Issue: #554
PR: #577
Branch: contrib/issue-554-non-finite-ts
Status: MONITORING
CI: ALL GREEN (gate, lint, scan, test 3.11/3.12/3.13/3.14 — no
first-time-contributor action_required gate; workflows ran on first push)
Review: AWAITING_REVIEW (a copilot bot summary only; no human review yet)
Notes: First non-odysseus track. Selection research 2026-10-09: 25+
repos discovered, 10 screened, 5 verified in depth; backlot scored ~97/100
(15/15 merged PRs Oct 7-9 from outside authors, human CHANGES_REQUESTED/
APPROVED cycles by nuriyoo and khj809, 1-2 day merge turnaround).
Issue #554 (labels: bug, good first issue, help wanted, fidelity,
hacktoberfest) was unassigned with 0 comments and no competing PR —
re-verified before implementation, before commit, and at 18:41Z
immediately before opening the PR. Fix: one isfinite guard in `_slack_ts`
(backlot/routers/slack.py) so `oldest=inf`/`nan` and every spelling
`float()` reads non-finite (Infinity, -inf, NaN, 1e999) answers
invalid_ts_oldest/invalid_ts_latest instead of the 500 the window's
uncaught `int()` raised. 14-case regression test (2 params × 7
spellings) fails without the fix, passes with it. Local: 6088 passed/
10 skipped on a .[dev,official-sdk,llamaindex] install; SDK suite
1371 passed; ruff + scripts/prose_check.py clean. PR follows the repo's
template exactly (Closes #554, source-prefixed title, measured table,
install-specific verification lines); the finite-but-huge ts
(`oldest=1e19`, SQLite bind overflow) is documented as out of scope in
the PR description — it belongs with the lenient-parse change the
issue names. Policy: one open PR at a time here until the first merge.
Next Action: Monitor PR for maintainer review (reviewers nuriyoo/
khj809 turn comparable PRs in 1-2 days); respond on the same branch.

### Track 009
Project: libredb/libredb-studio
Issue: #1411
PR: #1628
Branch: fix/test-connection-bucket-catalog-1411
Status: MONITORING
CI: RUNNING (Socket Security x2, GitGuardian and semgrep all pass;
the repo's OWN workflows - CI, CodeQL Advanced, Security Scan, Platform
Integration Check - sit at action_required, the first-time-contributor
approval gate, exactly like odysseus; must not be bypassed)
Review: AWAITING_REVIEW
Notes: First libredb-studio track. Selection research 2026-10-09: ~26
repos discovered, ~10 screened, libredb-studio verified in depth
(447 merged PRs/30d nearly all external; maintainers kaya-abdullah/
cevheri respond within minutes-hours; claim-by-comment; 100% line
coverage gate; Bun 1.4.2 installed for the run). Issue #1411
(maintainer-authored E2E measurements + prescribed fix plan) was
unassigned with 0 comments and no competing PR; claimed by comment
19:38Z per policy, re-verified clean immediately before the PR at
20:4xZ. Couchbase: `connect()` now refuses a 404 on
`/pools/default/buckets/<bucket>` naming the bucket (only 404 refuses;
RBAC 403/network keep the pools-proved connect). Trino: after the
`SELECT 1` probe, the pinned catalog is checked against
`system.metadata.catalogs` (the provider's own seam, not SHOW CATALOGS
— introspect.ts documents why; deviation stated in the PR) and a miss
is carried as a warning naming it via `connectWarnings()`, the channel
the test-connection route+dialog already deliver since #1401 (no
client/route change needed). TDD: all new tests shown failing on
unmodified main first. Local: all gates green; 552/552 across the five
affected files; full suite green except tests/unit/test-runner-cli.test.ts
(2 SIGINT tests failing identically on the unmodified base, proven by
stash/re-run — unrelated; the runner never merges lcov on a red run, so
coverage:check runs in CI where the 100% gate is a required check).
Two prose fixes from an independent pre-commit review were applied
before commit (measured wording from the issue; paragraph reflow).
Next Action: Monitor PR for maintainer review (kaya-abdullah/cevheri
respond within minutes-hours); respond on the same branch.

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

None. All seven odysseus open PRs sit behind GitHub's first-time-contributor
`action_required` CI gate — an expected protection that must not be bypassed.
No human review comments since 2026-10-03; odysseus maintainers merge daily.
The backlot PR (#577) has no such gate — all eight checks already ran green
on the first push; it awaits only a human reviewer.

## Environment

- GitHub account: `ShahabAhmed01` (id 192491541)
- Odysseus fork: https://github.com/ShahabAhmed01/odysseus
- Odysseus remotes: `origin` = fork, `upstream` = odysseus-dev/odysseus
- Backlot fork: https://github.com/ShahabAhmed01/backlot
- Backlot remotes: `origin` = fork, `upstream` = brekkylab/backlot
- LibreDB Studio fork: https://github.com/ShahabAhmed01/libredb-studio
- LibreDB Studio remotes: `origin` = fork, `upstream` = libredb/libredb-studio
- LibreDB Studio workspace: `/run/media/xfc11/EOD/opensource/libredb-studio`
  (shallow clone of `main` @ 4ebc78761380, bun 1.4.2 at ~/.bun/bin,
  1238 packages installed)
- Backlot workspace: `~/opensource-work/backlot` (branch
  `contrib/issue-554-non-finite-ts`, uv venv with `.[dev,official-sdk,
  llamaindex]`, bundled corpus imported in `data/`)
- Public tracker repo: https://github.com/ShahabAhmed01/opensource-contributions
- Known env-dependent test failures (identical on unmodified dev): browser
  tests need Playwright chromium binaries; containment/workspace tests need a
  bubblewrap-visible interpreter path (venv on an external mount); wave3 local
  tests need real model downloads; test_tls_overrides_scope fails due to
  in-tree worktree clones.
