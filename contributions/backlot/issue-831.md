# brekkylab/backlot — #831

## Status

**PR #851 OPENED, CI 9/9 green** — opened 2026-10-19T12:01:53Z, ready
for review (not draft), base `main` @ `ff92bdd` (verified current at PR
creation and still the tip). All nine check-runs completed green:
`gate`, `lint`, `scan` and the test (3.11)–(3.15) matrix all success; the
bare `test` job is the workflow's skipped shape. `mergeable_state`
`blocked` on open (fork-lane first run), `clean` once the matrix
finished. Copilot left a COMMENTED bot review (recorded as a bot, not a
human review). Per policy, no pings. Not merged as of 2026-10-19T12:20Z.

## Issue

https://github.com/brekkylab/backlot/issues/831
"gmail: a quoted address value with a - in it matches the joined word,
where real matches nothing"

OPEN, unassigned, 0 comments, created 2026-10-19T06:02:06Z by `nuriyoo`
(found while reviewing the merged #805), labels `good first issue`,
`help wanted`, `fidelity`, `hacktoberfest`. Its timeline cross-references
are only merged #805 and the Hacktoberfest index issue — no competing PR
at selection, and 0 open PRs naming it re-checked by API immediately
before `POST /pulls`. The divergence is live on `main` at `ff92bdd`
(reproduced: the issue's script printed `1, 1, 1` on the base).

## Pull Request

[#851 — gmail: a quoted address value with a - in it finds its words
alone, as real reads it](https://github.com/brekkylab/backlot/pull/851)

- Base branch: `main` @ `ff92bdd01c423b833a96c0ece823265c47d0e6be`
  (verified current at PR creation)
- Opened: 2026-10-19T12:01:53Z · State: open, mergeable, `clean`, not
  draft
- Fork head: `ShahabAhmed01:contrib/issue-831-gmail-quoted-address-value`
  @ `cbe2c61e4861da3654934507b3a1f24866436685` (verified by
  `ls-remote` before the PR was opened)
- Closes #831 (`Closes #831.` first line of the body)
- Size: 3 files, +36/−13

## Branch

`contrib/issue-831-gmail-quoted-address-value`, cut from
`upstream/main` @ `ff92bdd` in an isolated worktree
(`~/opensource-work/backlot-831`, from the `~/opensource-work/backlot`
clone — the main checkout's uncommitted confluence-`expand` work for
#792 was left untouched, as was its branch). Commit
`cbe2c61e4861da3654934507b3a1f24866436685`, pushed to the fork and
verified by `ls-remote` (SHA match) before the PR was opened.

## Commits

- `cbe2c61e4861da3654934507b3a1f24866436685` — gmail: a quoted address
  value with a - in it finds its words alone, as real reads it (3 files,
  +36/−13)

## Problem

`GET /gmail/v1/users/me/messages?q=from:"no-reply"` against a mailbox
whose sender is `noreply@shop.example` returned that message, where
gmail.googleapis.com answers none: `_parse_gmail_q` stripped the quotes
before storage, so the matcher could not tell `from:"no-reply"` from
`from:no-reply` and ran the hyphen-joined alternative — `no-reply` →
`noreply` — on a value real reads as words alone.

## Root Cause

`_take` in `backlot/routers/google.py` appended `value.strip('"')` for
every operator, discarding the quoting that `_GMAIL_OP` had captured;
`_gmail_address_match` then had no way to gate its joined-spelling
alternative, whose rule ("unless it holds `--` or a `.`") never mentioned
quoting. The docstring had already recorded the measured reading — a
quoted value found its words alone — but no code implemented it.

## Solution

- `_take` keeps the surrounding quotes on a quoted `from:`/`to:`/`cc:`/
  `bcc:` value (`quoted = key in _GMAIL_ADDRESS_KEYS and len(value) > 1
  and value[:1] == value[-1:] == '"'`); `subject:`, `label:`, `in:` and
  `has:` keep the old stripping, so only the operators real reads
  differently carry the marker.
- `_gmail_address_match` strips one quote pair first (so the
  exact-address path `from:"lena@acme.com"` behaves as before) and skips
  the joined alternative only when the value came quoted.
- The `me` substitution in `_gmail_query` compares through the quotes
  (`v.strip('"').lower() == "me"`), preserving `from:"me"` exactly.
- Lone `"` (`from:"`, issue #828's separate divergence) and `from:""` are
  untouched: the `len > 1` guard and the quote-pair test leave both on
  their old path.

## Files Changed

- `backlot/routers/google.py` — storage condition in `_take`, quote
  handling and the measured rule in `_gmail_address_match`'s docstring,
  `me` substitution (+23/−8)
- `tests/test_google.py` — six new rows in
  `test_gmail_hyphenated_address_search` over both listings (+9/−1)
- `tests/test_search.py` — three parse expectations pin the quotes
  reaching the matcher (+5/−4)

## Tests

- **Regression proof run:** with `backlot/routers/google.py` stashed to
  its base revision and the new rows in the tree, ten of the twelve new
  cases fail — the four quoted operators and `from:"jt-snowball"`, on
  both `messages` and `threads` — while the control row
  `from:"noreply"` passes either way; the three `tests/test_search.py`
  parse rows fail likewise (verified independently by a read-only review
  agent in a scratch copy). With the fix, all pass.
- **Full suite (zero-skip install):** `pytest -rs` on
  `uv pip install -e ".[all]"` (uv, Python 3.14.8): **11034 passed,
  3 skipped in 186s.** The three skips are environmental and none is
  gmail: `test_mcp.py:154` (Docker not available), `test_mcp.py:196`
  (npx not available), `test_llamaindex.py:127`
  (`llama_index.readers.hubspot` not importable).
- **CI-mode suite:** `PYTHONWARNDEFAULTENCODING=1 pytest` — 8184 passed,
  38 skipped on the earlier `.[dev]` install (the same three skips are
  in the `.[all]` numbers; the other 35 are the extra-gated surfaces
  `.[all]` opens).
- **Lint:** `ruff check .` clean; `ruff format --check .` — 159 files
  already formatted; `ruff check --preview --select PLW1514 .` clean.
- **Prose gate:** `python scripts/prose_check.py` exits 1 on four
  findings byte-identical to its output on a clean `main` tree (verified
  by stashing all changes and re-running) — none sits on a line this
  change adds; the new measurement date lives in the router docstring
  only, no test line dates it.
- **Diff hygiene:** `git diff --check` clean; independent read-only
  review (path trace of every ops consumer, edge cases `no"reply`,
  `reply"`, `"reply`, `""`, `"lena@acme.com"`, `me`, negated forms,
  mutation run of the new rows) found no critical or major issue; its
  two wording findings were applied before the commit.

## Runtime Validation

No live gmail.googleapis.com call from this environment (no Google
token). The acceptance measurement is the issue's own
gmail.googleapis.com matrix (603-message Workspace mailbox,
2026-10-19, eight words across the four operators), transcribed into
the `_gmail_address_match` docstring beside the rule; the issue's
reproduction script runs locally over `backlot.serve()` and moved from
`1, 1, 1` (base) to `1, 1, 0` (fix) — real's answers `1, 1, none`.

## CI (live at 2026-10-19T12:16Z)

- gate: success · lint: success · scan: success
- test (3.11): success · test (3.12): success · test (3.13): success ·
  test (3.14): success · test (3.15): success
- bare `test`: skipped (workflow shape)
- 9/9 check-runs completed, none failing; `mergeable_state: clean`.
- Copilot (bot) COMMENTED — not a human review.

## Review

None yet — awaiting maintainer review (`nuriyoo`/`khj809` by history;
sixth backlot contribution, all five previous ones reviewed or merged
directly by `nuriyoo`).

## Merge

Not merged. Open, mergeable, `mergeable_state: clean` as of
2026-10-19T12:16Z, awaiting the first human review.

## Lessons Learned

- The maintainer's own issue text is the acceptance contract: the
  eight-word matrix pinned both the failing side and the control
  (`op:"<word>"` must not move), so the test rows could encode both.
- Preserving an input's shape through a parser (`"quoted"` vs unquoted)
  beats special-casing the divergence at the matcher: three parse-level
  expectations changed representation, but every observable behavior
  except the reported one stayed byte-identical, which the full suite
  then proved.
- Two shell commands that both touch the working tree (a formatter and a
  stash round-trip) must not run in parallel: the race stashed the test
  edits mid-run and needed a `git restore --source=stash@{0}` recovery,
  verified file-by-file before continuing.
