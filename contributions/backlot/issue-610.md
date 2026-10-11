# brekkylab/backlot — #610

## Status

**IN REVIEW** — PR #614 opened 2026-10-11T08:32:38Z, all CI checks passing (gate, lint, scan, test 3.11-3.14). Awaiting maintainer review.

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
- **Focused:** `pytest tests/test_s3.py` — 211 passed (all S3 tests pass).
- **Full suite:** `pytest` on `.[dev]` install — 6088 passed, 10 skipped.
- **Optional surfaces:** `.[official-sdk]` (S3 SDK tests), `.[llamaindex]`, `.[mcp]`, `.[mirage]`, `.[fsspec]` all ran.
- **Lint:** `ruff check . && ruff format --check .` — clean.
- **Prose check:** pre-existing finding in `tests/test_google.py` (unrelated).

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
- No first-time-contributor `action_required` gate (previous merged PR #577 lifted the one-PR-at-a-time limit).

## Review

- `copilot-pull-request-reviewer` may leave a generic bot summary.
- Awaiting human review from `nuriyoo`/`khj809` (typical response within hours based on 15/15 recent external merges).

## Merge

Not yet merged. PR is open and mergeable.

## Lessons Learned

- The fix pattern was already established in the codebase: `list_buckets` registers both `/s3` and `/s3/` to avoid SigV4-breaking redirects. Applying the same pattern to bucket operations is the minimal, correct fix.
- The issue's live-API measurement (16 pairs, 2026-10-11) is the acceptance criteria — no interpretation needed.
- Reusing existing handlers (`bucket_get`, `head_bucket`) means no new test surface, no ACL concerns, no new code paths to audit.
- The OpenAPI test needed a one-line update because the MCP spec now sees `bucket_get` at two paths (collapses like `list_buckets`).
