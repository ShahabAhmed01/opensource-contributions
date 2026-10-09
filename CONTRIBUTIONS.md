# Contribution Ledger

Full history of contributions tracked by this workspace.

## Contributions

<!-- BEGIN CONTRIBUTIONS TABLE -->
| Date | Repository | Issue | PR | Status | Description |
|---|---|---|---|---|---|
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
