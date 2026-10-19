# Contribution Handoff

Last updated: 2026-10-19T13:44Z (Track 020: starlette PR #3682 open with
11/11 checks green and `mergeable_state: clean`, awaiting first human
review — this same day also recorded Track 019, backlot #831/PR #851,
opened 12:01Z. Track 017 note of 2026-10-17T20:35Z: the #786 review
response is done: all
four of nuriyoo's points applied verbatim in `27e8922f`, the branch
rebased onto `e9b9d72`, all 9 check-runs green by 20:21:55Z,
`mergeable_state: clean`, the PR renamed, reply comment `6240438402`
posted 20:22:46Z — Track 017. Also this session: a full re-audit of all
18 records against live GitHub; every our-side item verified or fixed
(2026-10-17T19:40Z audit section). Both open backlot PRs (#786, #806)
are now wait-only.)

## Portfolio Summary

Active Contributions: 0
Monitoring Contributions: 10
Merged Contributions: 9
Closed/Superseded Contributions: 1

**New this session (2026-10-19T13:17Z): starlette #3682** —
`Include all matching routes in the Allow header of 405 responses`.
`Router.app` kept only the first `Match.PARTIAL` route, so with two or
more routes on one path a 405 advertised just that first route's methods
— reproduced three ways on `dc20b21` (bare `Router`, `Starlette` app,
`/items` + `/{name}`), always `HEAD, GET` with `POST` absent, violating
RFC 9110 §10.2.1 (anchor: discussion #2738, which @Kludex answered
"Seems valid." in 2024 and which no PR had touched in two years). The
router now collects every partial match and renders the union of their
methods, sorted for a deterministic header (`Route.handle` joins a
sorted set now too), and only when every match exposes a non-empty
`methods` — a custom `BaseRoute` keeps its own `handle()`, the guard
cubic's P2 asked for, fixed in `9fb4097` with a threaded reply. Three
new tests + one tightened assertion: **1400 passed / 2 skipped /
2 xfailed, 100% branch coverage**, ruff + mypy strict clean, zensical
build clean; `docs/routing.md` documents the behaviour, release-notes
untouched (maintainer-owned). CI 11/11 green on `9fb4097` (check,
zizmor x2, Python 3.11–3.15, benchmarks, cubic; docs preview skipped),
codspeed bot: "will not alter performance", `mergeable_state: clean`
at 13:44Z. Copilot quota-limited (no content); no human review yet, no
pings. Duplicate sweeps before opening: 3007-item corpus, all 33 open
PR bodies, all 622 discussions — discussion #2738 doubles as the PR
template's required prior discussion; AI assistance disclosed in the
body.

**New this session (2026-10-19T12:01Z): backlot #831 / PR #851** —
`gmail: a quoted address value with a - in it finds its words alone, as
real reads it`. A quoted `from:`/`to:`/`cc:`/`bcc:` value with a `-` in it
was stripped to the bare value before storage, so
`_gmail_address_match` ran the hyphen-joined alternative on it and
`from:"no-reply"` answered the messages of `from:noreply`, where real
answers none (the issue's own gmail.googleapis.com matrix, 603-message
mailbox, 2026-10-19, eight words across the four operators). `_take` now
keeps the quotes on address values, the matcher reads a quoted value's
words alone (exact-address path and `subject:`/`label:`/`in:`/`has:`
untouched), and the `me` substitution reads through the quotes. Six new
rows in `test_gmail_hyphenated_address_search` over both listings plus
three parse pins in `tests/test_search.py`; with the router stashed to
`ff92bdd` ten of the twelve new rows fail (the control
`from:"noreply"` passes either way). Zero-skip run: **11034 passed /
3 skipped** on `.[all]` (Docker/npx/llama_index-reader, environmental);
`PYTHONWARNDEFAULTENCODING=1` suite green; ruff lint/format + PLW1514
clean; prose_check exit 1 on four findings byte-identical to clean
`main`. Independent read-only review: no critical/major findings, two
wording nits applied pre-commit. CI 9/9 green (gate/lint/scan + test
3.11–3.15), `mergeable_state: clean`, Copilot bot COMMENTED (not a
human review), not merged. Availability re-checked by API to the minute
before publication (open, 0 assignees, 0 comments, 0 competing PRs,
base still `ff92bdd`). Track 019 below.

**Merge news since the last audit: #806 (backlot #779) merged
2026-10-19T06:34:01Z** (merge commit `2ffef165033c`) and **#786 (backlot
#775) merged 2026-10-18** — the portfolio is now **9 merged, 9
monitoring, 1 closed, 0 active (19 records)**; the counts above were
refreshed from live `contributions-state.json` after the 2026-10-19
sync. Both landed the same day this track's research ran, and #806's
merge freed the same-day lane for #831.

**This session (2026-10-17T19:40–20:35Z): #786 review response + full
portfolio audit.** Every one of the 18 records was re-verified against
live GitHub (merge-commit SHAs for the 7 merged; head/fork-tip/checks/
reviews/issues for the 10 open; #2699 intact as closed-unmerged), plus a
live `is:pr author:ShahabAhmed01 is:open` search confirming the
account's 10 open PRs are exactly the 10 tracked. The one our-side
defect — nuriyoo's unanswered four-point review on #786 — was fixed:
their three code suggestions applied verbatim in `27e8922f`, the branch
rebased onto `e9b9d72`, the PR renamed to "jira: a comment read reads
orderBy as Java reads it, so a no-break space is refused and U+0001 is
served" (both examples still hold), CI 9/9 green by 20:21:55Z,
`mergeable_state: clean`, reply comment `6240438402` posted 20:22:46Z.
Two non-defects were root-confirmed rather than papered over: #6473's
`gitleaks` failure is upstream history (`dab660543b5b` re-verified an
ancestor of `dev`, so every merge-ref contains its 4 findings — not
fixable from our side, and non-required), and #2700's `license/cla` is a
`microsoft-github-policy-service` check-run QUEUED since
2026-10-14T17:53Z (re-running needs base-repo write access; the
account's CLA already reads `pass` on #2699). Both backlot PRs are now
wait-only. Track 017; audit section below.

**New this session (2026-10-17T18:19Z): backlot #779 / PR #806** —
`slack: a message at latest is left out unless inclusive is sent, as one at
oldest is`. `conversations_history` served a message whose ts equals
`latest`, where real Slack leaves it out and puts it back only with
`inclusive`; `_in_window` now reads `latest` the way it already read
`oldest` (`ts_us > hi_us if inclusive else ts_us >= hi_us`), and the
disproven "latest is inclusive" comment is replaced by the issue's own
slack.com/api measurement (2026-10-16, nine rows). One parametrized test
encodes all nine rows over HTTP; with the router at its base revision the
`latest=T` row fails and the other eight pass on both revisions. Full suite
7865 passed/38 skipped on `.[dev]` Python 3.14.8 under
`PYTHONWARNDEFAULTENCODING=1`; ruff lint/format, the PLW1514 preview rule,
`prose_check upstream/main` and `git diff --check` clean; independent
read-only review found no defect (its two prose nits were applied before
the commit). PR opened MERGEABLE at 2026-10-17T18:19:47Z (template
followed: three headings + three checkboxes, `Closes #779.`); gate/lint/
scan green at 18:20Z and the full 3.11–3.15 matrix green by 18:25Z (9/9
check-runs completed, the bare `test` job is the workflow's skipped
shape); `mergeable_state` moved from `blocked` to `clean` once the matrix
finished. Copilot bot COMMENTED; no human review yet. Availability gates
held: AGENTS.md's two fork-lane checks (no assignees, empty
`closedByPullRequestsReferences`) plus no open PR naming #779, re-run
immediately before publishing; open-PR count 1 of 3 → 2 of 3 after this
one. Track 018.

**Also verified this session: a human review is waiting on #786** —
`nuriyoo` reviewed PR #786 (Track 017) at 2026-10-17T10:47:21Z and asked
for four changes, with code suggestions attached: after the direction
sigil the strip is *not* a second `String.trim` (a control character
there stays, and the refused field is named differently), a line
terminator behaves in two ways, and the refused rows should assert the
field real named — all from a fresh 65-spelling Jira Cloud measurement on
2026-10-17, with a suggested pattern to paste beside `_JIRA_ORDER_FIELD`.
#786 now reads `mergeable_state: behind` (base `main` advanced from
`41199cf` to `e9b9d72` via the #782 merge at 11:56Z) and is otherwise
untouched (no reply posted, no commits added). This is the highest-value
open action in the portfolio.

**Discovery notes for this session** — issue-first (10 search queries →
284 unique open tickets across 121 repos) plus repo-first (863-repo pool
from 8 repository searches; external-merge probe over 614 repos; the
probe itself was cut short by secondary rate limits and only partially
usable, so the shortlist was verified by direct API calls instead). Six
portfolio projects re-verified live; new candidates inspected but not
chosen: repowise (4 external merges in the sampled 50, a 51-ticket
unassigned queue, impersonal lane), libredb-studio (19 external merges;
its free `good first issue` tickets are locale-sync docs and a nixpkgs
packaging task), isomorphic-git (12 external merges; only three stale
2017–2020 tickets), markitdown (repo stale since 2026-10-04), odysseus
(15 external merges against 100+ open PRs, zero human review on six of
ours). The issue-first pool also surfaced a large number of newly created
low-star repos whose "good first issue" batches have no external-merge
history; none was pursued. No hidden exclusions were touched
(`lingdojo/kana-dojo` excluded on instruction; the homelab-monitor
locale-sync competitor is out of scope; open-source-starter-lab remains
only a lead).

**New this session (2026-10-16T20:52Z): backlot #775 / PR #786** —
`jira: a comment read trims orderBy as Java's trim does, so a no-break
space is refused and U+0001 is served`. nuriyoo measured the divergence
against Jira Cloud on #775 (2026-10-16): a comment read's `orderBy` was
stripped with Python's `str.strip()` (NBSP/em space lifted off, U+0001
kept), while real trims as Java's `String.trim` (chars ≤ U+0020 only).
`_jira_order_desc` now trims with the module's `_JAVA_TRIMMED` — the same
bytes the merged `project/search` path (#762, the PR whose review
surfaced this issue) already uses — before the direction sigil and again
after it. Five new parametrized rows (three `takes`, boundary included;
two `refuses`); the four diverging ones fail on pre-change main. Full
suite 7685 passed/38 skipped on `.[dev]` Python 3.14.8; ruff lint/format
and PLW1514 preview clean; prose_check clean on both bases (it flagged
the re-dated measurement; tests point at the router's dating); `git diff
--check` clean; independent read-only review of the diff passed. PR
opened MERGEABLE at 2026-10-16T20:48:05Z (template followed: three
headings + three checkboxes, `Closes #775.`); **all 8 checks green at
20:52:53Z** (gate/scan/lint + test 3.11–3.15); Copilot bot COMMENTED; no
human review yet.
Availability gates held: #778/#776/#774 claimed by #781/#783/#785 during
screening, #775/#763 free, #775 chosen; re-verified live immediately
before publishing. Track 017.

**Discovery notes for this session** — screened the live state of all six
portfolio projects plus fresh search results (search API, topic pages):
libredb's best unassigned tasks (#1787/#1805) are short-window features or
already claimed; repowise fires many unassigned bugs daily but its
merge lane is broad yet impersonal; linux-vitals (real bugs, security
labels) worth a future look. No hidden exclusions were touched
(`lingdojo/kana-dojo` excluded on instruction; homelab-monitor
locale-sync competitor still active per the tracker's prior audit;
open-source-starter-lab only a lead).

**Also this session: tracker-sync honesty** — the tracker's documented
`update_tracker.py` needs the `gh` CLI, which is absent on this machine;
a REST shim (`~/bin/gh`) reproduces the two calls the script makes. The
run refreshed every entry's `lastVerified` to 2026-10-16T20:51:52Z and
updated remote-derived fields; three odysseus tracks flipped to
`ci-failed` because their live "Check PR description" checks fail on
GitHub (verified against the API, not inferred) — see Blockers.

**New this session (2026-10-14T17:53Z): markitdown #1897 / PR #2700** —
`Add --llm-client, --llm-model, and --llm-prompt options to the CLI`. The
gap maintainer afourney reaffirmed as "still wanted" on #175
(2026-09: "a fresh PR against `main` would be very welcome and will get a
much faster look"): the markitdown-ocr README documents a
`--llm-client openai --llm-model gpt-4o` command the CLI never defined.
Three argparse options, lazy `openai.OpenAI()` construction (openai stays
optional; missing package/key → one-line actionable error), pairing
validation, `**llm_kwargs` forwarded on all three `MarkItDown(...)`
constructor paths. Nine regression tests in `tests/test_cli_misc.py`, all
nine proven failing on unmodified `main`; focused file 29 passed, CLI
vector matrix 82 passed, black 23.7.0 and mypy clean on changed files;
speech-transcription failure proven pre-existing on base. PR opened
MERGEABLE; license/cla queued at 17:55Z; Copilot COMMENTED; no human
review yet. Competing-lane honesty: #2277 (CONFLICTING, stale since
2026-08-05) and #2422 (docs-only) are named in the PR body. Track 016.

**Also this session: markitdown #1784 / PR #2699 CLOSED-UNMERGED
(2026-10-14T17:10:55Z)** — the CSV-empty-warning patch from the previous
session was a duplicate: a fresh timeline sweep found PR #2675
(languor-daiduode, 2026-10-08) fixing the same lines with tests six days
earlier. Our PR (no tests, title-only body) was strictly dominated, so it
was closed with a courteous self-critical comment; branch preserved on the
fork; no maintainer pinged. The prior session's "0 cross-references" claim
was wrong — the issue timeline is the only reliable duplicate check. First
closed-unmerged track; `contributions/markitdown/issue-1784.md` and
`projects/markitdown.md` carry the post-mortem. Track 015.

**Also this session: backlot #633 MERGED 2026-10-14T08:06:47Z** — the
fourth merged backlot PR and the portfolio's seventh merge, caught by the
6-hourly tracker sync and recorded in `contributions-state.json`. Track
014's status lines below were reconciled with this fact.

**New this session (2026-10-12T09:30Z): backlot #603 / PR #633** —
`slack: a token query parameter is refused as invalid_auth, and a token
form field outranks the bearer header`. The two-part Slack auth
divergence the maintainer filed as #603: a non-empty `token` query
parameter authenticated (real answers `invalid_auth` — Slack closed the
query channel for apps created after February 24, 2021, and Backlot is
such an app), and the bearer header outranked the `token` form field
(real reads the form field first). `auth.slack_token` now reads
form-then-bearer and no longer touches the query; the new
`auth.slack_query_token_refused` is answered in `_caller_or_error`
before anything resolves, so a refused channel preempts even a valid
credential. Two new tests (13 refusal rows + 8 precedence rows) failed
on unmodified main and on a revert-proof against the final base
`94e79a0` (`2 failed`); replay of the issue's 19 rows over
`backlot.serve()`: main diverges on 11, the branch on 0. Full suite
6877 passed/10 skipped (junit 6887 events, 0 failures; all skips
import-gated and none Slack; `test_slack.py` 495 whole,
`test_sdk.py` 5 whole incl. the official slack_sdk); ruff clean (152
files); prose_check clean under CI's invocation (`--github HEAD^1`).
Rebased onto `94e79a0` with no conflicts (upstream's +11 commits
included merged #585 and #613 — no overlap). PR opened ready for
review, **CI 7/7 green on first push** (verified 09:28Z), MERGEABLE,
awaiting first human review. Not merged. Backlot open slot 2 of 3.
**Update: MERGED 2026-10-14T08:06:47Z — seventh merge (see the #633
MERGED entry above; Track 014 reconciled).**

**Also this session: #614 MERGED 2026-10-12T04:31:35Z** — `nuriyoo`
APPROVED at 04:31:31Z, four seconds before the squash merge (commit
`19d68c40`), on the response head `7abf5b4` with no further asks. The
portfolio's fourth merge and the second to carry a full human review
cycle (all four requested items). It freed the backlot slot Track 014
used.

**Also this session: isomorphic-git #2456 MERGED 2026-10-12T07:52:12Z**
— `jcubic` merged it directly (squash `c5916f4c`) with no formal
approval review, the portfolio's fifth merge and its first JS-library
track, ~13 hours from PR to merge. Caught by the tracker's GitHub sync
while preparing Track 014; this session's pre-creation rechecks had
covered the backlot issue only.

**New this session (2026-10-11T18:58Z): isomorphic-git #2286 / PR #2456** —
`feat(log): add author filter`, the portfolio's first JavaScript-library
track. `git.log()` gains an `author` option: a case-insensitive JS RegExp
over the author's `Name <email>`, applied before `depth` is counted,
composing with `filepath`, author-only (the issue thread conflates
author/committer — a dedicated test pins it), invalid regex rejects.
Four new tests; focused suite 14/14; full jest 1433 passed / 2 failed,
both the pre-existing `clone noTags` 30s-timeout flake proven identical
with and without the patch; eslint + tsc clean. Independent review
approve-with-nits, 7 items applied before commit. Selected after
screening ~34 repos / deep-verifying ~12 finalists — isomorphic-git
merges outside contributors fast (10 substantive merges in two weeks),
has a no-claim CONTRIBUTING, and pure-JS local testability (Node 22
toolchain required; system Node 26 breaks the `@zenfs/core` fixtures).
PR opened ready for review; MERGEABLE; `isomorphic-git-PR` check completed
**SUCCESS** (first-time-fork approval gate); CodeRabbit posted one
actionable comment (filepath+depth boundary), verified pre-existing and
replied to with evidence. **jcubic merged it 2026-10-12T07:52:12Z
(squash `c5916f4c`) with no formal approval review** — the portfolio's
fifth merge.

The thirteenth track is the first new project since the 2026-10-09
research; `projects/isomorphic-git.md` carries the full
policy/environment notes.

**New this session (2026-10-11T16:45Z): backlot #586 / PR #620** — the
`invalid_cursor`/`invalid_ts` precedence follow-up nuriyoo filed while
reviewing our merged #577. `conversations_history`'s three error guards
reordered to real's reading order (latest, oldest, cursor); one
parametrised test over the issue's 11 measured rows (8 fail on unmodified
main, all 11 pass with the fix); full suite 6346 passed/10 skipped; CI
7/7 green on first push, mergeStateStatus CLEAN. Opened ready for review,
awaiting `nuriyoo`/`khj809`. Not merged. This is the second open backlot
PR (policy allows three). **Update: MERGED 2026-10-12T10:45:03Z (squash
commit `4e7bb13f662abee8135231a9faba1d391d772181`) — the portfolio's sixth
merge; caught by the 6-hourly sync; Track 012 below reconciled.**

Five of the fourteen tracks have merged: backlot #577
(2026-10-10T13:59Z), libredb-studio #1628 (2026-10-11T00:34Z), repowise
#3338 (2026-10-11T07:56Z), backlot #614 (2026-10-12T04:31Z) and
isomorphic-git #2456 (2026-10-12T07:52Z). The seven odysseus PRs are
unchanged since 2026-10-09 (no new comments, no reviews, no state change).
**Reconciled 2026-10-14T20:30Z: seven of sixteen tracks merged — the five
above plus backlot #620 (2026-10-12T10:45Z) and backlot #633
(2026-10-14T08:06Z); eight open (the odysseus seven + markitdown #2700),
one closed-unmerged (#2699).**

**The eighth, backlot #614, got the portfolio's second human review today.**
`nuriyoo` requested changes at 2026-10-11T08:52:43Z, 20 minutes after the
PR opened, opening with "The change is right" and asking for four specific
items: a parametrised regression test (code supplied), two ACL-scoping
rows, a **Not in this PR.** line, and an inline comment wrap. Items 1-3
were pushed at 09:06Z (`9b1aad7`); item 4 was still outstanding and was
applied at 14:26Z (`7abf5b4`) along with a correction to a false causal
claim in our own description. CI 7/7 green on the response head; reply
posted 14:29Z; awaiting re-review at that sweep. **nuriyoo then APPROVED
at 2026-10-12T04:31:31Z and merged at 04:31:35Z (`19d68c40`) with no
further asks** — the portfolio's fourth merge, second human-reviewed.

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
CI: gitleaks FAIL — upstream history content, not our diff (see the
2026-10-17 audit); every other check passes (description/title/unmergeable,
pytest, compileall, CodeQL, analyze/linters, dependency-review).
Review: AWAITING_REVIEW
Notes: Target code still unfixed upstream (research_* still unguarded int()).
MERGEABLE; no rebase needed. 2026-10-17 root cause: the repo's secret-scan
workflow runs `gitleaks git .` over the PR merge-ref's full history and
finds 4 leaks inside upstream commit `dab660543b5b` ("chore(publication):
close pre-integration release blockers", author `alteixeira20`,
2026-10-05) — not authored here (this PR is a single commit, `35e3b298`);
removing it needs an upstream history rewrite or allowlist, a maintainer
action out of scope for this bugfix PR.
Attempt timeline (2026-10-17): attempt 1 of every `pull_request` workflow
on this head is `action_required` — the scan never ran at PR open
(2026-10-03). On 2026-10-15T23:53Z the maintainer-side approval re-ran the
whole fleet (attempt 2): ci.yml, CodeQL, container scans, dependency
review, workflow security ALL success — only Secret scan failed, in 24 s,
on 4 `generic-api-key` findings in upstream's own `THIRD_PARTY_PROVENANCE.json`
(lines 281/650/726/737; none in our diff). Upstream has no `.gitleaksignore`
on `dev` and the existing `.gitleaks.toml` `[[allowlists]]` do not cover
that file, so any re-run fails the same way. Gate for this PR is lifted
after the Oct 15 approval; the remaining item is that one allowlist/list
the maintainers own.
Next Action: Monitor PR for maintainer review; respond on same branch.

### Track 004
Project: odysseus-dev/odysseus
Issue: #6464
PR: #6475
Branch: fix/caldav-opencloud-token-spaces-6464
Status: MONITORING
CI: PASSING — description/title/unmergeable green, `ready for review`
label reapplied by the repo's checker. The 2026-10-03 `ci-failed` record
was a stale failure: the failing runs predate the 2026-10-09 body updates
that already satisfied the checker, and our tracker sync resolved duplicate
check names to the OLDEST run — both fixed 2026-10-17; the fresh re-run
after a factual Re-verification body edit is success (2026-10-16T21:17:36Z).
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
CI: PASSING — description/title/unmergeable green, `ready for review`
label in place. The 2026-10-03 `ci-failed` record was stale (failing runs
predate the body updates; sync tooling resolved duplicate check names to
the oldest run) — both fixed 2026-10-17; the fresh re-run after the
Re-verification body edit is success (2026-10-16T21:17:40Z).
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
Status: **MERGED 2026-10-12T04:31:35Z** (squash commit `19d68c40`) after
`nuriyoo` APPROVED at 04:31:31Z on the response head `7abf5b4`, with no
further asks — the portfolio's fourth merge and the second full human
review cycle.
CI: ALL GREEN on the response head 7abf5b4 — gate, lint, scan, test (3.11/
3.12/3.13/3.14), verified 14:31Z. Still no first-time-contributor
action_required gate (previous merged PR #577 lifted the one-open-PR cap;
up to three now permitted).
Review: **CHANGES_REQUESTED by nuriyoo 2026-10-11T08:52:43Z** — the second
human review cycle in this portfolio, 20 minutes after the PR opened. Opens
with "The change is right", then four items. Copilot's only entry is a
non-review (quota exhausted). **APPROVED by nuriyoo 2026-10-12T04:31:31Z**
on the response head, merged four seconds later; the review asked for
nothing beyond the four items, all delivered.
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
Next Action: None — merged 2026-10-12T04:31:35Z. Nothing owed on this
track; the fork branch `contrib/issue-610-s3-bucket-slash` can be deleted
whenever convenient.

### Track 012
Project: brekkylab/backlot
Issue: #586
PR: #620
Branch: contrib/issue-586-history-error-order
Status: **MERGED 2026-10-12T10:45:03Z** (squash commit
`4e7bb13f662abee8135231a9faba1d391d772181`) — the portfolio's sixth merge.
Opened 2026-10-11T16:45:32Z ready for review (never a draft). `nuriyoo`
reviewed 2026-10-12T04:17:07Z with a COMMENT review (measurement-backed,
three items + description note, explicitly not a request for changes); all
items applied and pushed (head `a3138ec`), evidence reply comment
`6121983174`; merged ~40 minutes after the last local verification of the
CLEAN state, caught by the 6-hourly sync (no formal approval recorded).
CI: 7/7 GREEN on the response head (gate, lint, scan, test 3.11/3.12/3.13/
3.14), mergeStateStatus CLEAN, MERGEABLE at base `c641b079`, verified
2026-10-12T10:03Z after merging main in `c4e18f5`. No action_required gate.
Review: copilot non-review (COMMENTED) + **nuriyoo COMMENTED
2026-10-12T04:17:07Z** — re-measured against slack.com/api that morning (54
requests; 43/49 refusals byte-for-byte at b9af620 vs 19 at main 0c87917;
"the reorder is right … no request where this head answers a timestamp or
cursor refusal differently from real"). Items: (1) fold the three refusal
tests into one 24-row table (15 one-argument controls + 9 order rows) with
the two old functions deleted, (2) move the order comment with the 2026-10-12
sentence, (3) keep #613's limit line with this order below it when merging
(that PR conflicted exactly where he predicted), plus description counts
→ nine/fifteen/twenty-four. All applied: suggestions verbatim (`a3138ec`),
main merged resolving per item 3 (`c4e18f5`), body updated, reply posted.
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
(#614 was the other until it merged 2026-10-12; #633 was the other after
that, until it merged 2026-10-14 — no open backlot PRs remain); policy
allows three after the first merge.
Next Action: None — merged. Backlot capacity fully restored: three open
PRs allowed, three slots free (re-verify claim-clean at selection).

### Track 013
Project: isomorphic-git/isomorphic-git
Issue: #2286
PR: #2456
Branch: feat/log-author-filter
Status: **MERGED 2026-10-12T07:52:12Z** (squash commit `c5916f4c`) by
`jcubic` directly, with no formal approval review on record. Opened
2026-10-11T18:58:36Z ready for review (never a draft) — the portfolio's
fifth merge and its first JS-library track, ~13 hours from PR to merge.
CI: `isomorphic-git-PR` **SUCCESS / COMPLETED** (plus CodeRabbit,
bundlewatch and security/snyk checks pass). The check ran to completion
once the first-time-fork workflows were approved; the repo has no
required-check branch protection, so it is informational, not a merge
gate. `mergeStateStatus` still reads BLOCKED only because the fork-workflow
approval gate has not been clicked by a maintainer — no check is red.
Review: CodeRabbit comment + Copilot COMMENTED review only; no formal
human review — `jcubic` merged the PR as-is the next morning.
Notes: First isomorphic-git track and the portfolio's first JS-library
track. Issue #2286 (filed 2026-02-14, 4 comments) asks for basic author
filtering on `log` "since it aims to be fully compatible with Git".
Selected 2026-10-11: OPEN, unassigned, 0 competing PRs (PR search for
2286 / "author flag" + cross-reference timeline all empty); re-verified
open / unassigned / 0 cross-references immediately before `gh pr create`.
No claim protocol in this repo (fork + branch + PR; CONTRIBUTING's only
first-timer requirement is `npm run add-contributor`, shipped as its own
commit 3fd4ab1e, same as merged PRs #2385/#2449). Implementation:
`src/commands/log.js` compiles `authorRegex` once per call and guards the
single `pushCommit` choke point that all seven commit-emission sites
route through (so merge/shallow/filepath paths cannot leak); `src/api/log.js`
documents the param. Semantics: case-insensitive JS RegExp over the
author's `Name <email>`; applied before `depth` (like
`git log --author --max-count`); composes with `filepath`; filters on
author not committer; invalid regex rejects. One deliberate git
divergence, disclosed in JSDoc + PR body: git's `--author` is
case-sensitive BRE, this is a JS RegExp with the `i` flag (independent
reviewer verified git's actual behavior against git 2.56 before the
claim was reworded). Four new tests (name/email filter + case
insensitivity + regex metacharacters + no-match `[]` + invalid regex;
depth counts matching commits; filepath combination; author != committer).
Verification on the Node 22.22.0 toolchain (system Node 26 breaks the
repo-wide `@zenfs/core` fixtures): focused test-log.js 14/14; TDD proof
by stashing src/ (new tests fail); full jest --ci 1433 passed / 2 failed,
both the pre-existing `clone › clone with noTags` 30s-timeout flake in
test-clone.js + test-clone-in-submodule.js, reproduced with and without
the patch (27-28s pass, 30s fail); eslint clean; tsc clean, index.d.ts
picks up the param. Independent read-only review approve-with-nits; 7
items applied pre-commit (dropped the false git-parity claim from the
JSDoc, repo-wide `@param [args.author]` style, `author: null` =
no-filter, explicit boolean, comment fix, tighter regex assertion, added
the author-vs-committer test). Appendix A submodule mirror deliberately
omitted (that file is behind main; #2385/#2413 skipped it) — offer
stated in the PR body. Diff: 5 files +216/-9.
Next Action: None — merged 2026-10-12T07:52:12Z. Nothing owed on this
track.

### Track 014
Project: brekkylab/backlot
Issue: #603
PR: #633
Branch: contrib/issue-603-query-token-form-precedence
Status: **MERGED 2026-10-14T08:06:47Z by nuriyoo** (squash
`0288cc807735f0fe97be40d50c240067b3091cd3`) — portfolio seventh merge,
caught by the 2026-10-14 tracker sync. At open it was CI 7/7 green on the
first push (2026-10-12T09:28Z) and MERGEABLE.
CI: All seven checks passed on head `5aaea3b`, verified 09:28:02Z; no
first-time-contributor gate (PR #577 lifted it). Local numbers CI agrees
with: full suite 6877 passed/10 skipped on Python 3.11.17.
Review: None recorded at merge (no formal review; nuriyoo merged directly).
Notes: Fourth backlot track, taken the morning after #614 merged (the
merge freed this slot; backlot allows three open PRs after the first
merge). Selection gate run twice: issue OPEN, unassigned, 0 comments, no
cross-referenced PR at 08:28Z and again immediately before `gh pr create`
at 09:22Z. The issue's two divergences, both silent: (1) a non-empty
`token` query parameter authenticates where real answers `invalid_auth`
— measured over auth.test GET+POST, conversations.list, users.list and
search.messages with a bearer header or a form token beside it; Slack's
changelog closed the query channel for apps created after February 24,
2021 and Backlot's fixture app dates from 2026; (2) the bearer header
outranks the `token` form field where real reads the form field first.
Fix: `auth.slack_token` reads form-then-bearer and drops the query; new
`auth.slack_query_token_refused` refuses a non-empty query token
whatever else the request carries and an empty one beside a bearer
header (empty-alone stays `not_authed`), answered in `_caller_or_error`
before resolution so refusal preempts a valid credential elsewhere;
`_caller_or_error`'s table and `docs/auth.md` move with the rule. Two
unmeasured combos (empty `token=` beside form-only; multiple `token`
params) deliberately left unpinned and disclosed as **Not in this PR.**
TDD: the two new tests (13 refusal rows, 8 precedence rows) failed on
unmodified main; revert-proof on the final base `94e79a0` reproduced
`2 failed`. Replay of all 19 issue rows over `backlot.serve()`:
main@94e79a0 diverges on 11, this branch on 0. Full suite 6877
passed/10 skipped (junit: 6887 events, 0 failures; skips = mcp 1,
mirage 2, gdrive_fsspec 6, hubspot reader 1, none Slack;
`tests/test_slack.py` 495 whole; `tests/test_sdk.py` 5 whole incl. the
official slack_sdk against `backlot.serve()`); ruff check/format clean
(152 files); prose_check clean under CI's exact invocation
(`--github HEAD^1`) — with the script's default base the fork's
`origin/main` trails upstream and the range swallows main's pre-existing
`test_google.py:6355`/`test_s3.py:338` findings, verified pre-existing on
a clean `94e79a0` worktree. Rebase onto `94e79a0` was conflict-free
(upstream's +11 commits included merged #585 auth.test member reorder and
#613 number validation — no overlap with this diff; #585's reorder was
why the identity tests assert `user_id` only). PR body follows the
merged-#577/#614 template: `Closes #603`, three headings, three
checkboxes (ACL box unchecked with the no-new-endpoint note, as #577
did), replay table, AI-assistance disclosure.
Next Action: None — merged 2026-10-14T08:06:47Z. All four merged backlot
PRs (#577, #614, #620, #633) are closed chapters.

### Track 015
Project: microsoft/markitdown
Issue: #1784
PR: #2699
Branch: contrib/issue-1784-csv-empty-warning
Status: **CLOSED-UNMERGED 2026-10-14T17:10:55Z (duplicate of #2675)**.
Opened 2026-10-14T15:25:04Z by the previous session; closed by us ~1h45m
later. Issue #1784 remains OPEN.
CI: license/cla passed on #2699; no other checks ran before closure.
Review: Only a Copilot COMMENTED bot review; no human review, ever.
Notes: The previous session's report claimed "0 cross-references" for
#1784 — false. The issue timeline shows PR #2675 (languor-daiduode,
opened 2026-10-08T14:47:38Z, still OPEN) fixing the exact same
`if not rows:` branch in `_csv_converter.py` with `pytest.warns`
regression tests, a full PR body, and a passing license/cla. Our patch
was the same one-line warning without tests and a title-only body —
strictly dominated. Closed with a courteous comment owning the oversight
and noting the branch is preserved; nothing merged, no maintainer pinged,
no issue comment posted. Post-mortem in
`contributions/markitdown/issue-1784.md`; the lesson (timeline
cross-reference sweep is the only reliable duplicate check) is written
into `projects/markitdown.md` §Pitfalls.
Next Action: None. Only revisit the lane if #2675 closes unmerged; then
reopen the branch with tests added first.

### Track 016
Project: microsoft/markitdown
Issue: #1897
PR: #2700
Branch: contrib/issue-1897-cli-llm-options
Status: **OPEN — awaiting first human review** (opened
2026-10-14T17:53:21Z; MERGEABLE; `mergeStateStatus: BLOCKED` = review +
required checks pending, normal for a fresh PR). Not merged.
CI: license/cla QUEUED/pending at 17:55:39Z; Copilot COMMENTED bot
review only. No green-CI claim until it reports.
Review: None human yet. Do not ping.
Notes: Sixteenth track, first markitdown survivor. Maintainer-confirmed
task: afourney (MEMBER) called the `--llm-*` CLI gap "still wanted" and
invited "a fresh PR against `main`" on 2026-09-03 (#175); prior attempts
#1898/#1908 were self-closed by their authors, never rejected. Lane
competition, disclosed in the PR body: #2277 (CONFLICTING, stale since
2026-08-05) and #2422 (docs-only alternative). Implementation:
`--llm-client {openai}`/`--llm-model`/`--llm-prompt`, pairing validation
through `_exit_with_error`, lazy `_create_llm_client()` (missing openai
package or OPENAI_API_KEY → one-line actionable error), `**llm_kwargs`
forwarded on the default/DocIntel/CU constructor paths. Commit
`48d0f1164cb28c4620f1d59757d96befc3f66256` (2 files, +253/−3). Nine new
tests in `tests/test_cli_misc.py`, all proven failing on unmodified
`main` (9 failed) and passing with the fix (29 passed); CLI vector matrix
82 passed; black 23.7.0 clean; mypy clean on changed files (28 pre-existing
errors elsewhere); `test_speech_transcription` failure proven pre-existing
on base. Base `4cc9fa1` verified unchanged immediately before publication;
issue re-verified OPEN/unassigned with no new competing PR.
Next Action: Watch PR #2700 for license/cla result and first human
review; respond on the same branch if requested. If review requests the
OpenAI-compatible `base_url` option, that is a small additive follow-up.

### Track 017
Project: brekkylab/backlot
Issue: #775
PR: #786
Branch: jira-comment-orderby-java-trim
Status: **OPEN — review response pushed, awaiting nuriyoo's re-review**
(opened 2026-10-16T20:48:05Z; rebased onto `main` @ `e9b9d72` and
reworked 2026-10-17T20:16Z; head `27e8922f62f6`, 2 commits; MERGEABLE;
`mergeable_state: clean`). Not merged.
CI: all 9 check-runs green on the reworked head by 2026-10-17T20:21:55Z
(gate/lint/scan + test 3.11–3.15); bare `test` job is the workflow's
skipped shape. Copilot bot COMMENTED (a bot, not a review).
Review: **`nuriyoo` COMMENTED 2026-10-17T10:47:21Z — four change requests
with code suggestions** (3 inline comments), from a fresh 65-spelling
Jira Cloud measurement: (1) the strip after the direction sigil is *not*
a second `String.trim` — `-%01created` is a 400 naming `\x01created`
where the inner `_JAVA_TRIMMED` strip served 200, while
`%20`/`%09`/`%0A`/`%0B`/`%0C`/`%0D` after the sigil do go; (2) a line
terminator behaves in two ways — one at the end goes (`created%C2%85` is
200), one anywhere else makes real name the value whole, sigil and all;
(3) the refused rows should assert the field real named (12 measured
rows offered); (4) all 65 answers fit Java's `^([+-]?)\s*(.*)$` under
`find`, with a ready pattern to paste beside `_JIRA_ORDER_FIELD`.
**All four applied in `27e8922f` (suggestions verbatim); reply comment
`6240438402` posted 2026-10-17T20:22:46Z; the PR was renamed to "jira: a
comment read reads orderBy as Java reads it, so a no-break space is
refused and U+0001 is served" (both of its examples still hold under the
new reading).**
Notes: Seventeenth track, fifth backlot contribution. Issue filed
2026-10-16 by `nuriyoo` from their Jira Cloud measurement: a comment
read's `orderBy` was stripped with Python's `str.strip()` (NBSP/em space
lifted off, U+0001 kept), real trims as Java's `String.trim` (chars
≤ U+0020 only). The first cut (commit `166bb7a`, rebased to `e1a0f3a`)
applied `_JAVA_TRIMMED` twice — outer trim, sigil, inner trim, matching
`project/search` (#762)'s order — and the review disproved the inner
trim: the comment read *reads* the value with `_JIRA_ORDER` (the
reviewer's pattern, pasted below `_JIRA_ORDER_FIELD`, matched with
`.match` so `^` holds only at the start). Final tables: 7 `takes` rows,
12 `refuses` rows each asserting the field real's 400 named. Full suite
on the rebased branch **7872 passed/38 skipped** on `.[dev]` Python
3.14.8 under `PYTHONWARNDEFAULTENCODING=1`; collect-only delta vs the
base is +16 = exactly the 7 takes + 9 refuses rows (the base itself
gained +176 tests in the #782 rebase, which is why the absolute count
moved); ruff lint/format + PLW1514 preview + prose_check
(`upstream/main`) + `git diff --check` clean. Lane check at screening:
#778/#776/#774 claimed by #781/#783/#785; #775/#763 free; #775 chosen
(acceptance clarity, dev-covered test file); issue re-verified
open/unassigned/0-comments at publication. Commits
`e1a0f3a31b094047fe3d61daac63e268450ce924` +
`27e8922f62f6345948c563db2dc8d75f980b3215` (2 files, +49/−9 vs base).
Next Action: Await `nuriyoo`'s re-review or merge; respond on the same
branch if anything further is asked. No ping. No second new PR in
backlot during this execution (one-contribution rule; two open now, the
after-first-merge limit is three).

### Track 018
Project: brekkylab/backlot
Issue: #779
PR: #806
Branch: slack-history-latest-exclusive
Status: **OPEN — awaiting first human review** (opened
2026-10-17T18:19:47Z; MERGEABLE; `mergeable_state: clean` once the matrix
finished at ~18:25Z; base `main` @ `e9b9d72` verified current at
publication and still the tip). Not merged.
CI: all 9 check-runs completed by 2026-10-17T18:24:59Z — gate/lint/scan
success and test (3.11)–(3.15) all success; bare `test` is the workflow's
skipped shape. Copilot bot COMMENTED (a bot review, not a human one).
Review: None human yet. nuriyoo/khj809 are the historical reviewers here
(4 merges in this portfolio, all reviewed). Do not ping; the PR is the
reply.
Notes: Eighteenth track, sixth backlot contribution. Issue filed
2026-10-16 by `nuriyoo` while reviewing the merged #767: the `oldest`
bound was exclusive unless `inclusive`, the `latest` bound kept equality.
`_in_window` now reads `ts_us > hi_us if inclusive else ts_us >= hi_us`,
so a message at `latest` is left out, the same ts on both bounds alone
only with `inclusive`, and a bound a microsecond either side behaves as
real does. One parametrized test encodes the issue's nine slack.com/api
rows (2026-10-16) over HTTP on the `paged_slack` corpus; with the router
at its base revision the `latest=T` row fails and the other eight pass on
both revisions. Full suite 7865 passed/38 skipped on `.[dev]` Python
3.14.8 under `PYTHONWARNDEFAULTENCODING=1`; ruff lint/format + PLW1514
preview + prose_check (upstream/main) + `git diff --check` clean;
independent read-only review verified all nine rows mechanically and
found no defect (two prose nits applied). Lane check at screening
(2026-10-17): #796/#794/#778/#776/#774 already claimed by open PRs,
#792/#763/#749/#779 free; #779 chosen (measured acceptance contract,
dev-covered test file, handler already known from #577/#620). Availability
re-verified to the minute before publishing (AGENTS.md's two commands:
no assignees, empty `closedByPullRequestsReferences`; plus no open PR
naming it). Commit `8b042783e3b872d97ff212a9735a7071401bc6df`
(2 files, +83/−2).
Next Action: Watch PR #806 for the first human review; respond on the
same branch if changes are requested. (#786's waiting review was
answered the same day — see Track 017 — so both backlot PRs are now
wait-only.)

### Track 019
Project: brekkylab/backlot
Issue: #831
PR: #851
Branch: contrib/issue-831-gmail-quoted-address-value
Status: **OPEN — awaiting first human review** (opened
2026-10-19T12:01:53Z; mergeable, `mergeable_state: clean`; base `main`
@ `ff92bdd` verified current at publication; head
`cbe2c61e4861da3654934507b3a1f24866436685` verified by `ls-remote`
before the PR). Not merged.
CI: 9/9 check-runs green — gate/lint/scan success and test
(3.11)–(3.15) all success; bare `test` is the workflow's skipped shape.
Copilot bot COMMENTED (a bot review, not a human one).
Review: None human yet. `nuriyoo`/`khj809` are the historical reviewers
(#806's merge came from `nuriyoo` at 2026-10-19T06:34Z). Do not ping;
the PR is the reply.
Notes: Nineteenth track, seventh backlot contribution. Issue filed
2026-10-19T06:02Z by `nuriyoo` while reviewing merged #805: a quoted
address value with a `-` in it was read as if unquoted, so
`from:"no-reply"` matched `noreply@shop.example` where gmail answers
none (their 603-message matrix, eight words, four operators, 2026-10-19).
`_take` keeps address-value quotes, `_gmail_address_match` reads a
quoted value's words alone (quote pair stripped before the
exact-address path; joined alternative gated on `not quoted`), and the
`me` substitution compares through quotes — `subject:`/`label:`/`in:`/
`has:` parsing byte-identical, lone `"` (#828's separate divergence)
and `from:""` on their old paths. Six new rows over both listings plus
three parse pins; regression proven by stashing the router (10/12 new
rows fail, control passes) and independently by a read-only review
agent's scratch-copy mutation run. Full suite **11034 passed/3 skipped**
on `.[all]` Python 3.14.8 (skips: Docker, npx, llama_index reader —
environmental, none gmail); `PYTHONWARNDEFAULTENCODING=1` 8184
passed/38 skipped on the earlier `.[dev]` install; ruff lint/format +
PLW1514 preview clean; prose_check exit 1 on four findings
byte-identical to clean `main`; `git diff --check` clean. Review found
no critical/major issue; two wording nits applied pre-commit. Lane check
(2026-10-19): same-day claim pressure proved again — #843→PR #848,
#842→PR #836 within hours; the gmail trio #828/#831/#834 was free at
screening and #831 stayed free to the minute of `POST /pulls` (0 open
PRs naming it, 0 assignees, timeline only merged #805). Alternatives
scored down with cause in the state `notes` (repowise 193 open PRs +
same-day claims; odysseus 343 + our #6648 untouched 10 days; kestra
assign-first + single-contributor lane; batpred clique merges;
markitdown frozen since 2026-10-04). Workspace: isolated worktree
`~/opensource-work/backlot-831` (the `~/opensource-work/backlot`
checkout's uncommitted #792 confluence work was left untouched). PR
followed the template: three headings, three checkboxes, `Closes #831.`,
`gmail:` title prefix, no issue number in comments (prose gate).
Next Action: Watch PR #851 for the first human review; respond on the
same branch if changes are requested. Do not open another backlot PR
while #851 is open unless a genuinely distinct task justifies it (the
post-first-merge limit is three; this is one of one active).

### Track 020
Project: Kludex/starlette
Issue: — (anchor: discussion #2738, not an issue)
PR: #3682
Branch: fix/405-allow-multiple-routes
Status: **OPEN — 11/11 checks green, awaiting first human review**
(opened 2026-10-19T13:17:51Z; mergeable, `mergeable_state: clean` at
2026-10-19T13:44:48Z; base `main` @ `dc20b216f065af3a487722141da9a29dcac388d1`
verified current at publication; head `9fb409771097e7eed3fb1cebddad9694b34808b2`,
2 commits, on the `ShahabAhmed01/starlette` fork; 3 files, +93/−9).
Not merged.
CI: check, zizmor (x2), Python 3.11–3.15, Run benchmarks and the cubic
AI reviewer all success; Docs preview (Cloudflare) skipped (workflow
shape). codspeed bot comment: "Merging this PR will not alter
performance". 11/11 check-runs completed on `9fb4097`.
Review: None human yet. `Kludex` is the historical reviewer/merger of
external PRs here (#3542, #3585, #3622, #3631, #3654). Copilot was
quota-limited and posted no content; cubic's P2 (a custom `BaseRoute`
partial match with no `methods` would be bypassed) was valid, fixed in
`9fb4097` with the guard plus `test_router_405_keeps_custom_route_
handling`, and answered in-thread (comment `4314473754`). Do not ping;
the PR is the reply.
Notes: Twentieth track, first starlette contribution. No issue was
filed — the anchor is discussion #2738 (2024-10-25T12:12Z, `ccrims0n`,
category *Potential Issue*) reporting exactly this bug: three routes on
one path answer a 405 with only the first route's `Allow`. `Kludex`
replied "Seems valid." two minutes later; it sat unfixed for two years
and no PR ever referenced it (corpus greps for `2738`, `discussions/2738`,
`first route`, `GET, PUT, DELETE` → 0 among 3007 items), so the
discussion doubles as the PR template's required prior discussion.
AI_POLICY.md honored: open+closed PRs, issues and **discussions**
searched before opening (duplicates ban); discussions paginated in full
(622). Selection evidence: rejected hard-gated repos (hono, zod, vitest,
pydantic — assign/auto-close; pytest — drive-by agentic PRs rejected;
eslint — OpenJS CLA; express/fastify — bug swarms; claude-mem — volatile)
and killed duplicate candidates (#3604 mixed byte ranges, #3495
Accept-Encoding, #3638 IPv6 brackets, query-param swarm
#3661/#3636/#3571/#3554/#3553, authority swarm #3579→#3671 — all closed
unmerged). Repro on `main` @ `dc20b21`: bare `Router`, `Starlette` app
and distinct patterns `/items` + `/{name}` all answered `HEAD, GET`
with `POST` missing (RFC 9110 §10.2.1 / §15.5.17). Fix: collect every
`Match.PARTIAL` route; when more than one matches, render the sorted
union in `Router` (`HTTPException` when `"app" in scope`, else
`PlainTextResponse`), **only** when every match exposes a non-empty
`methods` — otherwise first-match `handle()` runs unchanged (custom
routes safe); `Route.handle` joins `sorted(self.methods)`; new
`docs/routing.md` paragraph; `docs/release-notes.md` untouched
("Releasing" section is maintainer-owned; merged #3585/#3640 did not
touch it). Verification: **1400 passed / 2 skipped / 2 xfailed**;
`scripts/coverage` 100% branch (fail-under=100; tests count as source);
`scripts/check` clean (ruff format, mypy --strict, ruff check);
`zensical build --clean` clean. PR follows the template (three
headings, three boxes ticked truthfully), links discussion #2738 and
discloses AI assistance; body notes the in-flight neighbours #3665
(`==`→`is` in the same loop) and owner #3339 (trie rewrite — patch
fetched, keeps first-partial dispatch, not a duplicate) with an offer to
rebase. Workspace: isolated `~/opensource-work/starlette` clone; fork
created this session; pushed via askpass so no token entered argv;
tracker/backlot and other workspaces untouched until publication.
Live verification at 13:44:48Z: open, not draft, mergeable clean, 0
human comments, reviews = two bots + my threaded reply.
Next Action: Watch PR #3682 for the first human review; respond on the
same branch if changes are requested. Do not open another starlette PR
while #3682 is open. Before any future starlette work, re-run the
corpus + discussion duplicate sweep (AI policy: duplicates ban).

### Track 021
Project: Kludex/uvicorn
Issue: — (anchor: discussion #3108, not an issue)
PR: #3215
Branch: fix/shutdown-h11-error-state
Status: **OPEN — 26/27 checks green (docs-preview skipped, fork PR), one BOT
approval, awaiting first human review** (opened 2026-10-19T17:24:52Z;
mergeable, `mergeable_state: clean` at 2026-10-19T20:38:44Z; base `main` @
`cc6fea5b40ad559f7ca358a24b1a521451232281` verified current at publication;
head `c8eb28cdaaf78c74cdf987736bbdb262aa4aa4d2`, 3 commits, on the
`ShahabAhmed01/uvicorn` fork; 3 files, +94/−2). Not merged.
CI: check, zizmor (x2), Run benchmarks, CodSpeed Performance Analysis, cubic
AI reviewer, and Python 3.11–3.15 + free-threaded 3.14t/3.15t across
ubuntu/macos/windows all success — 26 of 27 check-runs; `docs-preview`
skipped because that job only runs for same-repo heads (docs built locally:
`uv run zensical build --clean` → "No issues found"). Commit status
`CodeRabbit` success at 17:51:48Z (CodeRabbit reports as a *status*, so
`mergeable_state` reads `unstable` while it runs and `clean` after).
codspeed bot comment: "Merging this PR will not alter performance". 27/27
check-runs completed on `c8eb28c`, none failing.
Review: No human yet. `Kludex` is the historical reviewer/merger of external
PRs here (#3184, #3195, #3092, #3209). Copilot was quota-limited and posted
no content; cubic found nothing in the fix commit, then raised two P3s on the
new docs sentence (close stated for in-flight responses too; "closing
handshake" implying a peer exchange `h11.ConnectionClosed()` never performs)
— both valid, both fixed in `c8eb28c`, answered in-thread (replies
`4316934181`, `4316934555`), after which cubic dropped the first finding;
`coderabbitai[bot]` commented a walk-through then `APPROVED` at 17:51:44Z —
**a bot approval, not a maintainer's**, so the ledger status "ready-to-merge"
means automated approval + green CI, never maintainer sign-off. Do not ping;
the PR is the reply.
Notes: Twenty-first track, first uvicorn contribution. No issue was filed —
the anchor is discussion #3108 (2026-08-29T13:25:39Z, `kazuki-ma`, category
*Potential Issue*) reporting that `H11Protocol.shutdown()` sends
`h11.ConnectionClosed()` with no `our_state` guard while `connection_lost()`
guards it twice, so one connection in h11 `ERROR` raises `LocalProtocolError`
out of `Server.shutdown()`'s loop and strands every later connection;
`amasen02` confirmed it 2026-09-05 and proposed the patch; no PR ever
referenced it. The discussion doubles as the PR template's required prior
discussion. AI_POLICY.md honored: open+closed PRs, issues and **discussions**
searched before writing code (duplicates ban); hard-gated repos rejected
(hono, zod, vitest, pydantic, pytest, eslint, express, fastify, claude-mem),
Pallets/yt-dlp/textual/fastapi rejected on AI policy, trending proved
star-farmed; other candidates dropped (#3183 author drafting own patch,
#3093 unreproducible, #3098 needs a PySocks dep, and claimed items
#3164/#3052/#3109/#3153/#3071/#3165/#3175/#3188/#3213). Repro on `main` @
`cc6fea5`: short body under `content-length: 10` → `our_state = ERROR` with
the transport still open → `Server.shutdown()` raised `Can't send data when
our state is ERROR`. Fix: guard the handshake with
`if self.conn.our_state != h11.ERROR:` and still `transport.close()`; the
commenter's `try/except` layers were deliberately **not** taken (unreachable
after the guard, and uvicorn's line coverage gate of `fail_under = 100` over
`uvicorn` **and** `tests` fails on dead lines), and a server-wide
`try/except` around the shutdown loop would swallow unexpected errors.
Verification: two regression tests fail without the fix (2 failed/6 passed)
and pass with it (8 passed); **1378 passed / 13 skipped**; `./scripts/coverage`
**100.00%** (8774 statements, 0 missed); `./scripts/check` clean (ruff
format, mypy, ruff check); `zensical build --clean` clean. PR follows the
template (three boxes ticked truthfully — the docs box because
`docs/server-behavior.md` gained the shutdown sentence), links discussion
#3108, records the duplicate search, discloses AI assistance. Workspace:
isolated `~/opensource-work/uvicorn` clone; fork created this session via
`POST /repos/Kludex/uvicorn/forks`; pushed via askpass so no token entered
argv; the `uv.lock` churn this machine's uv version causes was reverted
before every commit; tracker and other workspaces untouched until
publication. Live verification at 2026-10-19T20:38:44Z: open, not draft,
mergeable clean, 3 commits, 2 issue comments (codspeed, coderabbit), 4 review
comments (2 cubic + 2 mine), 6 reviews (copilot, cubic x2, mine x2, coderabbit
APPROVED), 0 human comments.
Next Action: Watch PR #3215 for the first human review; respond on the same
branch if changes are requested. Do not open another uvicorn PR while #3215
is open. Before any future uvicorn work, re-run the corpus + discussion
duplicate sweep (AI policy: duplicates ban) — and re-read `AI_POLICY.md`,
which changes acceptance behaviour more often than the issue queue does.

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

## Portfolio sweep 2026-10-11T19:35Z (all 13 contributions, "is everything ok from my side")

Every one of the 13 tracked contributions was re-verified against live
GitHub. Method: `gh pr view` for state/mergeability, `commits` for heads,
`commits/{sha}/check-runs` scoped to each PR's **current head SHA** (and
collapsed to the **latest run per check name**, because the raw endpoint
returns superseded historical runs too), `pulls/{n}/comments` and
`issues/{n}/comments` for anything needing a reply, plus a full
`commits/{sha}` existence probe for every recorded SHA in the state file.

**Nothing is blocked on us. No unanswered reviews, no unanswered maintainer
questions, no failing checks, no conflicts.** Specifically:

- **3 merged PRs still merged**, merge commits unchanged (backlot #577
  `78c06e50d2`, libredb-studio #1628 `ca7755b0cf`, repowise #3338
  `41bf297d57`).
- **10 open PRs: all OPEN, all MERGEABLE, none a draft, all on the correct
  base.** Latest check run per check name is green on every one.
  (The apparent red on #6475/#6476 was superseded 2026-10-03 runs of
  `Check PR description`; the latest runs, 2026-10-11T15:03Z, are SUCCESS.)
- **All 10 linked issues still OPEN** (none solved by someone else; no
  competing PR merged).
- **Every recorded commit SHA in the state file exists as a real object on
  GitHub** (13/13 contributions, 0 mismatches). The one defect found and
  fixed: isomorphic-git #2456's `commits` array was in preference order
  rather than GitHub's chronological order; corrected to
  `3fd4ab1e` (contributor) then `9cbc0feb` (feature).

**isomorphic-git #2456 — CI completed green** (`isomorphic-git-PR`
SUCCESS, plus CodeRabbit / bundlewatch / security-snyk checks pass) and
CodeRabbit posted one actionable comment: the `filepath`+`depth` boundary
can return `depth+1` when the boundary commit matches the author. Verified
empirically as **pre-existing and unchanged by this patch**: on unmodified
upstream main `909b97b1` (`authorRegex` absent), `log({filepath:'a.txt',
depth:1})` already returns 2 commits — byte-identical to this branch — and
the `author` filter sits in the single `pushCommit` choke point, so it can
only *remove* commits, never add one. Declined CodeRabbit's proposed
`endCommit` guard because it would change existing `filepath`+`depth`
semantics for **all** callers (`depth:1 → 2` becomes `depth:1 → 1`), a
behavior change out of scope for an author-filter feature. Evidence-based
reply posted 19:26Z (comment `4242897410`), offering a separate
follow-up issue/PR if maintainers prefer the strict bound.

**One item needs a human decision, deliberately not actioned:** `cevheri`'s
unanswered question on libredb issue #1411 ("how was first-contribute on
libredb studio / which databases are you using") requires the account
owner's personal context (which databases they actually use). It was **not**
answered with fabricated specifics. A short factual reply about the
contribution workflow (claim-by-comment, fast merge) is safe to send;
the "which databases" half needs real input first.

**Waiting on maintainers, not on us:** the odysseus seven have had zero
human review for 3 days behind the `action_required` first-time-contributor
gate; backlot #614 awaits `nuriyoo`'s re-review (all four requested items
addressed, reply posted 14:29Z); backlot #620 and isomorphic-git #2456
await first review. Per policy, no pings.

## Merge-readiness audit 2026-10-14T19:54–20:26Z (all 8 open PRs, "make sure they get merged")

Requested review of every outstanding contribution. Method: live `gh` state
per PR (state/mergeable/mergeStateStatus/head/reviewDecision), check-runs
collapsed to latest per name, commit statuses, reviews + issue comments +
inline review comments, linked-issue state and timelines, then a **fresh
local merge of every branch against current upstream `dev`** and a test run
of each merged result in an isolated Python 3.11 venv (`uv`, full
`requirements-dev.txt`), on throwaway `audit-*` branches in a disposable
worktree. Nothing was pushed; all seven original branches were re-verified
byte-identical to their remote PR heads afterwards.

**Result: all 8 PRs are OPEN, non-draft, MERGEABLE, with zero failing
checks, zero conflicts, zero unanswered feedback, and every branch proven
green against today's base. Nothing is fixable from our side.**

- **The 7 odysseus PRs (#6453, #6472, #6473, #6475, #6476, #6647, #6648)**
  show `mergeStateStatus: UNSTABLE` purely from the first-time-contributor
  gate: combined commit status `pending` with **zero** listed statuses, the
  only check-runs being the three green meta-checks (PR description,
  Conventional Commits title, flag-unmergeable). No human reviews, no
  comments, no inline review comments on any of the seven — only Copilot
  `COMMENTED` reviews. All 7 linked issues still OPEN; bugs confirmed still
  present on current `dev` (e.g. `sqlalchemy.ext.declarative` import still
  at `core/database.py:11`; `max_tokens=512` still hardcoded at
  `routes/calendar_routes.py:1873`), so none has been superseded.
- **`dev` moved under us**: head is now `c3819e3` (2026-10-14T11:20:35Z,
  including #6704's pytest-baseline restore), while the local clone's
  `origin` is the fork — always fetch `upstream` for the true base.
  `git merge-tree --write-tree upstream/dev <branch>`: **CLEAN-MERGE on all
  7**. Baseline on pure `dev`: 216 passed (1 warning = the MovedIn20Warning
  #6453 exists to remove).
- **Merged-result test runs (all green):** #6453 warning count 0 after
  merge + 178 passed; #6472 7 passed; #6473 13 passed; #6475 13 passed;
  #6476 38 passed; #6647 47 passed (incl. re-verified ordering: notes-read
  rows 123–125 precede the `ui` row 137, so first-match-wins routes
  correctly); #6648 2 passed (node present). **298 tests passing across the
  seven merged results.** Each diff also re-read line-by-line against
  current `dev` semantics; no changes warranted.
- **Odysseus is actively merging outside PRs** (e.g. #6704, #6701, #6693,
  #6683, #6643 merged 2026-10-13; #6633, #6610 merged 2026-10-14), ~100
  open PRs in the queue — our seven (5–12 days old) are simply waiting in
  line behind review attention, not blocked by anything of ours. Per
  policy: no pings.
- **markitdown #2700**: MERGEABLE, `mergeStateStatus: BLOCKED` (CLA +
  required review); `license/cla` still queued at 20:26Z (~2.5h,
  first-time-contributor queue); only policy-bot comments; Copilot declined
  (reviewer quota). Nothing actionable.

**Honest boundary:** merges require maintainer action. Everything a
contributor can legitimately do — mergeability, CI-equivalent local proof,
review-quality diffs, no unanswered feedback, no duplicate lanes — is done.
No gate was bypassed, no maintainer was pinged, no commit was pushed.

## Mergeability audit 2026-10-17 ("fully perfect from my side", all 17)

(Superseded by the 2026-10-17T19:40Z audit above — all 18 records,
post-#786-rework; kept for the record.)

Method: every record re-verified against the live GitHub API — merged
PRs' merge-commit SHAs vs recorded, open PRs' mergeable/mergeable_state,
the NEWEST conclusion of every check-run name, human reviews and comments,
fork branch tips vs PR heads, linked-issue states, competing-PR states —
plus a local re-implementation of odysseus' `check-pr-description.js`
rules run against the two flagged PR bodies.

- **7 merged PRs re-verified; every live merge commit matches the recorded
  SHA exactly** (backlot #577 `78c06e50d256`, #614 `19d68c40e61c`,
  #620 `4e7bb13f662a`, #633 `0288cc807735`; libredb-studio #1628
  `ca7755b0cff3`; repowise #3338 `41bf297d57a4`; isomorphic-git #2456
  `c5916f4ce474`).
- **backlot #786 (Track 017)**: mergeable_state=clean at audit time; 8
  success + the workflow-shape skip. **Superseded later that day**: at
  10:47:21Z nuriyoo's human review landed (COMMENTED, four change
  requests — see Track 017), so the "no human review yet" reading and the
  `clean` state no longer hold: the PR is now `behind` (base advanced via
  #782) and awaits our rework.
- **odysseus 7 PRs (#6453/#6472/#6473/#6475/#6476/#6647/#6648)**: all fork
  branch tips byte-match the live PR heads; all 7 linked issues still
  open; every PR-level check green after today's fix below; competing
  PR #6506 (on #6314) still open but mergeable=False/dirty while ours is
  mergeable. The heavier repo workflows remain behind GitHub's
  external-contributor approval gate (`mergeable_state=unstable` with no
  failing run) — protection that must not be bypassed.
- **Tracker-tooling bug found and fixed (our side)**: `normalize_checks`
  took the LAST rollup item per check name, and GitHub lists check-runs
  newest-first — so any name with re-runs recorded its OLDEST conclusion.
  That manufactured the persistent `ci-failed` on #6475/#6476 (the check
  had already re-run green on 2026-10-03 and after the 2026-10-09 body
  updates) and inflated the "Check PR description fails" reading of the
  2026-10-16T20:51Z sync. Fixed in `scripts/update_tracker.py`
  (newest-run resolution by check-run id) and in the `gh` shim (emits ids);
  unit-checked against both rollup shapes.
- **The two fixed tracks were made durable upstream**: appended a factual
  "Re-verification (2026-10-17)" section to each PR body (head unchanged,
  fork tip matches, mergeable, dev tip unchanged, issue open) — the
  `edited` event re-ran the check, **success at 2026-10-16T21:17:36Z
  (#6475) and 21:17:40Z (#6476)**; all three `ci / PR checks` entries
  green, `ready for review` labels in place, and the checker deleted no
  comment because it posts none when the description is complete.
- **#6473's remaining failure is upstream content**: its gitleaks job
  (`secret-scan.yml`, `gitleaks git .` — full merge-ref history) fails on
  4 findings inside upstream commit `dab660543b5b` ("chore(publication):
  close pre-integration release blockers", `alteixeira20`, 2026-10-05).
  This PR carries a single commit (`35e3b298d8f8`); no rebase or merge can
  remove another branch's history object. Every our-side check on that PR
  (description, title, unmergeable, pytest, compileall, CodeQL, analyze,
  dependency-review) passes.
- **markitdown #2700 (Track 016)**: `license/cla` still QUEUED since
  2026-10-14 (service-side queue; nothing our automation can sign). If it
  flips to failed, the account signs through the CLA web flow (human
  action). mergeable=True; no conflicts despite the 400+-PR backlog.
- **markitdown #2699**: closed-unmerged as decided (Track 015); record
  intact and untouched.
- **No record of the 17 has an unanswered human review or comment** — bot
  PRs only, everywhere they exist. **Update (post-audit, 2026-10-17)**:
  this held when the audit ran and no longer does — nuriyoo's review on
  #786 landed at 10:47:21Z and is unanswered as of 18:30Z; that is now
  the top open item (Track 017; Blockers).

## Portfolio audit 2026-10-17T19:40–20:35Z (all 18 records, "perfect and 100% mergeable from my side")

Method: every record in `contributions-state.json` re-verified against
the live REST API in one scripted pass — merged PRs' merge-commit SHAs
vs recorded; open PRs' state/draft/mergeable/mergeable_state, head vs
recorded commits, fork branch tip vs PR head; the newest conclusion of
every check-run name (check-runs merged with commit statuses, resolved
by run id so re-runs resolve newest); all reviews; linked-issue states —
plus a live `is:pr author:ShahabAhmed01 is:open` search for coverage.

- **Coverage:** the search returns exactly 10 open PRs, and all 10 are
  tracked — nothing of ours lives outside the ledger.
- **7 merged PRs: every live merge commit matches the record byte-for-
  byte** (backlot #577/#614/#620/#633, libredb-studio #1628, repowise
  #3338, isomorphic-git #2456).
- **#2699**: closed-unmerged as decided (Track 015); record intact.
- **odysseus 7 PRs**: all OPEN, MERGEABLE, heads byte-match the recorded
  commits and the fork tips, all 7 linked issues still open, every
  repo-declared check green — `Check PR description`, `Check PR title
  (Conventional Commits)` and `Flag unmergeable PRs` are success on all
  seven (the repo's own checker run live, better than any local
  re-implementation). `mergeable_state: unstable` on all seven is the
  external-contributor approval gate; protection that must not be
  bypassed.
- **#6473's `gitleaks` is the one red check portfolio-wide, and it is
  upstream content — re-confirmed live this session:** `dab660543b5b` is
  an ancestor of `dev` (compare: status `ahead`, 71 commits ahead / 0
  behind), and `secret-scan.yml` checks out the merge ref with
  `fetch-depth: 0`, so every PR's scan sees that commit's 4 findings in
  `THIRD_PARTY_PROVENANCE.json`. No rebase or push of ours can remove
  base-branch history. It is non-required (unstable, not blocked) and
  every our-side check on that PR passes.
- **markitdown #2700's `license/cla` is a
  `microsoft-github-policy-service` check-run QUEUED since
  2026-10-14T17:53:29Z** (verified via the check-run's app slug — not a
  workflow of the repo, nothing of ours to run). Re-running it needs
  base-repo write access a contributor does not have; the account-level
  CLA already reads `pass` on #2699 (2026-10-14). If it flips to failed,
  the human signs through the CLA flow. `mergeable=True`, no conflicts
  despite the backlog.
- **backlot #806**: `clean`, 9/9 green; nothing owed.
- **backlot #786**: the audit's one our-side defect (nuriyoo's
  four-point review, unanswered) — fixed this session; see Track 017.
- **No record has an unanswered human review or comment as of 20:35Z**
  (#786's reply is posted; nothing human waits on us anywhere).
- **Post-audit correction (20:24–21:18Z): the 6-hourly CI sync mis-read
  #6475/#6476, and the resolver is now fixed.** CI's 20:24Z run (real
  `gh`, GraphQL rollup shape: no check-run ids, oldest-first listing)
  resolved duplicate check names by first listing position and flipped
  both odysseus PRs to `ci-failed` on `Check PR description` runs that
  **failed on 2026-10-03** — ground truth (newest run resolved by REST
  id, completed 2026-10-16T21:17Z) is `success`, exactly what every
  shim-side sync read. `normalize_checks` now decides a name's newest
  run by timestamp (`completedAt`, then `startedAt`, then `createdAt`,
  so an in-flight re-run supersedes the run it replaced), with the
  integer id as tie-break only and first position only for shapes with
  no metadata at all. Validated against the real #6475 run sequence in
  three rollup shapes plus active-re-run/status-only/shapeless/
  same-second/node-id-string cases; the shim emits the same timestamp
  keys, and the 21:18Z re-sync restored both records to
  `pr-opened`/`pass`. Same flip-flop family as the check-name/id bug
  fixed earlier on 2026-10-17 — now closed for both rollup shapes the
  ledger is ever synced through.

## Blockers

Nothing is owed on our side anywhere in the portfolio (re-verified
2026-10-17T20:35Z). Both open backlot PRs are wait-only:

- **#786 (Track 017) — wait only.** nuriyoo's four-point review was
  applied verbatim (`27e8922f`), the branch rebased onto `e9b9d72`, CI
  9/9 green, reply `6240438402` posted 20:22:46Z; awaiting re-review.
  Do not ping.
- **#806 (Track 018) — wait only.** Full 9/9 check-runs green (bare `test`
  = workflow-shape skip), `mergeable_state: clean`; no human review yet.
  Do not ping.
- Outside backlot the only non-green items are service-side and not ours:
  #6473's `gitleaks` (upstream history content, non-required) and
  #2700's queued `license/cla` (microsoft-github-policy-service) — both
  root-confirmed in the 2026-10-17T19:40Z audit above.

The odysseus `ci-failed` corrections from the 2026-10-17 audit below
still stand unchanged.

CORRECTIONS from the 2026-10-17 audit (supersedes the "NEW from the
2026-10-16T20:51Z sync" items below, which were shaped by the
check-name-resolution bug described in the audit):

- #6453/#6472/#6475/#6476/#6647/#6648 are **not** `ci-failed` and have
  no failing check — the persistent `Check PR description: fail` reading
  on #6475/#6476 was the earliest run's stale conclusion, not the check's
  current state. Body edits + the tooling fix (see audit) make all three
  `ci / PR checks` entries green on fresh 2026-10-16T21:17Z runs.
- #6473 (Track 003 — the audit also relabels it; the sync block below
  called it "Track 006" in error) remains the only `ci-failed` record, on
  exactly one check: `gitleaks`, and from upstream history content
  (`dab660543b5b`), not from our diff — see the audit for the root cause.
- The approval gate and zero-human-review facts below still hold for
  #6453/#6472/#6647/#6648.

Original 2026-10-16T20:51Z sync reading, kept for the record (since
corrected above; run with the REST shim, statuses from GitHub):

- ~~#6475 and #6476 (Tracks 004/005) flipped to `ci-failed`~~ — stale
  runs (see audit; fixed).
- ~~#6473 (Track 006) remains `ci-failed`, now on one check only:
  `gitleaks`~~ — track number is 003; failure root-caused upstream.
- PRs #6453/#6472/#6647/#6648 `pr-opened` with the first-time-contributor
  `action_required`/external-contributor gate — an expected protection
  that must not be bypassed — still zero human review.

Historical record (unchanged): **all seven earlier non-odysseus tracks
have landed** — backlot #577 merged 2026-10-10T13:59:45Z, libredb-studio
#1628 merged 2026-10-11T00:34:47Z, repowise #3338 merged
2026-10-11T07:56:49Z, backlot #614 merged 2026-10-12T04:31:35Z after
`nuriyoo`'s APPROVED, isomorphic-git #2456 merged 2026-10-12T07:52:12Z
by `jcubic` without a formal review (Tracks 008-011, 013), backlot #620
merged 2026-10-12T10:45:03Z after `nuriyoo`'s measurement-backed COMMENT
of 2026-10-12T04:17Z (three items all applied and answered the same day,
head `a3138ec`, CI 7/7 green, reply comment `6121983174`, Track 012),
and backlot #633 merged 2026-10-14T08:06:47Z — seventh merge (Track 014).
Track 015 (markitdown #2699) remains the one closed-unmerged record.

Two open courtesies, neither blocking:

- cevheri's questions on libredb issue #1411 (2026-10-09T22:43:56Z, "how
  was first-contribute on libredb studio / which databases are you using")
  are still unanswered; he merged the PR anyway. Worth a short reply.
- backlot capacity: three open PRs allowed since the first merge and all
  four backlot PRs (#577, #614, #620, #633) have merged — three slots
  free, for the next measured-fidelity issue from the open pool
  (re-verify claim-clean at selection).

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
  `contrib/issue-603-query-token-form-precedence` @ `5aaea3b` cut from
  upstream `main` `94e79a0`, uv venv with `.[dev,official-sdk,
  llamaindex]` — resolves to Python 3.11.17, which Track 014's full
  suite and the 2026-10-10 review-response runs used; the #577 PR's
  first-run numbers came from the original Python 3.14 install — both
  recorded in the PR and the per-contribution record; bundled corpus
  imported in `data/`)
- Repowise fork: https://github.com/ShahabAhmed01/repowise
- Repowise remotes: `origin` = fork, `upstream` = repowise-dev/repowise
- Repowise workspace: `~/opensource-work/repowise` (shallow clone `--depth 60`
  of `main`; branch `fix/flat-ternary-python-3285-v2` @ `b8224ee` cut from
  `b010215`; uv workspace, Python 3.11.17 — **`git rebase` is unusable in this
  clone across a moved base, cherry-pick instead**)
- isomorphic-git fork: https://github.com/ShahabAhmed01/isomorphic-git
- isomorphic-git remotes: `origin` = fork, `upstream` = isomorphic-git/isomorphic-git
- isomorphic-git workspace: `~/opensource-work/isomorphic-git` (clone of
  `main`; branch `feat/log-author-filter` @ `9cbc0feb` cut from upstream
  `main` `909b97b1`; npm install with node_modules present; **tests must
  run on the Node 22.22.0 toolchain at
  `~/opensource-work/.toolchains/node-v22.22.0-linux-x64/bin` — system
  Node 26 breaks the `@zenfs/core` fixtures repo-wide**; mock servers
  git-http-mock-server :8888 / cors-proxy :9999 started with
  `nps test.setup` and stopped with `nps test.teardown` or by killing the
  PIDs on those ports; build artifacts `http/`, `index.d.ts`,
  `__tests__/__fixtures__/index.json` are generated locally and are NOT
  part of the PR)
- Public tracker repo: https://github.com/ShahabAhmed01/opensource-contributions
- Known env-dependent test failures (identical on unmodified dev): browser
  tests need Playwright chromium binaries; containment/workspace tests need a
  bubblewrap-visible interpreter path (venv on an external mount); wave3 local
  tests need real model downloads; test_tls_overrides_scope fails due to
  in-tree worktree clones.
