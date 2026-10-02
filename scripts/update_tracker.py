#!/usr/bin/env python3
"""Synchronize the contribution tracker with live GitHub state.

Reads ``contributions-state.json``, queries GitHub through the ``gh`` CLI for
every tracked pull request (and its issue), updates the machine-readable state,
and regenerates the contribution tables in README.md and CONTRIBUTIONS.md
between the ``BEGIN/END CONTRIBUTIONS TABLE`` markers.

The script is idempotent: files are only rewritten when their content actually
changes, so running it repeatedly with unchanged remote state is a no-op.

Authentication: uses the ambient ``gh`` session locally, or the ``GH_TOKEN``
environment variable in GitHub Actions.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "contributions-state.json"
TABLE_FILES = [ROOT / "README.md", ROOT / "CONTRIBUTIONS.md"]
BEGIN_MARKER = "<!-- BEGIN CONTRIBUTIONS TABLE -->"
END_MARKER = "<!-- END CONTRIBUTIONS TABLE -->"

STATUS_LABELS = {
    "candidate": "Candidate",
    "issue-selected": "In progress",
    "issue-confirmed": "In progress",
    "implementation": "In progress",
    "tested": "In progress",
    "committed": "In progress",
    "pushed": "In progress",
    "pr-opened": "In review",
    "ci-running": "In review",
    "ci-failed": "CI failing",
    "changes-requested": "Changes requested",
    "changes-applied": "Changes applied",
    "approved": "Ready to merge",
    "ready-to-merge": "Ready to merge",
    "merged": "Merged",
    "closed-unmerged": "Closed",
    "superseded": "Superseded",
    "blocked": "Blocked",
}

CHECK_STATES = {
    "SUCCESS": "pass",
    "FAILURE": "fail",
    "ERROR": "fail",
    "CANCELLED": "fail",
    "TIMED_OUT": "fail",
    "ACTION_REQUIRED": "fail",
    "STARTUP_FAILURE": "fail",
    "PENDING": "pending",
    "QUEUED": "pending",
    "IN_PROGRESS": "pending",
    "WAITING": "pending",
    "REQUESTED": "pending",
    "NEUTRAL": "neutral",
    "SKIPPED": "skipped",
    "STALE": "skipped",
}


def gh_json(*args: str):
    """Run a gh command and parse its JSON output."""
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.strip()}"
        )
    text = result.stdout.strip()
    return json.loads(text) if text else None


def normalize_checks(rollup) -> dict:
    checks = {}
    for item in rollup or []:
        name = item.get("name") or item.get("context") or "check"
        raw = item.get("conclusion") or item.get("state") or "PENDING"
        checks[name] = CHECK_STATES.get(str(raw).upper(), str(raw).lower())
    return checks


def derive_status(pr: dict, checks: dict, reviews: list) -> str:
    state = pr.get("state")
    if state == "MERGED":
        return "merged"
    if state == "CLOSED":
        return "closed-unmerged"

    review_states = {r.get("state") for r in reviews}
    if "CHANGES_REQUESTED" in review_states:
        overall = "changes-requested"
    elif "APPROVED" in review_states:
        overall = "approved"
    else:
        overall = "pr-opened"

    values = set(checks.values())
    if "fail" in values:
        return "ci-failed"
    if "pending" in values:
        return "ci-running"
    if values and values <= {"pass", "skipped", "neutral"}:
        return "ready-to-merge" if overall == "approved" else "pr-opened"
    return overall


def sync_contribution(entry: dict) -> bool:
    """Update one contribution entry in place. Returns True if anything changed."""
    changed = False
    repo = entry.get("repo")
    if not repo:
        return False

    issue_number = entry.get("issueNumber")
    if issue_number:
        issue = gh_json(
            "issue", "view", str(issue_number), "--repo", repo,
            "--json", "state,title,updatedAt",
        )
        if issue:
            for field, value in (
                ("issueState", issue.get("state")),
                ("issueTitle", issue.get("title")),
                ("issueUpdatedAt", issue.get("updatedAt")),
            ):
                if value and entry.get(field) != value:
                    entry[field] = value
                    changed = True

    pr_number = entry.get("prNumber")
    if pr_number:
        pr = gh_json(
            "pr", "view", str(pr_number), "--repo", repo,
            "--json",
            "state,title,mergedAt,mergeCommit,statusCheckRollup,reviews,"
            "updatedAt,baseRefName,url",
        )
        checks = normalize_checks(pr.get("statusCheckRollup"))
        reviews = [
            {
                "author": (r.get("author") or {}).get("login"),
                "state": r.get("state"),
            }
            for r in pr.get("reviews") or []
        ]
        status = derive_status(pr, checks, reviews)
        merge_commit = pr.get("mergeCommit") or {}
        updates = {
            "prState": (pr.get("state") or "").lower() or None,
            "prTitle": pr.get("title"),
            "prUrl": pr.get("url"),
            "baseBranch": pr.get("baseRefName") or entry.get("baseBranch"),
            "checks": checks,
            "reviews": reviews,
            "status": status,
            "mergedAt": pr.get("mergedAt"),
            "mergeCommit": merge_commit.get("oid") if merge_commit else None,
        }
        for field, value in updates.items():
            if entry.get(field) != value:
                entry[field] = value
                changed = True

    return changed


def render_table(entries: list) -> str:
    rows = sorted(
        entries, key=lambda e: (e.get("openedAt") or ""), reverse=True
    )
    lines = [
        "| Date | Repository | Issue | PR | Status | Description |",
        "|---|---|---|---|---|---|",
    ]
    for entry in rows:
        date = (entry.get("openedAt") or "")[:10]
        repo = entry.get("repo", "")
        issue = entry.get("issueNumber")
        issue_cell = (
            f"[#{issue}]({entry.get('issueUrl')})" if issue else "—"
        )
        pr = entry.get("prNumber")
        pr_cell = f"[#{pr}]({entry.get('prUrl')})" if pr else "—"
        status = STATUS_LABELS.get(entry.get("status", ""), "In progress")
        description = entry.get("description", "")
        lines.append(
            f"| {date} | {repo} | {issue_cell} | {pr_cell} | {status} | {description} |"
        )
    return "\n".join(lines)


def replace_table(path: Path, table: str) -> bool:
    text = path.read_text(encoding="utf-8")
    start = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)
    if start == -1 or end == -1:
        return False
    new_text = (
        text[: start + len(BEGIN_MARKER)]
        + "\n"
        + table
        + "\n"
        + text[end:]
    )
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    entries = state.get("contributions", [])

    changed = False
    for entry in entries:
        try:
            if sync_contribution(entry):
                changed = True
        except RuntimeError as error:
            # Never corrupt the ledger on an API failure: keep the last
            # known-good values and report the failure.
            print(f"warning: {error}", file=sys.stderr)

    # Only touch timestamps when something actually changed, so an unchanged
    # remote state is a true no-op (no empty commits from the scheduler).
    if changed:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        state["updatedAt"] = now
        for entry in entries:
            entry["lastVerified"] = now

    table = render_table(entries)
    for path in TABLE_FILES:
        if replace_table(path, table):
            changed = True

    serialized = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    if write_if_changed(STATE_FILE, serialized):
        changed = True

    print("tracker updated" if changed else "tracker already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
