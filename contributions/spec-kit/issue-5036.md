# github/spec-kit — #5036

## Status

**PR https://github.com/github/spec-kit/pull/5069 OPENED 2026-10-23T13:37:57Z** — ready for review, base `main` @
`27d14e2` (default branch verified current at creation: `27d14e20...`).
License compliance check `success` at filing; Lint / Security Audit / Test & Lint Python / Extension Version Guard / CodeQL all `action_required` (the first-time-fork workflow gate — a maintainer must approve the workflow runs before CI executes); no check failed as of 2026-10-23T13:40Z.

## Issue

https://github.com/github/spec-kit/issues/5036
"[Bug]: bug extension: README uses dotted command names, and re-assessing a
bug leaves the old fix and test reports in place"

Filed 2026-10-20, two-part, self-diagnosed from extension source with the
bot assessment (“Valid · severity medium”, slug `bug-extension-reasses...`);
labels `bug-assess`, `severity-medium`, `triage-must-have`; no human claim,
no assignee, no competing PR at selection (PR search for `5036|stale|README
uses dotted|bug extension` and the issue timeline both empty) — re-verified
immediately before `gh pr create`. The reporter themself disclosed AI
assistance in the issue body (Claude Opus 5.5, human-supervised draft) —
a project that models exactly the behavior its own CONTRIBUTING asks for.

## Pull Request

[#5069 — fix(bug): document installed command names and stale re-assessment flow](https://github.com/github/spec-kit/pull/5069)

- Base branch: `main` @ `27d14e2` — 4 files, +87/−4
- Fork head: `ShahabAhmed01:contrib/issue-5036-bug-extension-stale-reports-0f9d84c3`
- Fork repo: https://github.com/ShahabAhmed01/spec-kit
- Commit `45e3404d8fc4c57cd57da41e5cdfc6e37c21809e` with
  `Assisted-by: OpenCode (model: GLM-5.3-Flash Free, autonomous)` trailer
- Body keeps the live PR template exactly (Description / Testing / AI
  Disclosure with correct checkboxes checked and the free-form
  disclosure, naming agent, model, autonomous mode, extent)

## Semantics (two parts matching the issue's two findings)

1. **Installed command names documented.** `extensions/bug/README.md` gains
   an "Installed command names" section: the dotted `speckit.bug.*` names
   are the canonical extension command IDs (extension.yml / `specify
   extension list` / hook config), while agents install hyphenated skill
   names with per-agent invocation prefixes (`/speckit-bug-*` slash agents;
   `$speckit-bug-*` Codex/ZCode/Command Code; `/skill:speckit-bug-*` Kimi) —
   the same mapping as `docs/integrations/cli.md#command-invocation` and the
   integration guides. Typical-flow examples switched to the working
   `/speckit-bug-*` spellings; Guardrails gain the stale-report row.
2. **Re-assessment no longer leaves stale reports treated as current.**
   - `speckit.bug.assess.md`: after a *confirmed* interactive overwrite of
     `assessment.md`, the command asks what to do with sibling `fix.md` /
     `test.md` — rename to `fix.stale.md` / `test.stale.md` (never delete,
     disambiguating suffix if taken) or leave-and-flag in the Completion
     Report. Automated mode unchanged (already refuses overwrites).
   - `speckit.bug.test.md` prerequisites gain a **Staleness check**: stop
     when `assessment.md` was written after `fix.md` (compare `Created` vs
     `Fixed` header dates, fallback file mtimes), instruct re-running
     `__SPECKIT_COMMAND_BUG_FIX__ slug=<BUG_SLUG>` first; when timestamps
     can't be compared, interactive-confirm / automated-refuse. Guardrails
     mirror it. Prompt-template change only — no `.lock.yml` regeneration
     (lock files import markdown at runtime).

## Verification

- Environment locally: Python 3.14.8 (`uv`-managed repo), no node/go/rust.
- `uv run pytest tests/extensions/bug -q` with the change: **34 passed** (27
  before). Full suite `uv run pytest tests -q` on the final tree: **12,735
  passed / 461 skipped / 0 failed** (~6.5 min; pre-change baseline
  12,728/461/0). `git diff --check` clean; ruff is not part of the repo
  toolchain (not installed by `uv sync`).
- **Red/green proof** (evidence gate, D4): a separate `git worktree` of
  `origin/main` @ `27d14e2` with the same test file fails exactly the 7 new
  tests (7 failed, 27 passed); on the branch all pass. The change is
  template text itself, so the text tests pin the described behavior.
- Test lossage check: new tests in `tests/extensions/bug/
 test_bug_extension.py` follow the file's existing house style (classes +
 static text assertions).

## Agent disclosure ledger

- PR body: AI Disclosure section checked "did use", free-form disclosure
  naming OpenCode (GLM-5.3-Flash Free, autonomous) on behalf of
  ShahabAhmed01, extent = docs/prompt templates + their tests.
- Commit `45e3404`: `Assisted-by: OpenCode (model: GLM-5.3-Flash Free,
  autonomous)`.
- Filer cap: 0 open PRs by ShahabAhmed01 in spec-kit at filing (cap is 3).
- No issue comments posted on #5036 (the repo's own issue-assessment bot had
  already validated it; no claim protocol exists to follow).

Registry: this run reserved `github/spec-kit` in `coordination/parallel-runs.json` (branch `automation-coordination`) and is marked `PR_PUBLISHED` with head `45e3404`; the tracker-writer lease was held for these tracker edits and released after the push.
