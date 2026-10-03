# OS Contributions

A curated record of meaningful open-source contributions, with issue references, pull requests, validation, and merge status.

## Contributions

<!-- BEGIN CONTRIBUTIONS TABLE -->
| Date | Repository | Issue | PR | Status | Description |
|---|---|---|---|---|---|
| 2026-10-03 | odysseus-dev/odysseus | [#6432](https://github.com/odysseus-dev/odysseus/issues/6432) | — | In progress | Raise quick_parse max_tokens (512 to 6144) and timeout (20s to 60s) so reasoning models can return parseable JSON (bug 2 of #6432) |
| 2026-10-03 | odysseus-dev/odysseus | [#5049](https://github.com/odysseus-dev/odysseus/issues/5049) | — | In progress | Guard the three research_* settings reads in src/task_scheduler.py with try/except fallbacks to documented defaults (8192/90/3) |
| 2026-10-02 | odysseus-dev/odysseus | [#2740](https://github.com/odysseus-dev/odysseus/issues/2740) | [#6453](https://github.com/odysseus-dev/odysseus/pull/6453) | In review | Move SQLAlchemy 2.0 declarative imports off the deprecated sqlalchemy.ext.declarative path and drop the stale test stubs |
<!-- END CONTRIBUTIONS TABLE -->

_This table is maintained by [`scripts/update_tracker.py`](scripts/update_tracker.py), which runs in GitHub Actions every 6 hours and on demand._

## How This Works

This repository keeps a factual record of contribution work: the issue, the pull request, the files and tests involved, and the merge status. Machine-readable state lives in [`contributions-state.json`](contributions-state.json); per-contribution records live under [`contributions/`](contributions/).

## Projects

- **odysseus-dev/odysseus** — self-hosted AI workspace (Python/FastAPI, AGPL-3.0). Notes: [`projects/odysseus.md`](projects/odysseus.md).
