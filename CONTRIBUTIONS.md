# Contribution Ledger

Full history of contributions tracked by this workspace.

## Contributions

<!-- BEGIN CONTRIBUTIONS TABLE -->
| Date | Repository | Issue | PR | Status | Description |
|---|---|---|---|---|---|
| 2026-10-03 | odysseus-dev/odysseus | [#6432](https://github.com/odysseus-dev/odysseus/issues/6432) | — | In progress | Raise quick_parse max_tokens (512 to 6144) and timeout (20s to 60s) so reasoning models can return parseable JSON (bug 2 of #6432) |
| 2026-10-03 | odysseus-dev/odysseus | [#5049](https://github.com/odysseus-dev/odysseus/issues/5049) | — | In progress | Guard the three research_* settings reads in src/task_scheduler.py with try/except fallbacks to documented defaults (8192/90/3) |
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
