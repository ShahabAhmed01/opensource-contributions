# Project notes — microsoft/markitdown

Last verified: 2026-10-14

## Facts

- "A Python utility for converting various file formats to Markdown" — PDF,
  Office, images, audio, HTML, and more, with a plugin system. ~28K stars.
  MIT license. Very active; `main` last moved 2026-10-04 (`4cc9fa1`).
- Python monorepo: `packages/markitdown` (core, `requires-python >=3.10,<3.15`),
  `packages/markitdown-ocr`, `packages/markitdown-mcp`,
  `packages/markitdown-sample-plugin`. Default and only dev branch: `main`.
- Core conversion pipeline: format converters feed an `HtmlConverter`
  built on BeautifulSoup + a vendored `_CustomMarkdownify`; DOCX goes
  through mammoth first. `MarkItDown(...)` accepts `llm_client`/`llm_model`/
  `llm_prompt` kwargs, stored on the instance and forwarded into converter
  calls (image/PPTX describers, `markitdown-ocr`).
- No root CONTRIBUTING.md; policy lives in README §Contributing (CLA via
  `microsoft-github-policy-service` bot, Microsoft Open Source CoC, "What to
  Contribute" scope section — CLI, converters, MCP, tests/docs/tooling are
  in scope; apps/servers are out).
- Contribution labels: `good first issue` (4 open), `open for contribution`
  (16 open, mostly large features). 313 open issues, ~402 open PRs — a huge
  review backlog; most well-written recent bugs already have 1–4 competing
  open PRs, and many table-adjacent areas have multiple competing
  implementations (#2252/#2521, #2537/#2651, #2441/#2465/#2608).
- Review responsiveness is the bottleneck: sibling PRs #1898/#1908/#2277/
  #2422 received ZERO maintainer comments over months; several died of
  neglect. Counter-signal: afourney actively triaged old PRs in September
  2026 (#175 closed with an invitation).

## Development / validation commands

```bash
cd packages/markitdown
uv run --extra all --with pytest pytest tests/test_cli_misc.py -q   # one file
uv run --extra all --with pytest pytest tests/test_cli_vectors.py -q # CLI matrix (~100s)
hatch test                      # what CI runs (Python 3.10–3.14, ubuntu+windows+arm)
uv run --with "black==23.7.0" black --check <files>   # pinned pre-commit hook
mypy --ignore-missing-imports src/markitdown tests    # types env (28 pre-existing errors in tests)
```

- CI (`tests.yml`): `hatch test` matrix + separate `ocr-tests` and `mcp-tests`
  jobs; `pre-commit.yml`: `pre-commit run --all-files` (black 23.7.0 only).
- Tests that need audio tooling (ffmpeg/ffprobe/exiftool) fail or skip on
  this machine; `tests/test_module_misc.py::test_speech_transcription` fails
  at baseline here.

## Contribution policy (README §Contributing)

- CLA required (bot decorates the PR; already satisfied for this account).
- Scope rules: bug fixes, converter fidelity, the CLI, markitdown-mcp,
  tests/docs/tooling are in scope; new apps/services are not; new formats
  are added sparingly.
- Issues labeled "open for contribution" are suggestions, not assignments;
  effectively nothing is formally assigned (2 of 313 issues have assignees).
  PRs reference issues directly; no claim-comment policy is documented.
- No AI-assistance policy found (no AGENTS.md/CLAUDE.md); the PR body for
  #2700 disclosed AI assistance anyway.

## Why this project was selected (2026-10-14 research)

- High volume of external merges, an active maintainer (afourney), and a
  documented scope that includes exactly the kind of bounded CLI work this
  portfolio targets.
- Issue #1897 carried an explicit maintainer invitation for a fresh PR
  (2026-09-03, on #175) — the strongest acceptance evidence in the whole
  2026-10-14 search.
- Risks known at selection: enormous PR backlog (402 open), silent review
  queue, heavy bot traffic, and saturated duplicate lanes on popular issues.

## Pitfalls learned

- #1784 (CSV empty warning): the previous session's duplicate check was
  wrong — issue #1784 had a cross-referencing open PR (#2675) with tests,
  six days older. The only reliable duplicate check is the issue TIMELINE
  cross-referenced events plus keyword PR searches, immediately before
  publishing. Our PR #2699 was closed as a duplicate.
- Symptom-only issues (like #1784) may have never-confirmed acceptance
  criteria; maintainer-confirmed gaps (#1897 via #175) are far safer.
- `_markdownify.py` is a hot spot: several open PRs compete on table
  rendering (`table_infer_header`, td→th promotion, caption/tfoot
  normalization); avoid that lane — issue #1086 was rejected as duplicated
  by open PR #2521 during this research.
- `hatch test` is the CI runner, but `uv run --extra all --with pytest`
  is a fast local equivalent for single files.

## Contribution history

### #1784 — Empty CSV input produces no diagnostic (**CLOSED-UNMERGED** as PR #2699, 2026-10-14)
Closed by us the same day: duplicated by open PR #2675 (see
`contributions/markitdown/issue-1784.md`). Branch preserved on the fork.

### #1897 — Documented `--llm-client`/`--llm-model` CLI flags never existed (**PR #2700 OPEN**, 2026-10-14)
Adds `--llm-client`/`--llm-model`/`--llm-prompt` to the core CLI with lazy
client construction, pairing validation, and 9 regression tests. Invited by
maintainer afourney on #175. See `contributions/markitdown/issue-1897.md`.

## Future leads (unverified / not claimed)

- #1145 (suppress the `## <SheetName>` header in xlsx output) — zero PRs,
  zero comments; needs a small API-design decision, no maintainer demand.
- #244 (option to skip DOCX headers/footers) — zero PRs; medium feature.
- #2275 (surface DOCX comments in markdown) — prior attempt #2322 closed
  unmerged; needs `word/comments.xml` parsing.
- Revisit the #1784 lane only if PR #2675 closes unmerged.
