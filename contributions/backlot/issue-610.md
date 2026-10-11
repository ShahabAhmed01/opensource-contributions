# brekkylab/backlot — #610

## Status

**CHANGES REQUESTED → RESPONSE PUSHED** — PR #614 opened 2026-10-11T08:32:38Z.
`nuriyoo` requested changes at 2026-10-11T08:52:43Z (first human review on this
PR). All four items applied and pushed by 2026-10-11T14:26:02Z (head `7abf5b4`);
reply comment posted at 14:29Z. CI 7/7 green on the response head. Awaiting
re-review. Not merged.

## Issue

https://github.com/brekkylab/backlot/issues/610
"slack: a bucket path ending in a slash is answered as an object whose key is empty, where real answers it as the bucket"
Labels: `bug`, `good first issue`, `help wanted`, `fidelity`, `hacktoberfest`

Unassigned, no competing PR, claimed by comment at 2026-10-11T08:19:36Z (issuecomment-6107066056).

## Pull Request

[#614 — s3: a bucket path ending in a slash is answered as the bucket, as real does](https://github.com/brekkylab/backlot/pull/614)

- Base branch: `main` (the repo's only development branch)
- Opened: 2026-10-11T08:32:38Z
- State: **open**, mergeable (all 7 checks green)
- Fork head: `ShahabAhmed01:contrib/issue-610-s3-bucket-slash`
- Closes: #610 (GitHub confirms the link)

## Branch

`contrib/issue-610-s3-bucket-slash` (from `upstream/main` @ `0c879173b`)

## Commits

- `4c2feb189fa26b5e417af15c0b487720f08bf075` — s3: a bucket path ending in a slash is answered as the bucket, as real does (fixes #610) (3 files, +5/−3)
- `9b1aad73b9e4481af7808160afa05ad23c141581` — test(s3): add regression test for trailing slash fix and ACL coverage (addresses review #614) (tests/test_s3.py, +31)
- `7abf5b4df7485ace2a435f042fbeae08486e7bd8` — tests: wrap the s3 alias comment at 100 columns (addresses review #614) (tests/test_openapi.py, +2/−1)

## Problem

`GET` or `HEAD /s3/{bucket}/` (with trailing slash) matches the object route `/{bucket}/{key:path}` with `key` = empty string, so Backlot answers it as a key lookup — returning `404 NoSuchKey` for listings and a key's refusal for sub-resources — where the real S3 API answers every such request as the bucket (the same as `/{bucket}` without the slash).

The issue measured 16 request pairs (8 queries × GET/HEAD) against s3.amazonaws.com (us-east-1) on 2026-10-11. Real S3 answers all 16 pairs identically. Backlot at `0c87917` answered 11/16 slashed paths differently (404 or key refusal).

## Root Cause

The router registers `GET /s3/{bucket}` and `HEAD /s3/{bucket}` for bucket operations, and `GET/HEAD /s3/{bucket}/{key:path}` for object operations. FastAPI/Starlette does not automatically redirect `/{bucket}/` to `/{bucket}` for signed requests (would break SigV4), and the object route's `{key:path}` parameter captures the empty string after the trailing slash.

The fix mirrors how `list_buckets` registers both `/s3` and `/s3/` (see module docstring in `backlot/routers/s3.py`).

## Solution

Two one-line route additions in `backlot/routers/s3.py`:

1. `@router.head("/{bucket}/")` on `head_bucket` (line 1024)
2. `@router.get("/{bucket}/", openapi_extra={"parameters": _P_BUCKET_GET})` on `bucket_get` (line 1068)

No new handlers, no behavior changes — the existing bucket handlers already implement the correct fidelity logic.

## Files Changed

- `backlot/routers/s3.py` — +2 route decorators (lines 1024, 1068)
- `docs/supported-sources.md` — auto-generated, endpoint count 4→5
- `tests/test_openapi.py` — expected `bucket_get` collapse in MCP spec (line 284)

## Tests

- **Regression proof:** the issue's 16-pair reproduction script fails 11/16 on unmodified main (slash ≠ no-slash), passes all 16 on the fix branch.
- **Maintainer-named regression test (2026-10-11):** `test_s3_a_bucket_path_ending_in_a_slash_is_the_bucket` — 8 queries × GET/HEAD = 16 cases comparing status, sorted header names and request-id-stripped body between `/{bucket}` and `/{bucket}/`. Replayed exactly as nuriyoo measured it: `backlot/routers/s3.py` restored to `main` → **15 of the 16 fail** (a HEAD with `?acl` already matched on main) plus the ACL test; fix restored → all 17 pass.
- **ACL rows (2026-10-11):** `("GET", "/s3/people-vault/", 200)` and `("HEAD", "/s3/people-vault/", 200)` appended to `test_s3_a_request_in_a_bucket_the_caller_cannot_see_is_nosuchbucket`.
- **Focused:** `pytest tests/test_s3.py tests/test_openapi.py` — pass on the review-response head.
- **Full suite (2026-10-11, review response):** `pytest` on a `.[dev,official-sdk,llamaindex]` install, Python 3.11 — **6351 passed, 10 skipped**, 0 failed. The 10 skips are the extras not installed here (`mcp`, `mirage`, `gdrive_fsspec`, `llama-index-readers-hubspot`); `test_s3.py` ran rather than self-skipping. (The original 2026-10-11 push recorded 6088/10 on a `.[dev]` run.)
- **Lint:** `ruff check . && ruff format --check .` — clean.
- **Prose check:** one pre-existing finding at `tests/test_google.py:6355`, a file this change does not touch.

## Runtime Validation

Bundled corpus (`backlot import backlot/data/hello.jsonl`) over `backlot.serve()`:

```
GET  /acme-artifacts        -> 200 ListBucketResult
GET  /acme-artifacts/       -> 200 ListBucketResult
GET  /acme-artifacts?list-type=2 -> 200 ListBucketResult
GET  /acme-artifacts/?list-type=2 -> 200 ListBucketResult
GET  /acme-artifacts?uploads     -> 200 ListMultipartUploadsResult
GET  /acme-artifacts/?uploads    -> 200 ListMultipartUploadsResult
GET  /acme-artifacts?versions    -> 200 ListVersionsResult
GET  /acme-artifacts/?versions   -> 200 ListVersionsResult
GET  /acme-artifacts?logging     -> 200 BucketLoggingStatus
GET  /acme-artifacts/?logging    -> 200 BucketLoggingStatus
GET  /acme-artifacts?encryption  -> 200 ServerSideEncryptionConfiguration
GET  /acme-artifacts/?encryption -> 200 ServerSideEncryptionConfiguration
GET  /acme-artifacts?max-keys=abc -> 400 InvalidArgument
GET  /acme-artifacts/?max-keys=abc -> 400 InvalidArgument
GET  /acme-artifacts?acl         -> 200 AccessControlPolicy
GET  /acme-artifacts/?acl        -> 200 AccessControlPolicy
```

All 16 GET pairs match. HEAD pairs similarly match (200 for listing, 405 for unsupported sub-resources on both sides).

## CI

- First push (2026-10-11T08:32Z): `gate`, `lint`, `scan`, `test (3.11)`–`test (3.14)` all passing; PR mergeable (`clean` state).
- Review-response head `7abf5b4` (2026-10-11T14:26Z): **7/7 green** — `gate`, `lint`, `scan`, `test (3.11)`, `test (3.12)`, `test (3.13)`, `test (3.14)`, verified at 14:31Z.
- No first-time-contributor `action_required` gate (previous merged PR #577 lifted the one-PR-at-a-time limit).

## Review

- `copilot-pull-request-reviewer` left a non-review: it could not review because the requester's quota was exhausted.
- **`nuriyoo` CHANGES_REQUESTED, 2026-10-11T08:52:43Z** — first human review. Confirmed the route change is right ("The change is right") and asked for four things:
  1. Nothing pinned the answer — add a parametrised test over the issue's eight queries on GET and HEAD comparing `/{bucket}` with `/{bucket}/` (exact code supplied, placement given). `tests/test_s3.py` was not in the diff, so the first checkbox had no test behind it; the three schema-reading tests that failed without the fix all read the schema and none sent a request to `/{bucket}/`.
  2. The second checkbox needed a scoped-token proof for the new path — two rows at the end of the `test_s3_a_request_in_a_bucket_the_caller_cannot_see_is_nosuchbucket` table.
  3. A **Not in this PR.** line in the description: the issue measured GET and HEAD only; `PUT`/`POST`/`DELETE`/`PATCH`/`OPTIONS` on `/{bucket}/` still reach `object_method_refusal` with key `""`.
  4. An inline wrap on `tests/test_openapi.py:283` (111 chars vs the file's 100-column wrap), with replacement text.
- Reviewer's own numbers, quoted for the record: 17 pass on the branch; with `s3.py` at `main`, 15 of the 16 and the ACL test fail; full suite on their side 6401 passed / 2 skipped (`.[all,dev]`, Python 3.13).
- Items 1, 2 and 3 were applied and pushed as `9b1aad7` at 09:06Z with the description updated; item 4 was still outstanding and was applied as `7abf5b4` at 14:26Z.
- **Correction made to our own description:** the original **Not in this PR.** paragraph said the object route was "declared before the bucket routes". That is false and was fixed rather than left standing — the bucket routes sit at `s3.py:1069-1070` and the object routes at `:1763` and `:2946`, so the object routes come *after*. Verified by measurement: with the two new decorators removed again, all five methods answer byte-identically, because the new decorators serve `GET` and `HEAD` only and those five never match them.
- Reply comment posted 2026-10-11T14:29Z (issuecomment-6110067054) listing each item, the regression replay and the corrected numbers. A PR author cannot formally re-request review; the reply notifies the reviewer.
- Awaiting re-review. PR reports MERGEABLE.

## Merge

**Not merged.** GitHub confirms PR #614 is OPEN and MERGEABLE at head `7abf5b4`, with CHANGES_REQUESTED outstanding from `nuriyoo` and no approval.

## Lessons Learned

- The fix pattern was already established in the codebase: `list_buckets` registers both `/s3` and `/s3/` to avoid SigV4-breaking redirects. Applying the same pattern to bucket operations is the minimal, correct fix.
- The issue's live-API measurement (16 pairs, 2026-10-11) is the acceptance criteria — no interpretation needed.
- Reusing existing handlers (`bucket_get`, `head_bucket`) means no new test surface, no ACL concerns, no new code paths to audit.
- The OpenAPI test needed a one-line update because the MCP spec now sees `bucket_get` at two paths (collapses like `list_buckets`).
- A maintainer who supplies the exact test code has already run it on the branch. Taking it verbatim (placement included) is faster and lower-risk than re-deriving an equivalent, and it makes the re-review a diff against what they expect to see.
- A reviewer's *causal explanation* deserves the same scrutiny as their requested change. The **Not in this PR.** paragraph we inherited a wrong reason from our own first draft ("the object route is declared before the bucket routes"). Source order disproved it (`s3.py:1069-1070` bucket vs `:1763`/`:2946` object), and removing the two decorators and diffing the five methods' answers byte-for-byte proved the correct reason: the new decorators serve only `GET`/`HEAD`, so the other five never match. Correcting the description in the same reply is better than leaving an accurate claim attached to an inaccurate reason.
- Re-running the maintainer's own regression replay (restore `s3.py` to `main`, count the failures) reproduced their number exactly — 15 of 16 plus the ACL test, with the `?acl` HEAD case already matching. Reproducing a reviewer's stated failure count is the cheapest way to prove you actually ran what you claim.
