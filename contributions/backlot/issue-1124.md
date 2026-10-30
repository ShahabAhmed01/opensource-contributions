# brekkylab/backlot — #1124

## Status

**PR #1153 OPENED** — opened 2026-10-30 (UTC) against `main` @
`81f33e465a47bfc745be75d2d97bdbf69123beed`, verified the current
upstream tip immediately before publication. Contribution 8 of 8 in
this repository. Published from `ShahabAhmed01/backlot` via the GitHub
Git Data API (blobs → tree → commit → ref) because bulk git transfer
(`git clone`/archive fetch/tarball) stalls in this environment; the
resulting commit `0a51616cb6d91b2b0fd2b8903d8715e37eda1438` is
byte-complete and SHA-verified end to end (see Publication). Not merged;
awaiting review.

## Issue

https://github.com/brekkylab/backlot/issues/1124
"github: the /agents routes ignore the API version for a token and ask
for a credential on any path"

OPEN, unassigned, 0 comments at selection and 0 immediately before the
PR opened, created by `nuriyoo` while measuring for #1119, label
`fidelity`. Two silent divergences recorded against `80e1f7a`, carried
into the issue by the maintainer's live calls to api.github.com on
2026-10-28:

1. On the four `/agents/...` operations the baseline publishes but no
   route serves (`GET /agents/automations/1/tasks`,
   `GET /agents/repos/{o}/{r}/automations/1`,
   `GET /agents/repos/{o}/{r}/automations/1/tasks`,
   `GET /agents/repos/{o}/{r}/pulls/1/agent-merge`), a token that
   resolves was answered the version's 400 on a pinned `1999-01-01`,
   and its 404 carried `x-github-api-version-selected` — real answers
   the same 404 with the header pinned as without and echoes nothing.
2. Any path under `/agents/repos/{owner}/{repo}/` and
   `/agents/tasks/{}/` asks for a credential — no credential → 401
   "Requires authentication", `Bearer nope` → 401 "Bad credentials", a
   token → the plain text `404 page not found` — where Backlot refused
   only its baseline patterns and router-404'd the rest (status still
   404 for a caller real 401s).

