# honojs/hono — issue #5569

## Status

**FIX COMMITTED AND PUSHED, PUBLISHED AS AN ISSUE COMMENT WITH THE BRANCH
LINKED — NO UPSTREAM PR, AND NONE CAN BE OPENED FROM OUTSIDE.**

The commit `e13a1d279d20041f5a8abbd38ed68d7f17c8272d` is on the fork
`ShahabAhmed01/hono` at branch `fix/issue-5569-non-utf8-charset-445b0cd7`,
based on upstream `main` @ `5ca49b0720755c585c9a9835f0a479ceea36fb52`
(verified current at publication). The fix was published on 2026-10-20T16:42:08Z
as a comment on issue #5569 (comment `6296083976`,
https://github.com/honojs/hono/issues/5569#issuecomment-6296083976), which is
the route `docs/CONTRIBUTING.md` prescribes for outside contributors.

**Not merged.** Nothing is in review. There is no pull request, no CI run and
no human review, because `honojs/hono` sets
`pull_request_creation_policy: collaborators_only` and every PR-creation
attempt is refused. See "Why there is no pull request" below.

## Issue

https://github.com/honojs/hono/issues/5569
"Lambda adapters corrupt text responses declared as Shift_JIS"

Opened 2026-10-19T13:34:41Z by `Retr0413` (association `NONE`), with a full
byte-level reproduction: a `text/plain; charset=shift_jis` response holding
the six bytes of "テスト" (`83 65 83 58 83 67`) comes back from the AWS
Lambda adapter as `EF BF BD 65 EF BF BD 58 EF BF BD 67` — every non-UTF-8
byte replaced with U+FFFD — while the content type still claims Shift_JIS.
The same is reported for the Lambda@Edge adapter, and the issue notes the
`isContentTypeBinary` override as the lossless control.

Availability checked immediately before publication: **open, 0 comments, 0
assignees, no labels, not updated since creation**, and no pull request
references it (`repos/honojs/hono/issues/5569/timeline` had no
`cross-referenced` event; the 124 open PRs were swept for the issue number).

## Problem

`hono/aws-lambda`, `hono/lambda-edge`, `@hono/aws-lambda` and
`@hono/lambda-edge` all turn a Hono response into a Lambda/CloudFront result
with a body that is either base64 or text:

```ts
const body = isBase64Encoded ? encodeBase64(await res.arrayBuffer()) : await res.text()
```

`isBase64Encoded` is decided from the content type alone.
`defaultIsContentTypeBinary()` classifies `text/plain` as non-binary
whatever charset it declares:

```ts
return !/^text\/(?:plain|html|css|javascript|csv)|(?:\/|\+)(?:json|xml)\s*(?:;|$)/i.test(contentType)
```

so `text/plain; charset=shift_jis` took the `res.text()` branch.
`Response.text()` always decodes the body as UTF-8, and the WHATWG UTF-8
decoder replaces every invalid sequence with U+FFFD. The bytes are silently
lost, and nothing in the response indicates it — the content type still
promises Shift_JIS.

This is data corruption on the wire, not a rendering nit: a Lambda handler
returning Shift_JIS, ISO-8859-1, Windows-1252 or EUC-JP content delivers
mojibake to the client.

## Root Cause

The adapters conflate two different questions:

1. *Is this content type binary?* — answered by `defaultIsContentTypeBinary()`
   / `isContentTypeBinary()`.
2. *Can this body be decoded as UTF-8?* — never asked.

A `text/*` body may legitimately be encoded in any charset the response
declares, so question 1 cannot stand in for question 2.

## Solution

- New `isNonUtf8Charset(contentType)` helper, placed with the other content
  type helpers at the bottom of each adapter file. It reads the `charset`
  parameter out of the content type and reports whether the declared charset
  is something other than UTF-8:
  - the parameter is read quoted (`charset="shift_jis"`) and unquoted, with
    optional whitespace around `=`;
  - `utf-8` and the `utf8` alias count as UTF-8;
  - a content type with no charset parameter is unaffected;
  - a parameter that merely contains the substring `charset`
    (`text/plain; x-charset=foo`) is **not** a charset declaration, because
    the match is anchored on `;` + optional whitespace + `charset` + `=`.
- Both adapters base64 encode a response whose content type declares a
  non-UTF-8 charset, so the runtime decodes the body back to the original
  bytes before the response reaches the client. The content type itself is
  left untouched.
- The AWS adapter's decision is now
  `(!!contentType && isContentTypeBinary(contentType)) || isNonUtf8Charset(contentType)`,
  and the Lambda@Edge adapter's single `||` chain gained the same term. The
  existing `content-encoding` check is unchanged.
