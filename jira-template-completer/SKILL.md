---
name: jira-template-completer
description: Generate or refine local Jira markdown issue documents for analytics and data-engineering work without calling Jira APIs or updating Jira directly. Use when Codex needs to create or normalize Epic, Story, Task, Sub-task, or Bug markdown files in `docs/Jira Documents` from a rough request, explicitly referenced local files, or an explicitly referenced existing Jira markdown document, including optional explicit parent-child batches with one issue per file.
---

# Jira Template Completer

## Overview

Generate or refine Jira-ready markdown issue documents for analytics and data-engineering work. Stay local: author files only in `docs/Jira Documents`, use the canonical templates bundled with this skill, and never call Jira APIs or load Jira state.

## Workflow

1. Confirm the request is only for local markdown authoring or refinement. If the user asks to create, update, import, sync, or inspect Jira state directly, stop and explain that this skill only prepares markdown artifacts.
2. Decide whether the task is `new` or `refine`.
3. Determine the supported issue type: `Epic`, `Story`, `Task`, `Sub-task`, or `Bug`. Support parent-child batches only when the user explicitly requests them.
4. Use only the chat request and files the user explicitly referenced. Do not inspect unrelated local files or assume hidden project context.
5. Read [runtime-rules.md](references/runtime-rules.md) and the matching template in `references/templates/`.
6. If blocking information is still missing after using the explicit inputs, ask concise grouped clarifying questions and stop before writing anything.
7. For new documents, use `scripts/issue_doc_helper.py copy-template` to create the collision-safe file in `docs/Jira Documents`, then replace every placeholder with final content.
8. For refinements, open only the explicitly referenced Jira markdown file and rewrite it to the canonical heading order for its issue type. Remove nonstandard headings instead of preserving template drift.
9. Keep markdown only, one issue per file, and no YAML frontmatter in generated issue documents.

## Helper Script

Use `scripts/issue_doc_helper.py` for deterministic template lookup and file naming.

Examples:

```powershell
python scripts/issue_doc_helper.py copy-template --issue-type Story --title "Add Snowflake warehouse utilization dashboard" --output-dir "docs/Jira Documents"
python scripts/issue_doc_helper.py reserve-path --issue-type Bug --title "Finance dashboard incorrect totals" --output-dir "docs/Jira Documents"
python scripts/issue_doc_helper.py template-path --issue-type Epic
```

## Template Map

- `Epic`: [references/templates/epic.md](references/templates/epic.md)
- `Story`: [references/templates/story.md](references/templates/story.md)
- `Task`: [references/templates/task.md](references/templates/task.md)
- `Sub-task`: [references/templates/sub-task.md](references/templates/sub-task.md)
- `Bug`: [references/templates/bug.md](references/templates/bug.md)

## Batch Rules

- Use `Related Stories` in Epic documents as the child document list when generating Story, Task, or Bug children.
- Use `Suggested Sub-tasks` in Story, Task, and Bug documents as the child document list when generating Sub-task children.
- Fill `Parent Epic` or `Parent Issue` in each child document with the parent title and markdown filename.
- Keep one issue per file even in batch mode.

## Guardrails

- Default `Jira Status or Phase` to `Not Started` only when the user omits it.
- Do not create `docs/Jira Documents`; stop if it does not already exist.
- Do not read or refresh `Jira Templates` at runtime. The canonical templates in this skill are the only source of truth.
- Keep analytics and data-engineering terminology specific. Do not broaden the skill into generic project management or Jira administration.