At publication the upstream tip had already moved `80e1f7a` →
`81f33e4` (#1119's merge plus #1105/#1112 touching
`backlot/routers/github.py` and #1027/#1055/#1068/#1081/#1120/#1140/#1141),
so the workspace was re-fetched and the patch re-applied onto the
current tip rather than the issue's pinned base.

## Pull Request

[#1153 — github: the /agents routes read no API version and ask for a
credential on any path of their two
families](https://github.com/brekkylab/backlot/pull/1153)

- Base branch: `main` @ `81f33e465a47bfc745be75d2d97bdbf69123beed`
  (verified current at PR creation: upstream `branches/main` returns
  this SHA)
- Fork head: `ShahabAhmed01:contrib/issue-1124-agents-version-token-977388f8`
  @ `0a51616cb6d91b2b0fd2b8903d8715e37eda1438`, 1 commit, parented
  directly on the upstream tip
- 3 files changed, +208/−3
- Closes #1124 (`Closes #1124.` in the description; the PR-gate's
  `closed_issues` read verified locally against
  `scripts/pr_gate.py:format_problems` — no problems, and the gate
  workflow itself ran success on the head)

## Publication (Git Data API, no git push)

The environment's throttled network stalls bulk git protocol; per-
request `gh api` calls work. The fork already holds the upstream
objects (verified `GET /repos/ShahabAhmed01/backlot/commits/81f33e4…`
in the fork). Steps taken, each verified before the next:

1. Local git history rebuilt from the SHA-verified fetch:
   `backlot-ws` git `main` holds the exact `81f33e4` tree (commit
   `67429da`, all 316 files hashed against the fetch's `git/trees`
   listing), branch `contrib/issue-1124-agents-version-token-977388f8`
   holds the patch (commit `e54858e` locally → `0a51616` in the fork).
2. Three blobs posted to the fork
   (`POST /repos/ShahabAhmed01/backlot/git/blobs`, base64) — the API's
   returned SHA matched the locally computed `git hash-object` value
   for each, proving upload integrity byte-for-byte:
   `github.py → 410170d5e9ebc5064f4b81277a2821d66b6fa419`,
   `main.py → c2b9559593e638334742df0b282c53901547ffd3`,
   `test_github.py → 497a59c5f05afe17129c55c627c1ceebbb11bb68`.
3. Tree created with `base_tree` = the tip's tree `ec45f766a063d347fef35a51ede8f7d6423a0b9a`
   and the three blob entries → `b8c0f1ab11bf81c413847086d1748710500515bf`.
4. Commit created (message = the PR title, one parent `81f33e4…`) →
   `0a51616cb6d91b2b0fd2b8903d8715e37eda1438`.
5. Ref `refs/heads/contrib/issue-1124-agents-version-token-977388f8`
   created at that commit; `POST /repos/brekkylab/backlot/pulls`
   opened #1153.
6. Verification after open: `GET /pulls/1153` reports 3 changed files,
   1 commit, `base sha 81f33e4`; body round-tripped intact (only a
   trailing newline added).

## Problem

`GET /github/agents/repos/{o}/{r}/nosuch`,
`GET /github/agents/repos/{o}/{r}/automations/1/nosuch` and
`GET /github/agents/tasks/1/nosuch` — all under the two families the
issue names — fell through to the router's 404 envelope with the no
credential / no five / token answering rules of an unrouted path, on
every method, with the version header read when pinned: an anonymous or
bad-credential caller is 401-able in real there, and a resolving token
is answered the plain-text `404 page not found` of real's own router,
not an envelope. Separately, a resolving token on the four
published-but-unserved agent operations got the version's 400 on a
pinned unknown version and the echo on its 404, where real reads no
version of any `/agents` caller.

## Root Cause

`backlot.routers.github.honours_api_version` exempted only code search
and a credentialless `/rate_limit`, so every `/agents` request was
version-checked and echoed by `backlot.main`'s echo middleware. The
credential refusals lived only in
`refuse_an_unserved_operation`, whose membership is the baseline's
`missing` operations plus the two routed-unpublished
`/agents/automations/…` shapes — outside the two families' path space —
so any other path under `/agents` was an ordinary unrouted GitHub path.

## Solution

- `honours_api_version` returns False for an `/agents` path
  (`_an_agent_path`), which silences both the version's 400 and the
  echo for the whole prefix; the docstrings of
  `honours_api_version` and `refuse_an_unserved_operation` carry the
  measurement and its four measured operations.
- New `under_an_agent_family(path)` reads the two families
  (`/agents/repos/{owner}/{repo}/…` and `/agents/tasks/{id}/…`, each
  family's own path included) from the scope path, with the maintainer's
  three measured paths and the negative rows
  (`/agents/nosuchthing`; `/agents/automations/1/nosuch`,
  `/agents/automations/x/y/z` 404-for-every-credential) in its
  docstring.
- New
  `refuse_a_credential_on_an_agent_path(request)`: no
  `Authorization` header (or one carrying no credential) is the 401
  "Requires authentication", counted for GET/POST and uncounted for
  PATCH/PUT/DELETE through the same state
  `refused_an_unserved_operation` reads (its docstrings note the
  sharing); a non-resolving credential is "Bad credentials"; a
  `Basic` value naming no token is `_require`'s 401; a resolving caller
  gets `PlainTextResponse("404 page not found", 404)` with none of the
  five.
- `backlot.main` registers the gate after
  `refuse_an_unserved_github_operation` and before the version echo and
  the rate-limit headers; its `runs_on` defers the paths an operation
  of the baseline publishes on a family, which keep the unserved
  machinery's refusals and the router's 404 for a token.
- `tests/test_github.py`: the `_UNSERVED_ROWS` refusal loop gains an
  `/agents` branch (no echo, pinned unknown version no longer a 400,
  same statuses), plus four new tests — three parametrized over
  `_AGENT_FAMILY_PATHS` (each of the three credential states, each with
  and without the version pinned) and one for the families' own paths
  (`GET /agents/repos/{o}/{r}`; `GET /agents/tasks/{}` is a published
  `missing` operation and stays on the unserved rows).

## Files Changed

- `backlot/routers/github.py` (+90/−2) — the version exception, the two
  path helpers, the gate, docstring updates
- `backlot/main.py` (+28/−1) — the middleware and the echo docstring's
  agent note
- `tests/test_github.py` (+90/−0) — the agents branch in the refusal
  loop, the docstring note, four new tests

## Tests

- **Fail-without-change:** with `backlot/` checked out to the base
  commit and the tests left in place, all four new
  `agent_families` tests fail (the three gate paths 401-expected vs 404,
  and the family's own path); with the tree's sources they pass.
- **Full suite:** `pytest -o addopts=""` (serial, exact counts) on the
  exact published tree: **8337 passed, 44 skipped in 547s, exit 0**
  (`.[dev]` editable install, Python 3.13-era venv already in the
  workspace). Green under xdist as well (~51s).
- **Skip census (-rs):** all 44 are missing-optional-import skips in
  `tests/test_s3.py` (botocore), `tests/test_sdk.py` (slack_sdk),
  `tests/test_mcp.py` (mcp), `tests/test_llamaindex.py`
  (llama_index.readers.*), `tests/test_telemetry.py:1069` (fastmcp) and
  the reader/Google/mirage tests of `tests/test_integrations.py`
  (mirage, gdrive_fsspec) — none touches the changed files.
- **Before/after probe:** a temporary 48-request probe (the three gate
  paths, the four published agent operations, and the negative
  neighbors, × {none, `Bearer nope`, admin token} × {version pinned,
  not} plus HEAD/OPTIONS/PUT/DELETE on a gate path) was run against the
  base tree and the patched tree. Every intended difference appears and
  nothing else moves: anonymous on a family path 404→401 (five kept for
  GET, kept-off for the uncounted write methods per the mirrored
  unserved semantics), `Bearer nope` 404→401 "Bad credentials" (no five,
  before and after), token text-404 (pinned or not), the published
  rows' version-400 gone and echo gone with statuses and the five
  unchanged, and
  the negative rows byte-identical to their before answers.
- **Lint:** `ruff check .` clean; `ruff format --check .` — 194 files
  already formatted. **Prose gate:** `python scripts/prose_check.py main`
  exits 0 (no issue-number prose, no test-line dates).
- **PR-gate dry check:** `scripts/pr_gate.py:format_problems(title,
  body, {"github"})` → no problems; `closed_issues(body)` → `[1124]`.

## Runtime Validation

No live api.github.com call from this session (no GitHub API token in
the environment; the network also cannot reach it directly). The
acceptance measurement is the maintainer's live-call table carried in
the issue (2026-10-28): the four operations' version behavior, the
three paths' credential behavior with and without the version pinned,
and the negative rows from the maintainer's table quoted in
`_ROUTED_UNPUBLISHED`'s note. Local Before/Now columns in the PR body
are this workspace's own probe run against both trees, stated as such.

## CI (live at 2026-10-30, all checks completed)

- gate: success · lint: success · scan: success
- test (3.11): success · test (3.12): success · test (3.13): success ·
  test (3.14): success · test (3.15): success — all five completed within
  ~45 minutes of open
- bare `test`: skipped (workflow shape on fork heads, as in #851)
- No gate-bot comment was posted on the PR.

## Review

None yet — awaiting maintainer review (`nuriyoo`; the previous seven
backlot PRs were all reviewed or merged by `nuriyoo`).

## Merge

Not merged. Open as of 2026-10-30 (UTC) with all CI check-runs
completed and none failing, awaiting the first human review.

## Lessons Learned

- **Mixed-pin workspaces lie:** the run's earlier file-by-file fetch
  had one half of the tree from `80e1f7a` (pinned) and one from the
  then-current `main` (unpinned `contents` calls) — 195 phantom test
  failures that looked like pre-existing breakage. Every fetched file
  must be hash-verified against its commit's own `git/trees` SHA, and
  the whole tree re-fetched when the base moves.
- **Upstream moved mid-run:** between the issue's pinned base and
  publication, `main` advanced nine merges including two that touch the
  same file (`backlot/routers/github.py`). The PR was re-based on the
  current tip and re-applied; the divergence was still live on all
  measured paths (re-verified by the probe), so no re-scoping was
  needed.
- **Git Data API publication:** for a repo whose bulk git transfer
  stalls, `blobs → tree(base_tree) → commit(parent=tip) → ref → PR`
  in the fork replaces push/clone entirely, and each blob SHA matching
  a locally computed `git hash-object` proves upload integrity —
  stronger than a push, because the API echoes what it received.
- **Serial counts under xdist:** this repo's `pyproject.toml` addopts
  force `-n auto --dist worksteal`, so `-o addopts=""` (not
  `-p no:xdist`, which leaves `--dist` unknown) is the way to get a
  definitive serial pass/skip line for a PR description.
