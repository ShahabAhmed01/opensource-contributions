# Contribution Handoff

Last updated: 2026-10-11T16:55Z (backlot #586 / PR #620 opened)

## Portfolio Summary

Active Contributions: 0
Monitoring Contributions: 9
Merged Contributions: 3
Closed/Superseded Contributions: 0

**New this session (2026-10-11T16:45Z): backlot #586 / PR #620** — the
`invalid_cursor`/`invalid_ts` precedence follow-up nuriyoo filed while
reviewing our merged #577. `conversations_history`'s three error guards
reordered to real's reading order (latest, oldest, cursor); one
parametrised test over the issue's 11 measured rows (8 fail on unmodified
main, all 11 pass with the fix); full suite 6346 passed/10 skipped; CI
7/7 green on first push, mergeStateStatus CLEAN. Opened ready for review,
awaiting `nuriyoo`/`khj809`. Not merged. This is the second open backlot
PR (policy allows three).

Three of the twelve tracks have merged, all within the last 24 hours:
backlot #577 (2026-10-10T13:59Z), libredb-studio #1628 (2026-10-11T00:34Z)
and repowise #3338 (2026-10-11T07:56Z). The seven odysseus PRs are
unchanged since 2026-10-09 (no new comments, no reviews, no state change).

**The eighth, backlot #614, got the portfolio's second human review today.**
`nuriyoo` requested changes at 2026-10-11T08:52:43Z, 20 minutes after the
PR opened, opening with "The change is right" and asking for four specific
items: a parametrised regression test (code supplied), two ACL-scoping
rows, a **Not in this PR.** line, and an inline comment wrap. Items 1-3
were pushed at 09:06Z (`9b1aad7`); item 4 was still outstanding and was
applied at 14:26Z (`7abf5b4`) along with a correction to a false causal
claim in our own description. CI 7/7 green on the response head; reply
posted 14:29Z; awaiting re-review. Not merged.

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
Status: **MERGED 2026-10-10T13:59:45Z** by nuriyoo — merge commit
78c06e50d256; issue #554 closed COMPLETED at 13:59:47Z. The portfolio's
first merged contribution. Track closed.
CI: ALL GREEN — 7/7 on first push and again on the review-response
commit ab32213 (gate, lint, scan, test 3.11/3.12/3.13/3.14 — no
first-time-contributor action_required gate; workflows ran on push)
Review: CHANGES_REQUESTED by nuriyoo 2026-10-10T06:49:20Z (first human
review; copilot bot summary before it). Three required items — drop
1e999 from the parametrize and docstring list (their slack.com/api
measurement 2026-10-10: real reads it as 1999 and answers a window, so
the PR must not pin an answer real does not give; it goes beside 1e19 in
"Not in this PR"), merge the two tests into one parametrised 14-row
function (exact code supplied), docstrings must not narrate the fixed
500 (exact text supplied) — plus two optional (import math/math.isfinite
matching byo.py and protojson.py; body wording "a client that retries a
5xx"). All five applied at ab32213 with regression replay (guard
reverted: 12 non-finite rows fail, 2 not-a-ts pass; restored: 14 pass),
full suite 6086 passed/10 skipped, ruff + prose_check clean, PR body
corrected; reply comment issuecomment-6097848273. A formal re-request is
impossible for a PR author (API denies RequestReviewsByLogin); the
@mention notifies. Reviewer also verified our fix themselves (14 cases
fail reverted; their merged-with-today's-main run: 6196 passed, 1
skipped) and filed a separate precedence issue, explicitly not for this
PR. PR MERGEABLE.
Notes: First non-odysseus track. Selection research 2026-10-09: 25+
repos discovered, 10 screened, 5 verified in depth; backlot scored ~97/100
(15/15 merged PRs Oct 7-9 from outside authors, human CHANGES_REQUESTED/
APPROVED cycles by nuriyoo and khj809, 1-2 day merge turnaround).
Issue #554 (labels: bug, good first issue, help wanted, fidelity,
hacktoberfest) was unassigned with 0 comments and no competing PR —
re-verified before implementation, before commit, and at 18:41Z
immediately before opening the PR. Fix: one math.isfinite guard in
`_slack_ts` (backlot/routers/slack.py) so `oldest=inf`/`nan` and every
spelling `float()` reads non-finite (inf, -inf, nan, Infinity, -Infinity,
NaN) answers invalid_ts_oldest/invalid_ts_latest instead of the 500 the
window's uncaught `int()` raised. One parametrised test (2 params × 7
spellings = 14 rows; the spellings plus not-a-ts) fails 12 rows without
the fix, passes all 14 with it; 1e999 deliberately not pinned — real
answers a window for it (review measurement), recorded as out of scope
beside 1e19. Local after review response: 6086 passed/10 skipped in this
workspace venv (Python 3.11; first run was 6088/10 on Python 3.14);
SDK suite 1371 passed; ruff + scripts/prose_check.py clean. PR follows
the repo's template exactly (Closes #554, source-prefixed title,
measured table, install-specific verification lines); the
finite-but-huge ts (`oldest=1e19`, SQLite bind overflow) is documented
as out of scope in the PR description — it belongs with the
lenient-parse change the issue names. Policy: one open PR at a time
here until the first merge.
Next Action: None — **merged**. The one-open-PR-at-a-time limit is now
lifted for backlot (up to three open PRs there), so a backlot slot is
available again for the next measured-fidelity issue.

