from __future__ import annotations

import argparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_ROOT = SKILL_DIR / "assets" / "templates"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold CODEX.md and .codex docs for a new data project."
    )
    parser.add_argument("--target-dir", required=True, help="Directory to write docs into.")
    parser.add_argument("--project-name", default="TODO: project name")
    parser.add_argument("--business-goal", default="TODO: describe the business goal")
    parser.add_argument(
        "--platform",
        choices=["snowflake", "databricks", "both", "unknown"],
        default="unknown",
    )
    parser.add_argument(
        "--tooling",
        default="TODO: list orchestration, transformation, CI/CD, and IaC tools",
    )
    parser.add_argument(
        "--stakeholders",
        default="TODO: list business owners, analysts, and engineering partners",
    )
    parser.add_argument(
        "--guardrails",
        default="TODO: capture non-negotiable standards, compliance needs, and risk constraints",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    return parser.parse_args()


def replacements(args: argparse.Namespace) -> dict[str, str]:
    platform_label = {
        "snowflake": "Snowflake",
        "databricks": "Databricks",
        "both": "Snowflake and Databricks",
        "unknown": "TODO: confirm platform",
    }[args.platform]
    return {
        "{{PROJECT_NAME}}": args.project_name,
        "{{BUSINESS_GOAL}}": args.business_goal,
        "{{PLATFORM}}": platform_label,
        "{{TOOLING}}": args.tooling,
        "{{STAKEHOLDERS}}": args.stakeholders,
        "{{GUARDRAILS}}": args.guardrails,
    }


def write_template_file(
    source: Path, destination: Path, values: dict[str, str], replace: bool
) -> None:
    if destination.exists() and not replace:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace(key, value)
    destination.write_text(text, encoding="utf-8")


def scaffold_templates(target_dir: Path, values: dict[str, str], replace: bool) -> None:
    for source in TEMPLATE_ROOT.rglob("*"):
        if source.is_dir():
            continue
        relative = source.relative_to(TEMPLATE_ROOT)
        destination = target_dir / relative
        write_template_file(source, destination, values, replace)


def main() -> None:
    args = parse_args()
    target_dir = Path(args.target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    scaffold_templates(target_dir, replacements(args), args.replace)
    print(f"Scaffolded Codex docs in {target_dir}")


if __name__ == "__main__":
    main()
