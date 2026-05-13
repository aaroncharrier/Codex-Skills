#!/usr/bin/env python3
"""
Create deterministic Jira issue document paths and template copies.

This helper stays intentionally small:
- resolve the canonical template for a supported issue type
- reserve a collision-safe output path using the required filename pattern
- copy the canonical template into docs/Jira Documents for new issues
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

ISSUE_TYPE_TEMPLATES = {
    "epic": "epic.md",
    "story": "story.md",
    "task": "task.md",
    "sub-task": "sub-task.md",
    "bug": "bug.md",
}

ISSUE_TYPE_ALIASES = {
    "epic": "epic",
    "story": "story",
    "task": "task",
    "bug": "bug",
    "subtask": "sub-task",
    "sub-task": "sub-task",
    "sub_task": "sub-task",
    "sub task": "sub-task",
}

MAX_TITLE_SLUG_LENGTH = 80


def normalize_issue_type(raw_value: str) -> str:
    value = raw_value.strip().lower()
    value = re.sub(r"\s+", " ", value)
    normalized = ISSUE_TYPE_ALIASES.get(value)
    if normalized:
        return normalized

    value = value.replace("_", "-")
    normalized = ISSUE_TYPE_ALIASES.get(value)
    if normalized:
        return normalized

    raise ValueError(
        "Unsupported issue type. Use Epic, Story, Task, Sub-task, or Bug."
    )


def slugify_title(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("Title must contain at least one letter or digit.")
    return slug[:MAX_TITLE_SLUG_LENGTH].rstrip("-")


def parse_timestamp(raw_value: str | None) -> datetime:
    if raw_value is None:
        return datetime.now()
    try:
        return datetime.strptime(raw_value, "%Y%m%d_%H%M%S")
    except ValueError as exc:
        raise ValueError(
            "Timestamp must use YYYYMMDD_HHMMSS, for example 20260511_121142."
        ) from exc


def format_timestamp(value: datetime) -> str:
    return value.strftime("%Y%m%d_%H%M%S")


def get_skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def get_template_path(issue_type: str) -> Path:
    template_name = ISSUE_TYPE_TEMPLATES[issue_type]
    return get_skill_dir() / "references" / "templates" / template_name


def ensure_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        raise ValueError(
            f"Output directory does not exist: {output_dir}. "
            "Create docs/Jira Documents separately before using this skill."
        )
    if not output_dir.is_dir():
        raise ValueError(f"Output path is not a directory: {output_dir}")


def reserve_issue_path(output_dir: Path, issue_type: str, title: str, base_time: datetime) -> Path:
    ensure_output_dir(output_dir)
    slug = slugify_title(title)
    current_time = base_time

    while True:
        filename = f"{issue_type}__{slug}_{format_timestamp(current_time)}.md"
        candidate = output_dir / filename
        if not candidate.exists():
            return candidate
        current_time += timedelta(seconds=1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Work with jira-template-completer templates and filenames."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    template_parser = subparsers.add_parser(
        "template-path", help="Print the canonical template path for an issue type."
    )
    template_parser.add_argument("--issue-type", required=True)

    reserve_parser = subparsers.add_parser(
        "reserve-path", help="Print a collision-safe output path for a new issue."
    )
    reserve_parser.add_argument("--issue-type", required=True)
    reserve_parser.add_argument("--title", required=True)
    reserve_parser.add_argument("--output-dir", required=True)
    reserve_parser.add_argument("--timestamp")

    copy_parser = subparsers.add_parser(
        "copy-template",
        help="Copy the canonical template to a collision-safe output path.",
    )
    copy_parser.add_argument("--issue-type", required=True)
    copy_parser.add_argument("--title", required=True)
    copy_parser.add_argument("--output-dir", required=True)
    copy_parser.add_argument("--timestamp")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        issue_type = normalize_issue_type(args.issue_type)
        template_path = get_template_path(issue_type)
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_path}")

        if args.command == "template-path":
            print(template_path)
            return 0

        output_dir = Path(args.output_dir).resolve()
        base_time = parse_timestamp(getattr(args, "timestamp", None))
        reserved_path = reserve_issue_path(output_dir, issue_type, args.title, base_time)

        if args.command == "reserve-path":
            print(reserved_path)
            return 0

        shutil.copyfile(template_path, reserved_path)
        print(reserved_path)
        return 0
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
