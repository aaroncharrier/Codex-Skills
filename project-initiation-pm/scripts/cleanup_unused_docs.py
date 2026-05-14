#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SHORT_PROJECT_FILES = [
    Path("docs/BRD PRD SRD/BRD_TEMPLATE.md"),
    Path("docs/BRD PRD SRD/PRD_TEMPLATE.md"),
    Path("docs/BRD PRD SRD/SRD_TEMPLATE.md"),
    Path("docs/BRD PRD SRD"),
    Path("docs/questionnaires/BRD_QUESTIONNAIRE.md"),
    Path("docs/questionnaires/PRD_QUESTIONNAIRE.md"),
    Path("docs/questionnaires/SRD_QUESTIONNAIRE.md"),
]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete unused BRD/PRD/SRD starter documents for short projects."
    )
    parser.add_argument("project_dir", help="Path to the bootstrap-generated project directory.")
    parser.add_argument(
        "--duration-weeks",
        type=float,
        required=True,
        help="Expected project duration in weeks.",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()

    if not project_dir.exists() or not project_dir.is_dir():
        print(f"ERROR missing project directory: {project_dir}")
        return 2

    if args.duration_weeks > 6:
        for rel in SHORT_PROJECT_FILES:
            target = project_dir / rel
            state = "KEPT" if target.exists() else "MISSING"
            print(f"{state} {rel.as_posix()} reason=duration_gt_6_weeks")
        return 0

    for rel in SHORT_PROJECT_FILES:
        target = project_dir / rel
        if target.exists():
            target.unlink()
            print(f"DELETED {rel.as_posix()} reason=duration_lte_6_weeks")
        else:
            print(f"MISSING {rel.as_posix()} reason=duration_lte_6_weeks")

    return 0

if __name__ == "__main__":
    sys.exit(main())
