#!/usr/bin/env python3
"""
Deterministically scaffold a project by creating folders and copying template files.

Usage:
    python .\scripts\bootstrap_project.py C:\path\to\project
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


SKILL_ROOT = Path(__file__).resolve().parent.parent

DIRECTORY_TARGETS = [
    "docs",
    "docs/BRD PRD SRD",
    "docs/Data Documents",
    "docs/questionnaires",
    "repo",
]

FILE_TARGETS = [
    ("templates/README.md", "README.md"),
    ("templates/AGENTS.md", "AGENTS.md"),
    ("templates/PM_AGENT.md", "PM_AGENT.md"),
    ("templates/DATA_ENGINEERING_LEAD.md", "DATA_ENGINEERING_LEAD.md"),
    ("templates/DOCUMENTATION_AGENT.md", "DOCUMENTATION_AGENT.md"),
    ("templates/PROJECT_PLAN.md", "docs/PROJECT_PLAN.md"),
    ("templates/WORK_LOG.md", "docs/WORK_LOG.md"),
    ("templates/BRD_TEMPLATE.md", "docs/BRD PRD SRD/BRD_TEMPLATE.md"),
    ("templates/PRD_TEMPLATE.md", "docs/BRD PRD SRD/PRD_TEMPLATE.md"),
    ("templates/SRD_TEMPLATE.md", "docs/BRD PRD SRD/SRD_TEMPLATE.md"),
    ("templates/DATA_DICTIONARY_TEMPLATE.md", "docs/Data Documents/DATA_DICTIONARY_TEMPLATE.md"),
    ("templates/DATA_MAPPING_DOCUMENT_TEMPLATE.md", "docs/Data Documents/DATA_MAPPING_DOCUMENT_TEMPLATE.md"),
    ("templates/DATA_QUALITY_AND_RECONCILIATION_PLAN.md", "docs/Data Documents/DATA_QUALITY_AND_RECONCILIATION_PLAN.md"),
    ("templates/METRIC_DEFINITION_SIMPLE_TEMPLATE.md", "docs/Data Documents/METRIC_DEFINITION_SIMPLE_TEMPLATE.md"),
    ("templates/METRIC_DEFINITION_TEMPLATE.md", "docs/Data Documents/METRIC_DEFINITION_TEMPLATE.md"),
    ("templates/METRIC_DICTIONARY_TEMPLATE.md", "docs/Data Documents/METRIC_DICTIONARY_TEMPLATE.md"),
    ("templates/RUNBOOK_SUPPORT_TEMPLATE.md", "docs/Data Documents/RUNBOOK_SUPPORT_TEMPLATE.md"),
    ("questionnaires/AGENTS.QUESTIONNAIRE.md", "docs/questionnaires/AGENTS.QUESTIONNAIRE.md"),
    ("questionnaires/WORK_LOG.QUESTIONNAIRE.md", "docs/questionnaires/WORK_LOG.QUESTIONNAIRE.md"),
    ("questionnaires/BRD_QUESTIONNAIRE.md", "docs/questionnaires/BRD_QUESTIONNAIRE.md"),
    ("questionnaires/DATA_QUALITY_AND_RECONCILIATION_PLAN_QUESTIONNAIRE.md", "docs/Data Documents/DATA_QUALITY_AND_RECONCILIATION_PLAN_QUESTIONNAIRE.md"),
    ("questionnaires/PRD_QUESTIONNAIRE.md", "docs/questionnaires/PRD_QUESTIONNAIRE.md"),
    ("questionnaires/RUNBOOK_SUPPORT_QUESTIONNAIRE.md", "docs/Data Documents/RUNBOOK_SUPPORT_QUESTIONNAIRE.md"),
    ("questionnaires/SRD_QUESTIONNAIRE.md", "docs/questionnaires/SRD_QUESTIONNAIRE.md"),
    ("templates/NOTEBOOK_BUILD_REQUIREMENTS.md", "docs/NOTEBOOK_BUILD_REQUIREMENTS.md"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a project scaffold by copying the bundled template pack.",
    )
    parser.add_argument(
        "output_dir",
        help="Explicit output directory for the generated project.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files. Existing directories are never deleted.",
    )
    return parser.parse_args()


def windows_rel(path: Path, root: Path, is_directory: bool = False) -> str:
    rel = path.relative_to(root).as_posix().replace("/", "\\")
    if is_directory and not rel.endswith("\\"):
        rel += "\\"
    return rel


def validate_sources(skill_root: Path) -> None:
    missing: list[str] = []
    invalid: list[str] = []

    for source_relative, _ in FILE_TARGETS:
        source_path = skill_root / source_relative
        if not source_path.exists():
            missing.append(source_relative)
        elif source_path.is_dir():
            invalid.append(source_relative)

    if missing or invalid:
        problems: list[str] = []
        if missing:
            problems.extend(f"Missing source file: {item}" for item in missing)
        if invalid:
            problems.extend(f"Expected file but found directory: {item}" for item in invalid)
        raise FileNotFoundError("\n".join(problems))


def ensure_directory(target: Path, root: Path, summary: list[str]) -> None:
    existed = target.exists()
    if target.exists() and not target.is_dir():
        raise NotADirectoryError(f"Expected directory but found file: {target}")
    target.mkdir(parents=True, exist_ok=True)
    label = "SKIPPED" if existed else "CREATED"
    summary.append(f"{label} {windows_rel(target, root, is_directory=True)}")


def write_file(
    source_path: Path,
    target_path: Path,
    root: Path,
    force: bool,
    summary: list[str],
) -> None:
    if target_path.exists() and target_path.is_dir():
        raise IsADirectoryError(f"Target path is a directory: {target_path}")

    existed = target_path.exists()
    if existed and not force:
        summary.append(f"SKIPPED {windows_rel(target_path, root)}")
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, target_path)

    line = f"CREATED {windows_rel(target_path, root)}"
    if existed and force:
        line += " (overwrote existing file)"
    summary.append(line)


def main() -> int:
    args = parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    validate_sources(SKILL_ROOT)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary: list[str] = []

    for relative_dir in DIRECTORY_TARGETS:
        ensure_directory(output_dir / relative_dir, output_dir, summary)

    for source_relative, target_relative in FILE_TARGETS:
        write_file(
            SKILL_ROOT / source_relative,
            output_dir / target_relative,
            output_dir,
            args.force,
            summary,
        )

    for line in summary:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
