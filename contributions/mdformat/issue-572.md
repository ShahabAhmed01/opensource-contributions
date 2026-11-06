# hukkin/mdformat — issue #572

## Status

**PR #602 OPENED, AWAITING FIRST HUMAN REVIEW — NOT MERGED** — opened
2026-11-06T09:33:32Z, non-draft, base `master@56b24ef0c6cfdab501844925971204f858185547`,
head `9cceeea9fb2bdd626ddfe8c1af420dd2bd4eda5b`, branch
`fix/572-html-comment-spacing` on `ShahabAhmed01/mdformat`, 4 files
(+91/−11). GitHub reports the PR MERGEABLE.

Verified remote state at publication: `docs/readthedocs.org:mdformat` PASS;
`pre-commit.ci - pr` ERROR **before any hook ran** — pre-commit.ci failed to
build the third-party `hukkin/docformatter` hook environment under Python
3.14 (`AttributeError: 'Constant' object has no attribute 's'` from
docformatter's setup.py during `pip install .`), twice, on the merged ref
`2e0469f`. This is upstream CI infrastructure, unrelated to the diff (no
hook reached our files). No GitHub Actions checks reported. Local checks
black/flake8/mypy on the changed file are clean.

## AI / automated contributions disclosure

There is no upstream AI policy in mdformat; the PR body carries a voluntary,
explicit disclosure (agent: OpenCode; model: DeepSeek V4.1 Flash Free;
autonomous, run `ossrun-20261105T213846Z-61850b7d`; extent: implementation,
tests, docs, evidence). The functional commit is the agent's own work; no
human review is claimed.

## Issue

https://github.com/hukkin/mdformat/issues/572
"Formatting over HTML comments crates newline between each comment"

Filed 2025 (metadata: created 2025-06-2x, `bug` label), still OPEN,
unassigned, one comment, no linked PR at selection or at publication.
The reporter uses [mark](https://github.com/kovetskiy/mark) to publish
Confluence metadata comments (`<!-- Space: MyGroup -->` …), which mdformat
spread out with blank lines; a commenter (fchastanet, 2026-03-21) hit the
same shape with `<!-- markdownlint-disable-next-line MD013 -->`, which
mdformat detaches from the line it guards and thereby breaks markdownlint.

## Root cause

`make_render_children(separator)` joins a node's rendered children with the
given separator, and the root/blockquote/loose-list renderers pass
`"\n\n"`, so **every** HTML block gets a blank line after it — including
HTML comments that are meant to modify the block that follows them. An HTML
comment ends at `-->` and needs no following blank line to parse, so the
extra line is pure presentation damage.

Repro (`printf -- '<!-- test -->\n<!-- test2 -->' | mdformat -`): baseline
inserts a blank line between the two comments.

## Implementation

One functional commit `9cceeea` ("fix: keep HTML comments attached to the
following block"), 4 files +91/−11 against `master@56b24ef`:

- `src/mdformat/renderer/_context.py`:
  - add `_is_html_comment()` (`html_block` whose content starts with `<!--`);
  - `make_render_children(separator, *, attach_html_comments=True)` emits a
    single newline after an HTML comment instead of the configured
    separator (document/root and block-quote paths keep the default);
  - `list_item` passes `attach_html_comments=False` — a blank line between
    blocks in a list item can determine tight vs. loose, and the CLI's
    `is_md_equal` safety check would (correctly) reject a change that
    tightens a list.
- `tests/data/default_style.md`: four regression cases (adjacent root
  comments + `markdownlint-disable-next-line`; the same in a block quote;
  a non-comment HTML block that must keep the blank line; a loose list
  item that must keep its blank line).
- `docs/users/style.md`: document the rule and the list-item exception.
- `README.md`: drop blank lines after section-marker comments so the repo's
  own docs remain mdformat-formatted (`test_for_profiler`).

## Verification

Environment: Windows 11, Python 3.14.10, editable install.

- Red/green against the new fixture cases: baseline (`56b24ef`) fails the
  root and block-quote cases (2 failures), patched passes all four (0).
- Issue repro and the markdownlint-directive case produce the expected
  output; `mdformat --check README.md` fails on baseline and passes patched.
- Focused suite: 28 passed, 1 pre-existing Windows symlink failure
  (`WinError 1314`); `test_for_profiler`: 1 passed.
- Full suite: 4 failed, 4281 passed, 2 skipped — the four failures are the
  pre-existing Windows failures (3 symlink `WinError 1314`,
  `test_check__multi_fail`), identical on the unpatched baseline in the same
  environment.
- black/flake8 (repo `.flake8`)/mypy clean on the changed source file;
  `git diff --check` clean.
- 2,184 generated block combinations (comments, text, headings, lists, block
  quotes, fences, non-comment HTML blocks joined by one or two newlines)
  checked for idempotency (`format(format(x)) == format(x)`) and HTML
  equivalence (`is_md_equal`): 0 failures.

No changelog entry: the changelog documents Python API/CLI breaking changes;
this is a formatting-style fix.

## Coordination / publication

- Reserved `mdformat #572` in the shared automation-coordination registry
  (`registry-live.json`, run `ossrun-20261105T213846Z-61850b7d`, acquired
  2026-11-06T07:24:13Z).
- Discovered via a breadth-first sweep (100 filtered candidates across 18
  repos + 15 more repos) and scored top-5; open PRs already covered other
  finalists (AnyIO #1452, dateutil #1653, coveragepy #2358), several repos
  were excluded by policy (sphinx-doc, pandas, Pallets, networkx, Textual,
  rich, jsonschema).
- Publication: created fork `ShahabAhmed01/mdformat`, pushed
  `fix/572-html-comment-spacing`, PR opened at 09:33:32Z via
  `gh pr create` (`executablebooks/mdformat` redirects to `hukkin/mdformat` —
  recorded under the canonical slug).

## Next action

Awaiting human review. If maintainers prefer no attachment inside list
items to also apply only when the list would stay loose, the conservative
clause is isolated to one boolean argument and easy to adjust. If
pre-commit.ci keeps erroring on the docformatter hook, that is the hook's
under-Python-3.14 build, not this PR.
