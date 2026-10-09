# odysseus-dev/odysseus — #6464

## Status

In review

## Issue

https://github.com/odysseus-dev/odysseus/issues/6464
"Unable to authenticate to Radicale CALDAV behind Opencloud"

## Pull Request

[#6475 — fix(caldav): handle passwords with spaces in Basic auth (fixes #6464)](https://github.com/odysseus-dev/odysseus/pull/6475)

- Base branch: `dev`
- Opened: 2026-10-03
- State: open, mergeable
- Fork head: `ShahabAhmed01:fix/caldav-opencloud-token-spaces-6464`

## Branch

`fix/caldav-opencloud-token-spaces-6464`

## Commits

- `ce1fdbcdfdffbb3307df9e6e136df314e0c6c59a` — fix(caldav): handle passwords with spaces in Basic auth (fixes #6464)

## Problem

CalDAV authentication fails against Radicale behind Opencloud when the app
token contains spaces (six words separated by spaces), so the calendar
integration never authenticates.

## Solution

`_build_dav_client()` in `src/caldav_sync.py` now passes an explicit
`requests.auth.HTTPBasicAuth(username, password)` through the `auth` parameter
of `caldav.DAVClient()` instead of relying on the library's default handling of
the `username`/`password` arguments, so the raw password (spaces included) is
encoded into the `Authorization` header unchanged.

## Files Changed

- `src/caldav_sync.py` — explicit `HTTPBasicAuth` for `DAVClient`
- `tests/test_caldav_redirect_hardening.py` — new test asserting the client
  receives an `HTTPBasicAuth` carrying the raw spaced token, and that
  `session.max_redirects` is still pinned to `0`
- `tests/test_caldav_google_principal_url.py` — fake client accepts the `auth`
  parameter

## Tests

- Existing CalDAV tests (66) and calendar tests (184) pass
- New focused test: `test_build_dav_client_handles_password_with_spaces`
- Syntax: `compileall` clean
- SSRF protection unchanged: redirects remain disabled on the DAV session

## CI

PR checks passing (description, Conventional Commits, unmergeable). The
`CI`/`CodeQL`/scan workflows are `action_required` pending maintainer approval
for a first-time contributor — an expected gate, not a failure.

## Review

No maintainer review yet.

## Merge

Not merged.

## Notes

Reconciled against live GitHub state 2026-10-09.