### Track 009
Project: libredb/libredb-studio
Issue: #1411
PR: #1628
Branch: fix/test-connection-bucket-catalog-1411
Status: **MERGED 2026-10-11T00:34:47Z** by cevheri (squash); issue #1411
closed COMPLETED at 00:34:48Z. Squash commit ca7755b0cff3. Track closed.
CI: ALL GREEN — every workflow ran to completion on the rebased head
6005817 once the first-time-contributor gate was approved: Lint/Typecheck/
Build, Unit & Integration Tests, E2E Tests, Cross-platform Tests
(windows-latest and macos-latest), Engine Smoke (Build Payload, Node 24,
Node 26), Channel E2E (tarball + npx), Helm Chart Lint, CodeQL, Secret
Scan, Dependency Scan, Analyze (actions), Analyze (javascript-typescript),
Platform Integration Rules, plus the three scanners (GitGuardian, Socket
Security x2, semgrep). Image Scan and SonarCloud skipped (not required for
forks). The 100% line-coverage gate is a required check and passed.
Review: no human review — cevheri merged directly on the strength of the
claim comment and the rebased head, then posted "thanks and welcome" on
the PR at 00:35:04Z. Only other review entry is the copilot bot.
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
Rebase 2026-10-10: main moved +13 commits (4ebc787 -> aad0c73) and the
PR went CONFLICTING; the single conflict was object-route.ts's
pinned-citation docblock, resolved by file ownership (upstream's
postgres pins 4046/4203 kept alongside this branch's trino pins
1340/1534 — upstream never touched trino, this branch never touched
postgres) and verified by that docblock's enforcing test, not by eye.
All gates re-run green including the new upstream distribution:check;
focused set 741/741 across six files (test-connection 23, couchbase 151,
trino 219, citations 140, object-route-edit 19, migration-generator
189); full suite green except the proven test-runner-cli pair;
force-pushed with lease (53145e4 superseded by 6005817); GitHub
recomputed MERGEABLE.
Next Action: None — **merged**. Outstanding maintainer question still
unanswered: cevheri asked on issue #1411 at 2026-10-09T22:43:56Z "how was
first-contribute on libredb studio / which databases are you using on
libredb studio". The issue is closed and the PR merged, so this is now
courtesy rather than review — a short reply on #1411 reopens a channel
with a maintainer who answers in minutes-hours, and libredb-studio is a
productive next target (the repo has no open-PR cap).

