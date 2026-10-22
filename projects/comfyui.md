# Project notes — Comfy-Org/ComfyUI

Last verified: 2026-10-22

## Facts

- Node-graph UI for diffusion-model workflows: Python backend in this
  repo, frontend shipped as the `comfyui-frontend-package` wheel (web
  root read from site-packages). GPL-3.0; 141,980 stars / 16,740 forks
  (live 2026-10-22; trending +3,948 stars/week observed 2026-10-22).
  Very high push frequency — `master` advanced 3 commits while this
  session's PR was open (`1a82e6d` → `a071826`, 0 conflicts with the
  branch).
- Default branch `master` (not `main`); PRs target `master`. Core
  execution lives in `execution.py` (validation, executor,
  `PromptQueue`), API surface in `server.py`.
- Test setup: `uv venv --python 3.12`, `uv pip install -r
  requirements.txt -r tests-unit/requirements.txt` plus CPU torch from
  the pytorch index; execution tests boot a real server per class
  through the fixture in `tests/execution/test_execution.py`, which
  spawns `'python'` **from `PATH`** (system Python here), so runs must
  set `PATH="$PWD/.venv/bin:$PATH"`. CI reference commands:
  `python -m pytest tests/execution -v --skip-timing-checks`,
  `python -m pytest tests-unit`, `ruff check .` (ruff is NOT run in
  format mode), `pylint comfy_api_nodes` (only that package).
- The `tests/execution` asset-enabled server (4th fixture config)
  health-checks at teardown: it seeds and then requires ≥1 file in the
  output directory, so a single-test run that writes no images fails
  that check — pair the new test with an image-writing test locally
  (CI runs the whole suite, which populates output).
- Contribution policy: `AGENTS.md` is written for agents and demands
  hand-written-quality output (short PR descriptions: problem,
  behavioural change, tests — no implementation diaries; short direct
  commit subjects like `Fix ...`/`Add ...`).
- `.github/scripts/check-ai-co-authors.sh` FAILS any PR commit with an
  AI-agent `Co-authored-by` trailer (Claude/Cursor/Copilot/OpenAI/
  OpenCode/…): commit with the plain account identity, no trailers,
  and run the script locally before pushing.
- CLA: the `CLA Assistant Lite bot` comments on first PR; the PR author
  replies with exactly `I have read and agree to the Contributor
  License Agreement`, then the bot confirms signing and the
  `cla-assistant` check passes.
- First-time-contributor gate: all six repo workflows sit at
  `action_required` until a maintainer approves the run — a platform
  protection, not a failing check; do not try to bypass it and do not
  ping. Copilot review may come back quota-limited (COMMENTED only).
- External PRs merge routinely (#17224, #17241 observed 2026-10-22).

## `__value__` wrapper facts

- A bare list in a prompt means a node link `[node_id, slot]`
  (`is_link()` = list, len 2, `str` + number), so list widget values
  are transported as `{"__value__": [...]}` — an internal
  frontend↔execution convention; the only server-side readers are
  `validate_inputs()` and (since PR #17303) `get_input_data()`.
- `validate_inputs()` iterates exactly `required ∪ optional` declared
  inputs (not `hidden`, not undeclared) and unwraps `__value__` into a
  local value; before PR #17303 it also wrote the bare value back into
  the prompt, which is what stripped history/PNG storage (#17294).
- History shape: `GET /history/{prompt_id}` returns
  `{prompt_id: {"prompt": <queue item list>, "outputs": …}}` where the
  queue item is `(number, prompt_id, prompt_dict, extra_data,
  outputs_to_execute, sensitive)` — the submitted prompt dict is
  `history["prompt"][2]`.
- Concurrent lanes to avoid duplicating: #13095 (open, BOUNTY #8889 —
  removes tokens from history items; touches `execution.py` but a
  different concern), #13484 (merged — MultiCombo serialization),
  #15729 (closed).

## Acceptance record

- Issue #17294 and PR #17303 were opened 2026-10-22. At the time of
  writing, the CLA is signed, four external checks are green (CodeRabbit
  APPROVED after its own recommended gate was applied), the six repo
  workflows await first-time-contributor approval, and there is no
  human review (`reviewDecision: REVIEW_REQUIRED`). The fix is 3 files,
  +49/−2, with a red/green regression test across all four server
  configurations.
