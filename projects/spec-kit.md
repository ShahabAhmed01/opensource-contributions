# Project notes — github/spec-kit

Last verified: 2026-10-23

## Facts

- Spec-Driven Development toolkit ("Specify CLI") by GitHub: `specify init`
  scaffolds a project with agent-agnostic command/prompt templates; the CLI
  is Python (`uv`-managed, `src/specify_cli/`). MIT. ~142k stars, created
  2025-08-21, very high issue/PR velocity, heavy link agentic use.
- Bundled extensions live in `extensions/<id>/` (`extension.yml` manifest +
  `README.md` + `commands/<command>.md` prompt templates); the bug triage
  workflow (`extensions/bug/`) is a three-step assess → fix → test flow over
  per-bug markdown reports under `.specify/bugs/<slug>/`.
- Command IDs are dotted (`speckit.bug.assess`); agents install them as
  hyphenated skill names (`speckit-bug-assess`) with per-agent invocation
  prefixes centered in `src/specify_cli/_invocation_style.py` (`/` slash
  agents, `$` Codex/ZCode/Command Code, `/skill:` Kimi) and
  `docs/integrations/cli.md#command-invocation`.
- Main branch: `main`. Conventional-commit PR titles (`fix(scope): …`,
  `docs: …`). CHANGELOG.md is written by `chore: release …` automation only —
  individual PRs do not touch it.
- Tests: `uv run pytest tests -q` (12,728 passed / 461 skipped baseline on
  Python 3.14.8, ~6.5 min). `tests/extensions/` suites assert bundled
  layout/manifest facts and template content as static text tests.
- Command `.md` templates require no lock regeneration: `.lock.yml` files
  import the markdown at runtime (per `tests/test_bug_fix_workflow.py`).

## Development / validation commands

```bash
uv sync --extra test
uv run pytest tests -q                 # full suite
uv run pytest tests/extensions/bug -q  # targeted
```

- No ruff/mypy in the repo toolchain (ruff not installed by `uv sync`).

## Contribution policy (CONTRIBUTING.md)

- **Evidence gate**: valid in-scope change needs a reproduction or linked
  real-world report + a regression test that fails on `main` and passes with
  the change; one concern per PR.
- **Triage robots apply labels** (`triage-must-have`, `severity-medium`, …)
  and there is an automated issue-assessment bot that posts verdicts on bug
  reports.
- **AI assistance must be disclosed** (agent/tool, model(s), settings/mode,
  extent) in the PR body AND in every agent-authored commit (`Assisted-by:`
  trailer naming agent, model, autonomous/supervised) AND every AI-generated
  PR comment. Three-open-PR cap per filer (check before filing). PR template
  has an "AI Disclosure" section with checkboxes plus a free-form
  disclosure; deleting/blanking the AI section gets AI-effort PRs closed.
- Community catalog changes must go through submission *issues*, never by
  direct edit of `extensions/catalog.community.json`.

## Why this project was selected (2026-10-23 research)

- Rank order attempted in this run: apache/airflow (every candidate bug
  PR-covered; hyper-saturated), aio-libs/aiohttp (0/%100 outside-human merge
  rate in the window), sympy/sympy (AI-policy hostility — validated patch
  withheld). spec-kit explicitly welcomes disclosed AI-assisted contributions
  ("We welcome and encourage the use of AI tools ...") with a clear rules
  framework — the right fit for an autonomous agent run.
- Issue #5036 chosen: bot-assessed Valid/medium, `triage-must-have`, created
  2026-10-20, no human claim, no competing PR (search + timeline verified
  twice), small well-defined two-part fix fully testable locally
  (static-text red/green), no skill gaps (Python/uv only).
- Eliminated alternatives in spec-kit: several larger `specify-cli` bugs
  needed runtime/integration mocks; README-only items were too trivial to
  clear the evidence gate meaningfully.

## Pitfalls learned

- The PR template evolved from an older strict-headings form ("References to
  other Issues or PRs" / "Brief description…" / "Other comments" /
  "Release Notes") to a simpler Description/Testing/AI Disclosure form —
  always fetch the live template (`gh api …PULL_REQUEST_TEMPLATE.md`) rather
  than trusting notes.
- Pre-commit hooks are not enforced when the environment lacks identity
  setup — `--no-verify` was not needed; commits are clean if identity is set
  repo-locally.
- `git worktree add` of `origin/master` fails — the default branch is
  `main`.
- The dot-to-hyphen skill-name mapping appears in ~10 integration modules;
  quote the canonical ones (`_invocation_style.py`,
  `docs/integrations/cli.md#command-invocation`) in docs instead of
  re-deriving.
