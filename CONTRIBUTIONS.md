# Contribution Ledger

Full history of contributions tracked by this workspace.

## Contributions

<!-- BEGIN CONTRIBUTIONS TABLE -->
| Date | Repository | Issue | PR | Status | Description |
|---|---|---|---|---|---|
| 2026-10-12 | brekkylab/backlot | [#603](https://github.com/brekkylab/backlot/issues/603) | [#633](https://github.com/brekkylab/backlot/pull/633) | In review | Refuse a non-empty token query parameter as invalid_auth (an empty one beside a bearer header too) and read the token form field ahead of the bearer header, as real Slack does for apps created after 2021 |
| 2026-10-11 | isomorphic-git/isomorphic-git | [#2286](https://github.com/isomorphic-git/isomorphic-git/issues/2286) | [#2456](https://github.com/isomorphic-git/isomorphic-git/pull/2456) | Merged | Add an `author` option to git.log(): a case-insensitive JavaScript regular expression tested against the author's `Name <email>` string, applied before `depth` is counted and composable with `filepath`; filtering reads the author only, not the committer; an invalid regex rejects with SyntaxError |
| 2026-10-11 | brekkylab/backlot | [#586](https://github.com/brekkylab/backlot/issues/586) | [#620](https://github.com/brekkylab/backlot/pull/620) | Merged | Reorder conversations.history's argument-error checks to real Slack's reading order — latest, then oldest, then the cursor — so a request with two or more unreadable arguments is named by the first real would read |
| 2026-10-11 | brekkylab/backlot | [#610](https://github.com/brekkylab/backlot/issues/610) | [#614](https://github.com/brekkylab/backlot/pull/614) | Merged | Add GET/HEAD /s3/{bucket}/ routes delegating to bucket handlers so a bucket path ending in / returns the bucket listing (matching real S3) instead of 404 NoSuchKey for an empty key |
| 2026-10-10 | repowise-dev/repowise | [#3285](https://github.com/repowise-dev/repowise/issues/3285) | [#3338](https://github.com/repowise-dev/repowise/pull/3338) | Merged | Make a Python conditional-expression chain report one if decision instead of one per ifexp, matching the elif dispatch it compiles to and the flat ternary TypeScript already reports |
| 2026-10-09 | libredb/libredb-studio | [#1411](https://github.com/libredb/libredb-studio/issues/1411) | [#1628](https://github.com/libredb/libredb-studio/pull/1628) | Merged | Couchbase connect() now refuses a 404 on /pools/default/buckets/<bucket> naming the bucket; Trino connect() warns, via connectWarnings(), naming a pinned catalog absent from system.metadata.catalogs |
| 2026-10-09 | brekkylab/backlot | [#554](https://github.com/brekkylab/backlot/issues/554) | [#577](https://github.com/brekkylab/backlot/pull/577) | Merged | Mark a non-finite oldest/latest reading in _slack_ts as unparseable so conversations.history answers invalid_ts_oldest/invalid_ts_latest instead of a 500 from the window's uncaught int() |
| 2026-10-09 | odysseus-dev/odysseus | [#1912](https://github.com/odysseus-dev/odysseus/issues/1912) | [#6648](https://github.com/odysseus-dev/odysseus/pull/6648) | In review | Split the inverted guard in _resolveComposeSendAccountId so a deleted active account resolves to null (default SMTP fallback) instead of returning the stale id |
| 2026-10-09 | odysseus-dev/odysseus | [#6186](https://github.com/odysseus-dev/odysseus/issues/6186) | [#6647](https://github.com/odysseus-dev/odysseus/pull/6647) | In review | Route read-only Notes/todo requests to manage_notes by adding three rows to _ROUTING_PATTERNS in src/action_intents.py so Chat mode promotes to agent mode. |
| 2026-10-03 | odysseus-dev/odysseus | [#6314](https://github.com/odysseus-dev/odysseus/issues/6314) | [#6476](https://github.com/odysseus-dev/odysseus/pull/6476) | In review | Strip tool_calls from assistant messages whose predecessor is not a user or tool turn so strict providers reject neither the payload |
| 2026-10-03 | odysseus-dev/odysseus | [#6464](https://github.com/odysseus-dev/odysseus/issues/6464) | [#6475](https://github.com/odysseus-dev/odysseus/pull/6475) | In review | Pass an explicit HTTPBasicAuth to caldav.DAVClient so passwords containing spaces (Opencloud app tokens) are encoded correctly |
| 2026-10-03 | odysseus-dev/odysseus | [#6432](https://github.com/odysseus-dev/odysseus/issues/6432) | [#6472](https://github.com/odysseus-dev/odysseus/pull/6472) | In review | Raise quick_parse max_tokens (512 to 6144) and timeout (20s to 60s) so reasoning models can return parseable JSON (bug 2 of #6432) |
| 2026-10-03 | odysseus-dev/odysseus | [#5049](https://github.com/odysseus-dev/odysseus/issues/5049) | [#6473](https://github.com/odysseus-dev/odysseus/pull/6473) | In review | Guard the three research_* settings reads in src/task_scheduler.py with try/except fallbacks to documented defaults (8192/90/3) |
| 2026-10-02 | odysseus-dev/odysseus | [#2740](https://github.com/odysseus-dev/odysseus/issues/2740) | [#6453](https://github.com/odysseus-dev/odysseus/pull/6453) | In review | Move SQLAlchemy 2.0 declarative imports off the deprecated sqlalchemy.ext.declarative path and drop the stale test stubs |
<!-- END CONTRIBUTIONS TABLE -->

## Status legend

- **In progress** — issue selected, no PR yet
- **In review** — PR open, awaiting maintainer review and/or CI
- **Changes requested** — maintainer requested changes; being addressed
- **Ready to merge** — approved with CI green
- **Merged** — merged into the project
- **Closed** — closed without merge
- **Superseded** — another change resolved the problem

Per-contribution records with problem, root cause, solution, tests, and validation live under [`contributions/`](contributions/).
