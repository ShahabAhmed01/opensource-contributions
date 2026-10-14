# microsoft/markitdown — #1897

## Status

**PR #2700 OPENED** 2026-10-14T17:53:21Z — MERGEABLE, awaiting maintainer
review (no human review yet). CI: license/cla queued/pending at last check
(2026-10-14T17:55Z); Copilot left a COMMENTED bot review. Per policy, no
pings.

## Issue

https://github.com/microsoft/markitdown/issues/1897
"Unrecognized Arguments Error in markitdown CLI for undocumented arguments"

OPEN, unlabeled, unassigned, created 2026-05-20T12:02:52Z, unchanged since
2026-05-20T13:26:35Z. The markitdown-ocr README documents

```bash
markitdown document.pdf --use-plugins --llm-client openai --llm-model gpt-4o
```

but the CLI never defined `--llm-client`/`--llm-model`, so the documented
command fails with `unrecognized arguments`. (The issue also blames
`--use-plugins`; that flag has existed since PR #318, so only the `--llm-*`
flags were missing — verified against `main` @ `4cc9fa1`.)

Selection-time evidence (all verified live on 2026-10-14):

- **Maintainer invitation** — afourney (MEMBER), 2026-09-03T22:57:21Z on
  https://github.com/microsoft/markitdown/pull/175: "`llm_client`, `llm_model`
  and `llm_prompt` are available through the Python API, but there is still no
  `--llm-*` flag on the CLI … the feature is still wanted … a fresh PR against
  `main` would be very welcome and will get a much faster look."
- Prior attempts #1898 and #1908 were **self-closed by their authors** after
  maintainer silence — never rejected (verified via each PR's timeline).
- Competition at publication: #2277 ("Add OpenAI options to CLI") is OPEN but
  `CONFLICTING` with main and untouched since 2026-08-05; #2422 is a
  docs-only alternative that deletes the flags from the README; no open PR
  references #1897 (timeline cross-refs = only the two closed attempts).

## Pull Request

[#2700 — Add --llm-client, --llm-model, and --llm-prompt options to the CLI](https://github.com/microsoft/markitdown/pull/2700)

- Base branch: `main` @ `4cc9fa17653d695d64fb9eee5b33d4de55ff84e8`
- Opened: 2026-10-14T17:53:21Z · State: open, not draft, MERGEABLE
- Fork head: `ShahabAhmed01:contrib/issue-1897-cli-llm-options`
- Closes #1897 (`Fixes #1897` in the body; confirmed by
  `closingIssuesReferences`)
- Size: 2 files, +253/−3
- Body references all prior work (#175, #1898, #1908, #2277, #2422) and
  discloses AI assistance

## Branch

`contrib/issue-1897-cli-llm-options`, cut from `origin/main` @ `4cc9fa1`
(base verified unchanged immediately before publication). Workspace:
`/tmp/markitdown` (remotes: `origin` = microsoft/markitdown, `fork` =
ShahabAhmed01/markitdown).

## Commits

- `48d0f1164cb28c4620f1d59757d96befc3f66256` — Add --llm-client,
  --llm-model, and --llm-prompt options to the CLI (2 files, +253/−3)

## Problem

`llm_client`/`llm_model`/`llm_prompt` are first-class `MarkItDown(...)`
kwargs (`_markitdown.py` stores them and forwards them into every converter
call; `markitdown-ocr` reads them in `register_converters`), but the CLI had
no way to set them — the documented command in
`packages/markitdown-ocr/README.md:34` fails, and the CLI-only user cannot
use image/PPTX description or plugin OCR at all.

## Root Cause

`packages/markitdown/src/markitdown/__main__.py` never defined the flags nor
the plumbing; nothing else was missing (the Python API path has worked since
the kwargs were added).

## Solution

- Three argparse options: `--llm-client {openai}`, `--llm-model`,
  `--llm-prompt` (help texts document the pairing and the
  `OPENAI_API_KEY` source).
- Pairing validation via the file's existing `_exit_with_error` convention:
  client requires model; model/prompt without client exit 1 with an
  actionable message instead of being silently ignored.
- `_create_llm_client()` constructs `openai.OpenAI()` **lazily** (only when
  converting), so `openai` stays an optional dependency and
  `--list-plugins`/flagless usage are untouched; a missing `openai` package
  or missing API key produces a one-line actionable error, not a traceback.
- Resolved options are forwarded as `**llm_kwargs` on all three
  `MarkItDown(...)` constructor paths (default, `--use-docintel`, `--use-cu`),
  where the existing kwarg plumbing already hands them to the image/PPTX
  describers and to plugins.

## Files Changed

- `packages/markitdown/src/markitdown/__main__.py` — the three options, the
  validation block, `**llm_kwargs` at the three constructor call sites, and
  the `_create_llm_client()` helper (+62/−3)
- `packages/markitdown/tests/test_cli_misc.py` — new `TestLLMCLIArgs` class,
  9 tests, per `tests/README.md` ("CLI behavior outside the vector matrix"
  belongs here) (+194)

## Tests

- **Regression proof:** all 9 new tests fail against unmodified `main`
  (verified by restoring the original `__main__.py`: 9 failed), and pass with
  the fix.
- **Focused:** `uv run --extra all --with pytest pytest tests/test_cli_misc.py -q`
  → **29 passed** (20 baseline + 9 new; baseline captured before editing).
- **Neighbors:** `tests/test_cli_vectors.py` → **82 passed** (full CLI vector
  matrix); `tests/test_module_misc.py` → 159 passed, 11 skipped, 1 failed
  (`test_speech_transcription` — fails **identically on the unmodified base**;
  environmental, missing audio tooling).
- **Gates:** `black==23.7.0 --check` (the repo's pinned pre-commit hook) clean
  on both files; `mypy --ignore-missing-imports src/markitdown tests` reports
  **no issues in the changed files** (28 pre-existing errors in 9 untouched
  files, e.g. `test_pptx.py` Path/str); `git diff --check` clean.
- **Real-CLI smoke:** `--help` lists the flags; each error path
  (model-without-client, client-without-model, missing `openai`, missing
  `OPENAI_API_KEY`) exits with an actionable one-line message.

## Runtime Validation

No live OpenAI API call was made (no API key in this environment; live LLM
tests are env-gated in this repo anyway). Client construction, kwarg
forwarding, and every error path are covered with mocks and subprocess runs.

## CI

- 2026-10-14T17:53Z: license/cla QUEUED at PR creation; still pending at
  17:55Z. No other checks have reported yet. `mergeStateStatus: BLOCKED`
  (awaiting review + required checks — normal for a fresh PR).
- Note: PR #2699's license/cla passed within minutes historically, so a CLA
  pass is expected, but no green-CI claim is made until it reports.

## Review

- Copilot (`copilot-pull-request-reviewer`) left a COMMENTED bot review;
  **no human review yet**.

## Merge

Not merged. Open and awaiting review as of 2026-10-14T17:55Z.

## Lessons Learned

- A maintainer's written invitation ("a fresh PR against main would be very
  welcome") is the strongest acceptance evidence available — it also
  legitimizes opening in a lane with stale, unmergeable competition (#2277),
  provided the PR body says so explicitly.
- Closed-unmerged prior PRs must be read to distinguish REJECTED from
  ABANDONED; here both attempts died of neglect, not design disagreement.
- Pairing-validation error messages should name the missing flag, and client
  construction should be lazy so the base install stays dependency-free —
  both were cheap and are the kind of detail a reviewer checks first.