- `@hono/aws-lambda`'s README gained a short section: on an API Gateway REST
  API (payload format 1.0) the content type has to be listed in the API's
  **Binary Media Types** for API Gateway to decode the base64 body; HTTP APIs,
  Lambda Function URLs and ALB decode base64 bodies unconditionally.

The change is applied to all four shipped copies of the adapters —
`src/adapter/aws-lambda/handler.ts`, `src/adapter/lambda-edge/handler.ts`,
`adapters/aws-lambda/src/handler.ts` and `adapters/lambda-edge/src/handler.ts`
— which the repository keeps near-identical on purpose (they differ only in
import paths and `@deprecated` JSDoc).

## Files Changed

9 files, +329/−4, all under the adapter surface:

- `src/adapter/aws-lambda/handler.ts` — helper + `createResult()` decision
- `src/adapter/lambda-edge/handler.ts` — helper + `createResult()` decision
- `adapters/aws-lambda/src/handler.ts` — same change, published-package copy
- `adapters/lambda-edge/src/handler.ts` — same change, published-package copy
- `src/adapter/aws-lambda/handler.test.ts` — byte-level, table and
  end-to-end tests
- `src/adapter/lambda-edge/handler.test.ts` — byte-level and table tests
- `adapters/aws-lambda/src/handler.test.ts` — same tests, package copy
- `adapters/lambda-edge/src/handler.test.ts` — same tests, package copy
- `adapters/aws-lambda/README.md` — the Binary Media Types note

## Tests

- `test_should_encode_as_base64_when_the_content_type_declares_a_non_utf_8_charset`
  — the six Shift_JIS bytes come back as `isBase64Encoded: true` with the
  body `g2WDWINn` (the base64 of `83 65 83 58 83 67`).
- A table test pins the charset parsing in both adapters: `shift_jis` plain,
  quoted and with spaces, as a non-first parameter, plus `utf-8`, `UTF-8`,
  `utf8`, `"utf-8"`, no charset at all and `text/plain; x-charset=foo`.
- An end-to-end AWS test drives the whole `handle()` path with
  `c.body(shiftJis, 200, { 'Content-Type': 'text/plain; charset=shift_jis' })`
  and asserts `isBase64Encoded`, the base64 body **and** that the content
  type is retained unchanged.
- **Full suite:** `vitest run` → **145 files, 5251 passed, 46 skipped, 0
  failed**.
- **Adapter suites:** `vitest run src/adapter/aws-lambda/handler.test.ts
  src/adapter/lambda-edge/handler.test.ts` → 111 passed. `pnpm -r --filter
  "./adapters/aws-lambda" --filter "./adapters/lambda-edge" run test` → 100
  passed / 69 passed.
- **Static checks:** `tsc -p tsconfig.spec.json` clean, `vp lint` clean,
  `vp fmt --check` clean, `git diff --check` clean.
- **Regression proof:** the new tests fail without the fix — the adapter
  reported `isBase64Encoded: false` and the body was the replacement
  characters instead of the original bytes.

### Pre-existing failures that were not caused by this change

`build/declaration-emit.test.ts` (1 test) and `build/jsx-types.test.ts`
(4 tests) failed on the unmodified checkout with
`TS2307: Cannot find module 'hono'`: they resolve the built package, so they
need `dist/`. Reproduced identically on a stashed tree, then resolved by
`pnpm run build`, after which the whole suite is green. Environmental, not
caused by the patch.

## Independent review

A read-only reviewer (separate session, no write access to the checkout)
went over the whole diff and produced a 39-case regex matrix, a 26-case
content-type matrix, and per-file checks. It confirmed the regex on every
edge case it threw at it and found **two MAJOR findings**, both fixed before
the commit:

1. the lambda-edge "UTF-8 charset" control test was **vacuous** —
   `c.text(str, { headers })` lets Hono's default content type overwrite the
   user's (verified in `src/context.ts`: `setDefaultContentType()` merges the
   default first and `#newResponse()` applies the caller's headers second),
   so the test asserted nothing about the declared charset. It now uses
   `c.body('plain', 200, { 'content-type': 'text/plain; charset=utf-8' })`,
   whose content type survives, and uses a lowercase charset so a
   case-sensitivity bug would fail it.
2. the charset regex — which *is* the fix — had no direct coverage. It is now
   covered by the table test above.

