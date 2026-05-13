#!/usr/bin/env python3
"""
Deterministic helpers for the jira-updater skill.

This script validates local request contracts before Atlassian MCP is used for
live Jira metadata checks or mutations.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path

APPROVAL_ALLOWLIST = [
    "approved",
    "yes, create it",
    "yes, update it",
    "proceed",
]

ISSUE_SCHEMAS = {
    "Epic": {
        "top_heading": "# Epic",
        "ordered_headings": [
            (2, "Jira Project", False),
            (2, "Issue Type", False),
            (2, "Title", True),
            (2, "Fix Versions", True),
            (2, "Priority", True),
            (2, "Assignee", True),
            (2, "Reporter", True),
            (2, "Jira Status or Phase", True),
            (2, "Business Objective", True),
            (2, "Scope", True),
            (3, "Included", True),
            (3, "Excluded", True),
            (2, "Success Metrics", True),
            (2, "Stakeholders", True),
            (2, "Risks / Dependencies", True),
            (2, "Related Stories", True),
        ],
    },
    "Story": {
        "top_heading": "# Story",
        "ordered_headings": [
            (2, "Jira Project", False),
            (2, "Issue Type", False),
            (2, "Title", True),
            (2, "Fix Versions", True),
            (2, "Priority", True),
            (2, "Assignee", True),
            (2, "Reporter", True),
            (2, "Jira Status or Phase", True),
            (2, "Parent Epic", True),
            (2, "Business Problem", True),
            (2, "Desired Outcome", True),
            (2, "Users / Stakeholders", True),
            (2, "Data Sources", True),
            (2, "Acceptance Criteria", True),
            (2, "Success Metrics", True),
            (2, "Dependencies", True),
            (2, "Suggested Sub-tasks", True),
        ],
    },
    "Task": {
        "top_heading": "# Task",
        "ordered_headings": [
            (2, "Jira Project", False),
            (2, "Issue Type", False),
            (2, "Title", True),
            (2, "Fix Versions", True),
            (2, "Priority", True),
            (2, "Assignee", True),
            (2, "Reporter", True),
            (2, "Jira Status or Phase", True),
            (2, "Parent Epic", True),
            (2, "Objective", True),
            (2, "Technical Details", True),
            (2, "Risks / Impact", True),
            (2, "Validation Requirements", True),
            (2, "Dependencies", True),
        ],
    },
    "Bug": {
        "top_heading": "# Bug",
        "ordered_headings": [
            (2, "Jira Project", False),
            (2, "Issue Type", False),
            (2, "Title", True),
            (2, "Fix Versions", True),
            (2, "Priority", True),
            (2, "Assignee", True),
            (2, "Reporter", True),
            (2, "Jira Status or Phase", True),
            (2, "Parent Epic", True),
            (2, "Problem Description", True),
            (2, "Expected Behavior", True),
            (2, "Actual Behavior", True),
            (2, "Business Impact", True),
            (2, "Severity", True),
            (2, "Affected Systems", True),
            (2, "Affected Data Sources", True),
            (2, "Root Cause (If Known)", True),
            (2, "Reproduction Steps", True),
            (2, "Validation Requirements", True),
            (2, "Dependencies", True),
            (2, "Suggested Sub-tasks", True),
            (2, "Attachments / References", True),
            (2, "Definition of Done", True),
        ],
    },
    "Sub-task": {
        "top_heading": "# Sub-task",
        "ordered_headings": [
            (2, "Jira Project", False),
            (2, "Issue Type", False),
            (2, "Title", True),
            (2, "Fix Versions", True),
            (2, "Priority", True),
            (2, "Assignee", True),
            (2, "Reporter", True),
            (2, "Jira Status or Phase", True),
            (2, "Parent Issue", True),
            (2, "Objective", True),
            (2, "Technical Requirements", True),
            (2, "Definition of Done", True),
            (2, "Dependencies", True),
        ],
    },
}

HEADING_ALIASES = {
    "Fix Version": "Fix Versions",
}

ACTION_PATTERNS = [
    ("assigned-to-me", re.compile(r"\b(assigned to me|my jira issues|issues assigned to me)\b", re.IGNORECASE)),
    ("add-attachment", re.compile(r"\b(add|attach|upload)\b.*\battachment\b|\battach\b", re.IGNORECASE)),
    ("add-comment", re.compile(r"\b(add|post|leave)\b.*\bcomment\b|\bcomment on\b", re.IGNORECASE)),
    ("update", re.compile(r"\bupdate\b", re.IGNORECASE)),
    ("create", re.compile(r"\bcreate\b", re.IGNORECASE)),
]

ISSUE_KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")
HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+?)\s*$")


def detect_action(text: str) -> dict:
    matched_actions = []
    matched_phrases = []
    for action_name, pattern in ACTION_PATTERNS:
        match = pattern.search(text)
        if match:
            matched_actions.append(action_name)
            matched_phrases.append(match.group(0))

    result = {
        "ok": len(matched_actions) == 1,
        "input": text,
        "actions": matched_actions,
        "matched_phrases": matched_phrases,
        "issue_keys": ISSUE_KEY_PATTERN.findall(text),
    }

    if not matched_actions:
        result["error"] = "Missing explicit action verb."
    elif len(matched_actions) > 1:
        result["error"] = "Multiple action verbs detected."
    else:
        result["action"] = matched_actions[0]

    return result


def check_approval(text: str) -> dict:
    normalized = " ".join(text.strip().lower().split())
    return {
        "approved": normalized in APPROVAL_ALLOWLIST,
        "input": text,
        "normalized": normalized,
        "allowlist": APPROVAL_ALLOWLIST,
    }


def normalize_heading(text: str) -> str:
    return HEADING_ALIASES.get(text.strip(), text.strip())


def parse_markdown(issue_type: str, mode: str, input_path: Path) -> dict:
    if issue_type not in ISSUE_SCHEMAS:
        raise ValueError(f"Unsupported issue type: {issue_type}")

    content = input_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    schema = ISSUE_SCHEMAS[issue_type]
    ordered_headings = schema["ordered_headings"]
    heading_index = {(level, heading): index for index, (level, heading, _) in enumerate(ordered_headings)}
    required_headings = {
        (level, heading) for level, heading, required in ordered_headings if required
    }

    heading_matches = []
    for line_number, line in enumerate(lines, start=1):
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        heading_matches.append(
            {
                "line": line_number,
                "level": len(match.group(1)),
                "raw_text": match.group(2).strip(),
                "text": normalize_heading(match.group(2)),
            }
        )

    errors = []
    warnings = []

    if not heading_matches:
        errors.append("No markdown headings found.")
    else:
        top_heading = f"{'#' * heading_matches[0]['level']} {heading_matches[0]['text']}"
        if top_heading != schema["top_heading"]:
            errors.append(
                f"Expected top heading '{schema['top_heading']}' but found '{top_heading}'."
            )

    seen_headings = []
    section_ranges = []
    last_heading = None
    for heading in heading_matches:
        if heading["level"] == 1:
            last_heading = heading
            continue
        key = (heading["level"], heading["text"])
        if key not in heading_index:
            errors.append(
                f"Unexpected heading '{'#' * heading['level']} {heading['raw_text']}' on line {heading['line']}."
            )
        else:
            seen_headings.append(key)
            if heading["raw_text"] != heading["text"]:
                warnings.append(
                    f"Normalized heading alias '{heading['raw_text']}' to '{heading['text']}'."
                )
        section_ranges.append(heading)
        last_heading = heading

    last_seen_order = -1
    for key in seen_headings:
        current_order = heading_index[key]
        if current_order < last_seen_order:
            errors.append("Headings are out of canonical order.")
            break
        last_seen_order = current_order

    if mode == "create":
        missing = [
            f"{'#' * level} {heading}"
            for level, heading in required_headings
            if (level, heading) not in seen_headings
        ]
        if missing:
            errors.append(
                "Missing canonical headings for create mode: " + ", ".join(sorted(missing))
            )

    sections = OrderedDict()
    for index, heading in enumerate(section_ranges):
        start = heading["line"]
        end = section_ranges[index + 1]["line"] - 1 if index + 1 < len(section_ranges) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        sections[heading["text"]] = body

    normalized_fields = {
        "project": sections.get("Jira Project"),
        "issue_type": sections.get("Issue Type") or issue_type,
        "summary": sections.get("Title"),
        "fix_versions": parse_listish_value(sections.get("Fix Versions")),
        "priority": blank_to_none(sections.get("Priority")),
        "assignee": blank_to_none(sections.get("Assignee")),
        "reporter": blank_to_none(sections.get("Reporter")),
        "jira_status_or_phase": blank_to_none(sections.get("Jira Status or Phase")),
        "parent_epic": blank_to_none(sections.get("Parent Epic")),
        "parent_issue": blank_to_none(sections.get("Parent Issue")),
    }

    if sections.get("Issue Type"):
        declared_issue_type = sections["Issue Type"].strip()
        if declared_issue_type != issue_type:
            errors.append(
                f"Issue Type heading value '{declared_issue_type}' does not match '{issue_type}'."
            )

    parent_epic = normalized_fields["parent_epic"]
    parent_issue = normalized_fields["parent_issue"]
    normalized_fields["parent_epic_looks_like_issue_key"] = bool(
        parent_epic and ISSUE_KEY_PATTERN.fullmatch(parent_epic)
    )
    normalized_fields["parent_issue_looks_like_issue_key"] = bool(
        parent_issue and ISSUE_KEY_PATTERN.fullmatch(parent_issue)
    )

    return {
        "ok": not errors,
        "mode": mode,
        "issue_type": issue_type,
        "input_path": str(input_path),
        "top_heading": schema["top_heading"],
        "errors": errors,
        "warnings": warnings,
        "headings_seen": [f"{'#' * level} {heading}" for level, heading in seen_headings],
        "normalized_fields": normalized_fields,
        "sections": sections,
        "raw_markdown": content,
    }


def blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def parse_listish_value(value: str | None) -> list[str]:
    if not value:
        return []
    items = []
    for raw_line in value.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        items.append(stripped)
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description="Helpers for jira-updater contract checks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect_parser = subparsers.add_parser("detect-action", help="Detect the Jira action verb.")
    detect_parser.add_argument("--text", required=True, help="Raw user instruction text.")

    approval_parser = subparsers.add_parser("check-approval", help="Check approval text.")
    approval_parser.add_argument("--text", required=True, help="Raw approval reply.")

    parse_parser = subparsers.add_parser("parse-markdown", help="Validate and parse Jira markdown.")
    parse_parser.add_argument(
        "--issue-type",
        required=True,
        choices=sorted(ISSUE_SCHEMAS.keys()),
        help="Canonical Jira issue type for the markdown file.",
    )
    parse_parser.add_argument(
        "--mode",
        required=True,
        choices=["create", "update"],
        help="Use create for full canonical docs and update for partial update docs.",
    )
    parse_parser.add_argument("--input", required=True, help="Path to the markdown file.")

    args = parser.parse_args()

    if args.command == "detect-action":
        result = detect_action(args.text)
    elif args.command == "check-approval":
        result = check_approval(args.text)
    else:
        result = parse_markdown(args.issue_type, args.mode, Path(args.input))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