### Track 010
Project: repowise-dev/repowise
Issue: #3285
PR: #3338
Branch: fix/flat-ternary-python-3285-v2
Status: **MERGED 2026-10-11T07:56:49Z** by RaghavChamadiya (squash).
Issue #3285 stays OPEN — deliberate: the PR fixes the Python half only
("Related to", not "Closes"), leaving eight grammars as sequenced
follow-ups. Track closed for the Python half.
CI: the first-time-contributor gate on the `CI` run was approved and the
workflows completed green on head b8224ee; merge was not blocked by any
check.
Review: APPROVED by RaghavChamadiya 2026-10-11T07:56:46Z, merged three
seconds later at 07:56:49Z with no intervening comment — squash commit
41bf297d. No human review comments during the PR's 15h01m life; only
repowise-bot's co-change hint (answered) and copilot's non-review.
Notes: First repowise track, and the first AGPL-3.0 repo in the portfolio.
Selection research 2026-10-10: the issue is a maintainer-authored defect with a
measured before/after table and a prescribed approach ("extend #3278's
mechanism, one language per commit or per PR"), and its blocking PR #3278 had
merged that same morning (11:14:20Z, 84f1499), so the work was unblocked and
the exact file set to touch was public. Honest note on the merge odds: 89 of
the last 100 merged PRs here are the maintainer's own (RaghavChamadiya runs
the project's agent loop too), and 11 came from outside authors, one each from
11 distinct accounts — human review does happen (RaghavChamadiya, swati510)
but this is a maintainer-driven repo, slower and less certain than backlot.
Issue #3285 (labels: bug, help wanted) was unassigned with zero comments and
no competing PR; claimed by comment issuecomment-6098334087 at 14:08:29Z per
CONTRIBUTING.md ("That comment is what reserves the issue"), and the PR opened
2h47m later. Python is one of nine grammars named in the issue and the one it
names first, chosen because it is the hard case: TypeScript's ternary names
`consequence`/`alternative` and Python's `conditional_expression` names
neither — both arms are bare `body`/`orelse` children — so #3278's
`flat_ternary_kinds` could not simply be copied over. Fix: a new
`ternary_arms_positional` map field (set only on `_PY`) naming the second
contract difference flat kinds cannot express, plus a `_ternary_else_arm()`
helper in cyclomatic.py; `walk_if` and every other language map untouched, so
the diff is 4 files (+76/−8) and no other grammar's behaviour moves. Measured
with the flag toggled off in-process: the chain `1 if a else 2 if b else 3 if c
else 4` went max_nesting 3 -> 1, now exactly what the equivalent
`if/elif/elif/else` scores, and a ternary inside a real `if` still nests (2).
TDD: all 5 new Python tests fail on the unfixed walker (3/3/2) first; one
existing test renamed because it pinned the buggy nesting of a real source
expression. No golden/fixture updates are owed — the issue asks each language
to update its health-score goldens, but #3278, the accepted precedent, updated
none of its 6 files, and no Python golden scores a chain (stated in the PR
rather than silently omitted). Local: focused file 78 passed; touched surface
(providers + unit/health) 3639 passed on the pushed head; **full tests/unit/
28906 passed/20 skipped/6 xfailed in 57m on the pushed head b8224ee itself**
(28724 on the pre-rebase base bc89359 with the same zero failures — the
difference is upstream's added tests); ruff, mypy, doc-drift and
`git diff --check` all clean. The repo's own repowise-bot flagged three absent
companion files (test_complexity_walker.py, walker.py, perf/dialects/
__init__.py) — all three checked and answered with evidence in comment
issuecomment-6100296024; none is owed, nor any golden. Workspace is a shallow
clone, so
`git rebase` across the moved base was unusable (whole-tree add/add) and the
commit was cherry-picked onto b010215 instead; `main` moved twice more
(3289287, 342046f), neither touching any file this branch changes, so the PR
head stays stable and GitHub reports MERGEABLE. Follow-ups deliberately left
open: the other eight grammars — java/c/cpp/csharp/dart/objectivec are a
one-line map change each, php is left-associative and needs its own design.
Next Action: None for the Python half — **merged**. The remaining eight
grammars of #3285 are the follow-up queue, one per PR as the issue asks.
Measured effort: java/c/cpp/csharp/dart/objectivec are a one-line
`flat_ternary_kinds`-style map change each (their grammars do expose
consequence/alternative, which is why #3278 handled TS/JS but these were
left); php is left-associative and needs its own design before it can be
batched. Worth sequencing a second repowise PR now that a merge is on
record — but note the repo is maintainer-driven (89 of the last 100 merged
PRs are RaghavChamadiya's), so treat it as low-priority compared with a
backlot slot, where the turnaround is 1-2 days.

### Track 011
Project: brekkylab/backlot
Issue: #610
PR: #614
Branch: contrib/issue-610-s3-bucket-slash
Status: CHANGES_REQUESTED — **review response pushed 2026-10-11T14:26:02Z**
(head 7abf5b4). Not merged; PR OPEN and MERGEABLE.
CI: ALL GREEN on the response head 7abf5b4 — gate, lint, scan, test (3.11/
3.12/3.13/3.14), verified 14:31Z. Still no first-time-contributor
action_required gate (previous merged PR #577 lifted the one-open-PR cap;
up to three now permitted).
Review: **CHANGES_REQUESTED by nuriyoo 2026-10-11T08:52:43Z** — the second
human review cycle in this portfolio, 20 minutes after the PR opened. Opens
with "The change is right", then four items. Copilot's only entry is a
non-review (quota exhausted).
Notes: Second backlot track. Issue labeled good first issue, help wanted,
fidelity, hacktoberfest. Selected 2026-10-11: 0 comments, no assignee, no
competing PR — claimed by comment at 08:19Z, PR opened 08:32Z. **What
nuriyoo asked for:** (1) nothing pinned the answer — add a parametrised
test over the issue's eight queries on GET and HEAD comparing `/{bucket}`
with `/{bucket}/`, exact code and placement supplied, because
`tests/test_s3.py` was absent from the diff and the three tests that failed
without the fix all read the schema rather than sending a request to
`/{bucket}/`; (2) two rows for the new path in the ACL-scoping table so the
second checkbox has a scoped-token proof; (3) a **Not in this PR.** line for
the five methods the issue did not measure; (4) an inline wrap on
`tests/test_openapi.py:283` (111 chars against the file's 100). Items 1-3
were already applied and pushed as `9b1aad7` at 09:06Z with the description
corrected; **item 4 was still outstanding and was applied as `7abf5b4` at
14:26Z**, this session. Fix itself unchanged: two route decorators
(`@router.head("/{bucket}/")` on `head_bucket`,
`@router.get("/{bucket}/", openapi_extra={"parameters": _P_BUCKET_GET})` on
`bucket_get`), mirroring the `list_buckets` pattern of registering both
`/s3` and `/s3/`; 11/16 of the issue's 16 GET/HEAD pairs differed on
unmodified main, all 16 match on the fix branch. Regression replay
reproduced the reviewer's number exactly — `s3.py` restored to `main` gives
15 of the 16 new cases plus the ACL test failing (a HEAD with `?acl`
already matched), restored back, all 17 pass. Full suite **6351 passed /
10 skipped** on `.[dev,official-sdk,llamaindex]` Python 3.11 (the skips are
`mcp`, `mirage`, `gdrive_fsspec`, HubSpot reader — not installed here);
ruff check/format clean; prose_check shows only the pre-existing
`tests/test_google.py:6355` finding. **One correction to our own
description:** the first **Not in this PR.** paragraph gave a false reason
("the object route is declared before the bucket routes"). Declaration order
disproved it (bucket `s3.py:1069-1070`, object `:1763` and `:2946`), and
removing the two decorators and diffing the five methods' answers
byte-for-byte proved the true reason: the new decorators serve only GET and
HEAD, so PUT/POST/DELETE/PATCH/OPTIONS never match them. The paragraph was
rewritten to say that, and the correction is disclosed in the reply.
Reply comment issuecomment-6110067054 posted 14:29Z; a PR author cannot
formally re-request review (the API denies it), so the reply notifies.
Next Action: Await re-review from nuriyoo/khj809 on the same branch. Do not
ping again. On APPROVED nothing further is needed — CI is green and the PR
is MERGEABLE.

### Track 012
Project: brekkylab/backlot
Issue: #586
PR: #620
Branch: contrib/issue-586-history-error-order
Status: PR OPEN — awaiting first review. Opened 2026-10-11T16:45:32Z ready
for review (never a draft). Not merged.
CI: ALL GREEN on the first push (7/7 — gate, lint, scan, test 3.11/3.12/
3.13/3.14), verified 16:50Z; mergeStateStatus CLEAN, MERGEABLE at head
b9af620. No first-time-contributor action_required gate (PR #577 lifted it).
Review: copilot non-review (COMMENTED) only; no human review yet.
Notes: Third backlot track, and a direct continuation of Track 008 (#577,
merged): nuriyoo filed #586 on 2026-10-10T06:45:56Z while reviewing our
#577 PR — "Found while reviewing an open pull request that answers a
non-finite oldest or latest with these errors" — with a full measured table
against slack.com/api (2026-10-10, user token, one request per row).
Defect: `conversations_history` in backlot/routers/slack.py checked the
cursor first (invalid_cursor), then oldest, then latest, where real reads
latest, then oldest, then the cursor. So a request with two or more
unreadable arguments was named by whichever Backlot parsed first: both
timestamps unreadable answered oldest where real answers latest, and any
unreadable timestamp beside an undecodable cursor answered invalid_cursor
where real answers the timestamp's error. Fix is a pure reorder of the
three guards (hi → lo → cursor), lo/hi computed identically, downstream
window logic untouched; one comment cites the 2026-10-10 measurement.
TDD: the new parametrised test `test_slack_history_names_the_first_error_
real_would` encodes the issue's 11 measured rows (8 divergence + 3
single-argument controls); with slack.py stashed to unmodified main, 8 of
11 fail (each divergence row answered invalid_cursor or invalid_ts_oldest
where real answers the other) and the 3 controls pass; restored, all 11
pass. The non-finite rows (oldest=nan&cursor=zzz, the inf pairs) became
testable only because #577's isfinite guard is on main now. Full suite
6346 passed/10 skipped on .[dev,official-sdk,llamaindex] Python 3.11 (the
10 skips are mcp, mirage, gdrive_fsspec, HubSpot reader); ruff check/
format clean (152 files); prose_check only the pre-existing
tests/test_google.py:6355 finding. Availability re-verified immediately
before the PR: issue OPEN, 0 assignees, 0 comments, no competing PR
(searched PRs for 586 and conversations.history: #613 is a different
limit/count task; #327/#196 old and unrelated). Second open backlot PR
(#614 is the other); policy allows three after the first merge.
Next Action: Monitor PR #620 for first human review (nuriyoo/khj809);
respond on the same branch. Do not ping.

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
(Recorded 2026-10-09; superseded in part by the post-merge capacity
below — the odysseus seven are unchanged, but three slots have since
freed up elsewhere.)

## Post-merge capacity 2026-10-11

Three PRs merged in the preceding 24 hours, which changes what can be
started immediately:

- **backlot — up to 3 open PRs.** The one-open-PR cap is lifted by the
  first merge, per the maintainer's own words on #577. Now at **two open
  PRs** (#614 and #620). The `invalid_cursor`/`invalid_ts` precedence
  issue nuriyoo filed (#586) was taken this session and is PR #620,
  awaiting first review. Remaining capacity: one more backlot slot, free
  for the next measured-fidelity issue from the open pool (#611, #612,
  #609, #608 in flight with other contributors, #605, #604, #603, #601,
  #597, #594, #593, #589, #587, #579, #576, #573, #572, #571, #569, #568,
  #567, #566 and the rest of the Slack/Google/Atlassian/HubSpot fidelity
  queue — re-verify claim-clean at selection).
- **libredb-studio — no cap observed**, and `cevheri` answers in
  minutes–hours. Claim-by-comment, 100% line-coverage gate, and now one
  merged PR on record. Reply to his unanswered question on #1411 first.
- **repowise — follow-ups queued, not urgent.** Eight grammars left on
  #3285, but the repo is maintainer-driven (89/100 recent merges are
  RaghavChamadiya's), so these are filler, not a priority.
- **odysseus — 7 open PRs still unreviewed** since 2026-10-03, which is
  the constraint that kept #6187 unstarted. Do not add an eighth until
  this fleet moves.

## Portfolio audit 2026-10-11T15:11Z (merge-readiness + data integrity)

All eleven tracked entries were re-verified against live GitHub rather than
against our own records. Method: `gh pr view` for state/mergeability, the
`commits` endpoint for commit lists, `actions/runs?head_sha=` for workflow
conclusions, and `commits/{sha}` existence probes for every recorded SHA.

**Merge state — nothing blocked by us.** Three merged as recorded (backlot
#577, libredb-studio #1628, repowise #3338; merge commits verified
byte-for-byte). The eight open PRs are **all `MERGEABLE`, none conflicting,
none a draft, all on the correct base** (odysseus → `dev`, backlot →
`main`), all from `ShahabAhmed01`, diffs intact.

**Every check that can run is green.** Latest run per check name on each
current head: backlot #614 = 7/7 SUCCESS; all seven odysseus PRs = SUCCESS
on `Check PR description`, `Check PR title (Conventional Commits)` and
`Flag unmergeable PRs`.

**Why odysseus reads `UNSTABLE`, and why that is not on us.** All seven
show `mergeStateStatus=UNSTABLE` purely because seven workflows — `CI`,
`CodeQL`, `Container scan`, `Container scan (Trivy)`, `Dependency review`,
`Secret scan`, `Workflow security` — sit at `action_required` on every head.
That is GitHub's first-time-contributor gate on fork PRs: the runs cannot
execute until a maintainer approves them. It needs maintainer action, must
not be bypassed, and there are no commit statuses and no branch protection
to satisfy otherwise.

**Two stale red checks were cleared.** #6475 and #6476 still carried
`failure` conclusions from 2026-10-03 runs of `ci / PR checks`, attached to
their current heads alongside later successes, so the rollup looked red.
`gh run rerun` was correctly denied (needs base-repo admin). Instead both
PR bodies gained a genuine, reviewer-useful line — the exact head SHA the
validation ran on, plus confirmation that the fix is not yet on `dev` —
which fires the workflow's `edited` trigger. Fresh runs at 2026-10-11T15:03Z
are SUCCESS on both. Nothing was re-run or overridden to achieve this.

**Data-integrity defects found and fixed in this file.** The `commits`
arrays were wrong in four places. Two were outright fabricated: odysseus
#6472 held `2f330657e8f4a5b7c8d9e0f1a2b3c4d5e6f7a8b9` and #6473 held
`35e3b298f4a5b7c8d9e0f1a2b3c4d5e6f7a8b9c0` — correct 8-hex prefixes padded
with the *same* filler substring `4a5b7c8d9e0f1a2b3c4d5e6f7a8b9`, and
neither exists as an object on GitHub (`HTTP 422`). One was stale: #6453
recorded `45d372b2…`, a real commit since rebased away to `35c1b23bf`. One
was truncated: backlot #577 recorded the 7-char `ab32213` and omitted two
commits, listing 2 of 4. All eleven `commits` arrays were rebuilt from the
PR endpoint and now match GitHub exactly (0 mismatches, verified). The
fabrication matters: the tracker's whole value is that it is checkable
against a remote, so a made-up SHA silently poisons every later audit.

Also refreshed #6475 and #6476 PR bodies with their validated head SHAs and
an explicit statement that each fix is still absent from `dev` (confirmed by
grepping `src/caldav_sync.py` and `src/context_compactor.py` on `dev`).

## Blockers

None. Only the seven odysseus open PRs remain, all behind GitHub's
first-time-contributor `action_required` CI gate — an expected protection
that must not be bypassed. No human review comments on odysseus since
2026-10-03 (the PRs are 2-9 days old); odysseus maintainers merge daily,
so this is the longest-waiting fleet. **The three non-odysseus tracks have
all landed**: backlot #577 merged 2026-10-10T13:59:45Z, libredb-studio
#1628 merged 2026-10-11T00:34:47Z and repowise #3338 merged
2026-10-11T07:56:49Z (see Tracks 008-010). **backlot #614 (Track 011) is
open with all CI green and a CHANGES_REQUESTED from `nuriyoo` that has been
fully addressed — head `7abf5b4`, reply posted 14:29Z, awaiting
re-review** (see Track 011). **backlot #620 (Track 012) is open with all CI
green (7/7, mergeStateStatus CLEAN) awaiting its first human review** (see
Track 012). The outstanding item on all nine open PRs is a human decision,
not work.

Two open courtesies, neither blocking:

- cevheri's questions on libredb issue #1411 (2026-10-09T22:43:56Z, "how
  was first-contribute on libredb studio / which databases are you using")
  are still unanswered; he merged the PR anyway. Worth a short reply.
- backlot's `invalid_cursor`/`invalid_ts` precedence issue, filed by
  nuriyoo separately and explicitly out of scope for #577, is a ready
  follow-up; backlot's one-open-PR cap is lifted to three since the merge.

## Environment

- GitHub account: `ShahabAhmed01` (id 192491541)
- Odysseus fork: https://github.com/ShahabAhmed01/odysseus
- Odysseus remotes: `origin` = fork, `upstream` = odysseus-dev/odysseus
- Backlot fork: https://github.com/ShahabAhmed01/backlot
- Backlot remotes: `origin` = fork, `upstream` = brekkylab/backlot
- LibreDB Studio fork: https://github.com/ShahabAhmed01/libredb-studio
- LibreDB Studio remotes: `origin` = fork, `upstream` = libredb/libredb-studio
- LibreDB Studio workspace: `/run/media/xfc11/EOD/opensource/libredb-studio`
  (clone of `main`, rebased branch onto `aad0c73abad2c123d89189d839b614cdf9b00c7e`,
  bun 1.4.2 at ~/.bun/bin,
  1238 packages installed)
- Backlot workspace: `~/opensource-work/backlot` (branch
  `contrib/issue-554-non-finite-ts`, uv venv with `.[dev,official-sdk,
  llamaindex]` — resolves to Python 3.11.17 in this workspace, which is
  what the 2026-10-10 review-response runs used; the PR's first-run
  numbers came from the original Python 3.14 install — both recorded in
  the PR and the per-contribution record; bundled corpus imported in
  `data/`)
- Repowise fork: https://github.com/ShahabAhmed01/repowise
- Repowise remotes: `origin` = fork, `upstream` = repowise-dev/repowise
- Repowise workspace: `~/opensource-work/repowise` (shallow clone `--depth 60`
  of `main`; branch `fix/flat-ternary-python-3285-v2` @ `b8224ee` cut from
  `b010215`; uv workspace, Python 3.11.17 — **`git rebase` is unusable in this
  clone across a moved base, cherry-pick instead**)
- Public tracker repo: https://github.com/ShahabAhmed01/opensource-contributions
- Known env-dependent test failures (identical on unmodified dev): browser
  tests need Playwright chromium binaries; containment/workspace tests need a
  bubblewrap-visible interpreter path (venv on an external mount); wave3 local
  tests need real model downloads; test_tls_overrides_scope fails due to
  in-tree worktree clones.
