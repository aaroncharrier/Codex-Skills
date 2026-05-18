from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "quest-wiki"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "campaign"


def ensure_file_from_template(target: Path, template_name: str) -> bool:
    if target.exists():
        return False
    source = TEMPLATE_DIR / template_name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return True


def ensure_campaign_file(quest_wiki_dir: Path, slug: str, title: str) -> tuple[Path, bool]:
    target = quest_wiki_dir / f"campaign-{slug}.md"
    created = ensure_file_from_template(target, "campaign-template.md")
    if created:
        text = target.read_text(encoding="utf-8")
        text = text.replace("[Campaign Title]", title)
        target.write_text(text, encoding="utf-8")
    return target, created


def main() -> int:
    parser = argparse.ArgumentParser(description="Create quest-wiki scaffolding if missing.")
    parser.add_argument("project_path", help="Project root where quest-wiki should live.")
    parser.add_argument("--campaign-slug", help="Optional campaign slug for a campaign file.")
    parser.add_argument("--campaign-title", help="Optional campaign title for a campaign file.")
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    quest_wiki_dir = project_path / "quest-wiki"
    quest_wiki_dir.mkdir(parents=True, exist_ok=True)

    created_paths: list[Path] = []
    for filename in ("quest-backlog.md", "completed-quests.md", "skill-growth-notes.md"):
        target = quest_wiki_dir / filename
        if ensure_file_from_template(target, filename):
            created_paths.append(target)

    if args.campaign_slug or args.campaign_title:
        title = args.campaign_title or args.campaign_slug or "Campaign"
        slug = args.campaign_slug or slugify(title)
        campaign_path, created = ensure_campaign_file(quest_wiki_dir, slug, title)
        if created:
            created_paths.append(campaign_path)

    print(f"quest-wiki: {quest_wiki_dir}")
    if created_paths:
        for path in created_paths:
            print(f"CREATED {path}")
    else:
        print("NO_CHANGES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
