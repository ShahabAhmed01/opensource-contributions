# jupyter/jupyter_client — issue #1147

## Status

**PR #1155 OPENED, MERGEABLE, AWAITING FIRST HUMAN REVIEW — NOT MERGED**
— opened 2026-11-05T20:38:07Z, non-draft, base
`main@978361b3785dcd9cba6c733f4555e833e88fc0df`, head
`991fa2d8a9c83090f27d305f4ad5a1f8c247d01a`, branch
`fix/windows-kernel-handle-leak` on `ShahabAhmed01/jupyter_client`,
5 files (+34/−3 plus the new test module).

Verified remote state at record time: `state: OPEN`,
`mergeable: MERGEABLE`, `mergeStateStatus: BLOCKED` (expected for a
fresh fork PR), `pre-commit.ci - pr: PASS`,
`docs/readthedocs.org:jupyter-client: PASS`. The three GitHub Actions
workflows (`CI`, `Test downstream projects`, `Enforce PR label`) are
`action_required` — first-time-contributor approval gate, no check runs
yet. `copilot-pull-request-reviewer` commented that it could not review
because the requester's quota was exhausted (not a human review).

## AI / automated contributions disclosure

The PR body carries the agent disclosure and the two robot emojis
required by the IPython contributing guide (which jupyter_client's
CONTRIBUTING.md adopts). The commit subject also carries 🤖🤖. The work
was developed with an autonomous coding agent (OpenCode) and validated
in-run; the AI disclosure is explicit in the PR text.

## Issue

https://github.com/jupyter/jupyter_client/issues/1147
"Windows: launch_kernel leaks two handles per kernel (interrupt event
and parent-handle duplicate)"

Filed 2026-10-21 by `MichengLiang`, OPEN, unassigned, zero comments,
zero linked or closing PRs at selection (2026-11-05, 16 days later).
The report was complete: it identified both leaked handles, linked the
exact lines at `main@978361b`, supplied a standalone Windows repro
script with before/after output, and proposed the fix direction. The
reporter ended with "Happy to open a PR along these lines if this
direction looks right", but no maintainer replied and no PR was opened,
so this run implemented that direction and credits the reporter in the
PR body.

## Root cause

On `win32`, `launch_kernel` creates two process-owned handles per
kernel:

1. an inheritable interrupt event (`JPY_INTERRUPT_EVENT`), stored on
   the returned `Popen` object as `win32_interrupt_event` and used by
   `LocalProvisioner.send_signal`;
2. an inheritable duplicate of the current process handle, passed to
   the child as `JPY_PARENT_PID`.

Nothing closed either handle in the launching process. A garbage
collection does not release raw Win32 handles. The child uses only its
own inherited copies (`ipykernel.kernelapp` / `ParentPollerWindows`),
so the launcher's parent-handle copy is unused after `Popen` returns,
and the interrupt event is dead once the kernel process is reaped.

Measured on the unmodified base: 175 → 225 → 245 → 266 handles over 30
sequential kernel start/execute/shutdown cycles (two per kernel plus
startup noise).

## Implementation

- `jupyter_client/launcher.py`: retain the `DuplicateHandle` result and
  call `_winapi.CloseHandle` immediately after `Popen` succeeds. If
  `Popen` raises, close the duplicated parent handle and the interrupt
  event before re-raising, so a failed spawn leaks neither.
- `jupyter_client/win_interrupt.py`: add
  `close_interrupt_event(handle)` wrapping `kernel32.CloseHandle`.
- `jupyter_client/provisioning/local_provisioner.py`: close the event
  when `wait()` releases the process, and in `cleanup()` as a fallback
  for shutdown paths that never call `wait()`. The helper clears
  `proc.win32_interrupt_event`, so the second close is a no-op — exactly
  one `CloseHandle` per created event, including restarts.
- `tests/test_launcher.py` (new): exercise the Win32 branch
  cross-platform with a fake `_winapi`; verify the parent handle is
  closed after spawn and both handles are closed on `Popen` failure.
- `tests/test_provisioning.py`: `TestLocalProvisionerWindowsHandles`
  covers closure in `wait()`, in `cleanup()`, and no double-close when
  both run.

## Verification

Environment: Windows 11, Python 3.14.10, editable jupyter_client 8.10.0,
ipykernel 7.4.0, psutil 7.2.2.

- Independent handle-count repro (30 kernels): 175 → 225 → 245 → 266 on
  unmodified upstream versus 174 → 204 → 204 → 205 with the fix (flat
  after the one-time startup handles).
- Red/green: with the source fix stashed, all 5 new tests fail; with the
  fix, 18 targeted tests pass.
- Full suite: 246 passed, 33 skipped, 8 deselected. The deselection is
  `tests/test_kernelmanager.py::TestParallel`; its signalkernel timeout
  reproduces identically on unmodified upstream.
- Ruff 0.15.12 `check` and `format --check` clean on the five changed
  files. Mypy 1.20.2 shows no new real error against the 23-error
  Windows-local baseline (one `unreachable` suppression added for the
  `cleanup()` fallback).

## Coordination / publication

- Reserved `jupyter/jupyter_client#1147` in
  `ShahabAhmed01/opensource-contributions` branch
  `automation-coordination` under run
  `ossrun-20261105T184918Z-a2a369ea`; registry tip at reservation
  `a5f8b2627c034f38c9b1b55328d503939c2f8e0e`.
- Registry flipped to `PR_PUBLISHED` with the PR URL and head SHA and the
  tracker-writer lease acquired at commit `0f4e1cb`.
- Two earlier candidates of this run were blocked and released without
  tracker records: `pallets/flask#6182` (collaborator-only PR creation)
  and `sphinx-doc/sphinx#14817` (AI policy forbids autonomous agent PR
  submission).

## Next action

Awaiting maintainer approval of the Actions workflows and human review.
No code change is pending; if CI surfaces a Windows-specific failure,
re-run the targeted suite on this host and push a fix to the same
branch.