It also raised two MINOR points that were acted on or documented: the
aws-lambda test bypassed the public `handle()` path (an end-to-end test was
added), and API Gateway REST APIs need the content type in their Binary Media
Types for a base64 body to be decoded (documented in the adapter README).
Its remaining notes — that a response declaring a non-UTF-8 charset but
holding only ASCII bytes now becomes base64 too, and the false-positive
`text/plain; x="a;charset=shift_jis"` case — are recorded in the published
issue comment and in the PR description that could not be opened.

## Why there is no pull request

`honojs/hono` sets `pull_request_creation_policy: collaborators_only` and
`docs/CONTRIBUTING.md` says it in words:

> **Issues instead of Pull Requests** — "Pull requests are limited to
> maintainers. If you find a bug or want a change, please create an issue
> instead… If you have already fixed it in your fork, you can link the branch
> in the issue. A maintainer may open a pull request from it, and your
> commits keep your name."

Every attempt to open a PR was refused, from several angles:

- `POST /repos/honojs/hono/pulls` → `404 Not Found`, for a same-repo head,
  for another user's fork, and for this run's fork branch;
- `gh pr create --repo honojs/hono` → GraphQL `FORBIDDEN` "does not have the
  correct permissions to execute `CreatePullRequest`", with and without an
  explicit `headRepositoryId`;
- the same request against `honojs/middleware` (same organisation, policy
  `all`) returns `422 Validation Failed`, so the token and the account are
  fine — the refusal is repository-scoped.

The repository's own instruction was followed instead: the fix is pushed to
the fork and the branch is linked in the issue, which is what the
CONTRIBUTING guide asks for and what lets a maintainer open the PR in one
step with the commit attributed to `ShahabAhmed01`. The comment also offers
to open the PR directly if a maintainer adds `ShahabAhmed01` as a
collaborator.

## Duplicate elimination

The live issue queue was swept before implementing, because several issues in
this batch carry announced fork fixes from other contributors:

- **#5567** (`JSON validator skips +json media subtypes containing digits`) —
  `Kamaldeep-singh0` announced a ready fix in a fork branch on 2026-10-17.
  No PR had been opened, but the work was claimed, so the issue was dropped.
  A first implementation of it (a one-line change to `jsonRegex` plus a
  regression test, 57/57 tests green) was written, verified, and then
  **discarded** rather than duplicated.
- **#5566** (`TrieRouter returns 404 when a regex parameter precedes a
  literal bracketed segment`) — same contributor, same announcement. Dropped.
- **#5564** (`ALBProcessor does not URL-encode decoded query parameters`) —
  `okarin1511` announced a fork fix and wrote that they could not open a PR
  "since the repo restricts that to collaborators". Dropped.
- **#5520** (`methodOverride retains stale Content-Length after rewriting a
  form body`) — the reporter's own PR **#5521** is open against it. Dropped.
- **#5569** — no comment, no announcement, no referencing PR. **Taken.**

The 124 open PRs were swept for references to the open issue numbers, and the
closed PR history was searched for the affected code (`jsonRegex`,
`isContentTypeBinary`, `+json`, `shift_jis`, `charset`) before implementing.

## Merge

Not merged. There is no pull request and therefore no merge, no merge commit
and no upstream commit. The state as of 2026-10-20T16:44Z: the fork branch
carries the commit, the issue carries the published comment, and the
maintainers hold the next move.

## Next action

Watch issue #5569 for a maintainer response. If a maintainer asks for the
patch in a different shape, or offers to open the PR from the branch, answer
on the same branch. If `ShahabAhmed01` is added as a collaborator, open the
pull request from `fix/issue-5569-non-utf8-charset-445b0cd7` with the
description already written for the PR body. Do **not** file a duplicate
issue or a second fork branch for this bug.

## Lessons Learned

- `pull_request_creation_policy` in the repository object is the cheapest
  possible gate check, and it is not visible in the README, the contributing
  guide or the web UI's visible fields until you look for it. Check it
  **before** writing a line of code, not after the branch is pushed.
- A repository's documented contribution route can be a real, complete
  contribution channel even when it is not a pull request. Reading
  `docs/CONTRIBUTING.md` early turned "the API refuses my PR" into "publish
  the branch in the issue", which is what the maintainers asked for.
- Sweeping the issue queue for *announced fork fixes* (a comment linking a
  branch) is as important as sweeping for open pull requests. Three of the
  four most attractive issues in this batch were already claimed that way,
  and one of them had no pull request at all.
- An independent reviewer that cannot edit the tree is worth its weight: it
  caught a test that asserted nothing, in a place where the default value
  silently overrode the value under test.
