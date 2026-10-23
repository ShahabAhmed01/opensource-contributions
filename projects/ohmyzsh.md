# Project notes — ohmyzsh/ohmyzsh

Last verified: 2026-10-23

## Facts

- Oh My Zsh: community-driven framework for managing zsh configuration,
  ~190k stars / ~29.4k forks (retrieved 2026-10-23), MIT, created
  2009-08-28, default branch `master`. One of the most recognized shell
  ecosystem projects; maintained by a small volunteer team
  (`robbyrussell`, `mcornella` and company).
- Plugins live in `plugins/<name>/`: a `*.plugin.zsh` file with the
  aliases/behaviour, a `_<name>` completion helper, an optional
  `tests/<name>.test.zsh` self-executing suite, and a `README.md`.
  `extract` is one of the highest-traffic utilities (unpacks ~30 archive
  formats via one `extract` function).
- Main branch `master`; Conventional Commits required
  (`fix(extract): …`), changelog generated automatically from them.
- CI (`.github/workflows/main.yml`) runs **only** `zsh -n` syntax checks
  over `./oh-my-zsh.sh`, `./lib/*.zsh`, `./plugins/*/*.plugin.zsh` and
  completions — plugin behaviour tests (like `tests/*.test.zsh`) are
  executed by contributors locally, not in CI.
- Plugin tests are self-contained: `zsh -df
  plugins/<name>/tests/<name>.test.zsh` builds its own fixtures in a
  mktemp dir, prints `PASS: <case>` per case.

## Development / validation commands

```bash
zsh -df plugins/extract/tests/extract.test.zsh   # plugin test suite
zsh -n plugins/extract/extract.plugin.zsh        # CI-parity syntax check
```

## Contribution policy (CONTRIBUTING.md)

- Direct outside PRs are welcome via a fork branch off the latest
  upstream `master`; PR template includes a standards checklist, a
  "Changes" section and issue links via `Fixes #XXXX` when one exists.
- **AI disclosure policy**: AI-assisted contributions must mention the
  assistance in the PR description ("AI-assisted" suffices; naming the
  tool modelled on other contribution categories is better); "PRs that
  appear to be unreviewed AI output, or code the contributor can't
  explain, may be closed without extensive feedback."
- Conventional Commits: `fix(<scope>): subject`, scope = plugin/theme
  name; changelog tooling consumes these.
- Alias additions require justification for all plugin users; themes are
  not accepted for now.

## Why this project was selected (2026-10-23 research)

- Merge-readiness evidence: 7 distinct external contributors merged
  around 2026-10-20 alone (PRs #14184/#14188/#14190/#14191/#14195 and
  more, all authors `author_association: CONTRIBUTOR`); recent external
  fixes were merged 3–6 days after opening; ~31 external merged PRs
  within a recent 60-PR closed window.
- Popularity evidence: 190k stars / 29.4k forks retrieved 2026-10-23 via
  `gh api repos/ohmyzsh/ohmyzsh`; recognized across shell tooling
  ecosystems; heavy daily push activity (pr-log: dep bumps, plugin fixes,
  updater chores).
- Task chosen by own audit: found the `.deb` double-nesting defect by
  tracing the member-extraction recursion (no existing issue; verified
  against open + closed PR searches and the sibling-adjacent closed
  issues #4946/#7948/#5476 for .deb history). Local zsh 5.9.2
  reproduction, red/green test, and 4-compressor variant matrix verified
  end-to-end locally before filing.
- Run context: reserved `ohmyzsh/ohmyzsh` in the shared
  `coordination/parallel-runs.json` registry before implementation, after
  releasing a `honojs/hono` candidate (hono's CONTRIBUTING
  restricts PR creation to maintainers — see `contributions/hono/issue-5569.md`).

## Pitfalls learned

- The plugin's recursion relies on relative re-derivation of extraction
  dir names (`${1:t:r}` → optional `.tar` strip → `-e` collision check);
  any nested member whose basename matches a pre-existing dir gets a
  random-suffix directory instead of merging. Prefer direct member
  extraction with `tar -C` over `extract` recursion when layout must be
  deterministic.
- The `tar` fallbacks differ per compressor; mirror the plugin's
  own per-branch chains (pigz/pbzip2, `tar --xz --help` probes,
  `xzcat|tar` fallbacks) instead of inventing new ones.
- `zsh -df` in a script file is the established plugin-test harness
  convention (`emulate -L zsh; setopt err_return` at the top of the
  test file; `} always { cleanup }` for temp dirs).
- No issue templates for bug reports beyond the title/body checks in the
  issue template; PR template checklist requires the AI disclosure item
  checked when applicable.
