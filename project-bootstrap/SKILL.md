---
name: project-bootstrap
description: Deterministically create a new analytics or data-engineering project scaffold by creating the target folder and copying the bundled template pack into its existing layout. Use when Codex needs to initialize a new Codex project from the packaged root docs, role files, BRD/PRD/SRD templates, data-document templates, questionnaires, and an empty `repo/` with Windows-only behavior, minimal LLM involvement, overwrite protection via `--force`, and no runtime document editing or questionnaire processing.
---

# Project Bootstrap

## Overview

Use this skill to create a new project scaffold from the current bundled template pack. The skill is script-first and stops after deterministic folder creation and file copying.

This skill is Windows-only.

## Required Workflow

1. Run `scripts/bootstrap_project.py` first. Do not hand-create the scaffold when the script can copy it deterministically.
2. Pass an explicit output directory. The script creates the target folder if it does not already exist.
3. Use `--force` only when the user explicitly wants existing scaffold files overwritten.
4. Review the `CREATED` and `SKIPPED` summary to confirm the expected layout.
5. Stop after scaffold creation. Do not interpret questionnaire answers, synthesize document content, or continue into follow-up document updates as part of this skill.

## Bootstrap Command

Use PowerShell-style examples when showing the command:

```powershell
python .\scripts\bootstrap_project.py C:\path\to\project
```

Use `--force` only when the user explicitly wants existing files overwritten:

```powershell
python .\scripts\bootstrap_project.py C:\path\to\project --force
```

## What the Script Does

`scripts/bootstrap_project.py` is standard-library only and deterministic. It:

- Validates that every expected source template and questionnaire file exists before copying.
- Creates `docs\`, `docs\questionnaires\`, `docs\BRD PRD SRD`, `docs\Data Documents`, and `repo\` if they do not already exist.
- Copies the full current template pack into the target project with a fixed explicit source-to-target manifest.
- Copies templates unchanged. Placeholder tokens such as `{{PROJECT_NAME}}`, `{{OWNER}}`, and `{{LAST_UPDATED}}` remain untouched if they exist in source files.
- Refuses to overwrite existing files unless `--force` is provided.
- Proceeds safely in existing non-empty folders by copying missing scaffold files and skipping existing ones unless `--force` is used.
- Prints stable plain-text summary lines labeled `CREATED` or `SKIPPED`.
- Stops after copying. It does not read, interpret, or update any copied documents.

## Generated Layout

The generated project layout is:

```text
<output_dir>/
  README.md
  AGENTS.md
  PM_AGENT.md
  DATA_ENGINEERING_LEAD.md
  DOCUMENTATION_AGENT.md
  docs/
    PROJECT_PLAN.md
    WORK_LOG.md
    OPEN_QUESTIONS_AND_DECISIONS_LOG.md
    BRD PRD SRD/
      BRD_TEMPLATE.md
      PRD_TEMPLATE.md
      SRD_TEMPLATE.md
    Data Documents/
      DATA_DICTIONARY_TEMPLATE.md
      DATA_MAPPING_DOCUMENT_TEMPLATE.md
      DATA_QUALITY_AND_RECONCILIATION_PLAN.md
      METRIC_DEFINITION_SIMPLE_TEMPLATE.md
      METRIC_DEFINITION_TEMPLATE.md
      METRIC_DICTIONARY_TEMPLATE.md
      DATA_QUALITY_AND_RECONCILIATION_PLAN_QUESTIONNAIRE.md
      RUNBOOK_SUPPORT_TEMPLATE.md
      RUNBOOK_SUPPORT_QUESTIONNAIRE.md
    questionnaires/
      AGENTS.QUESTIONNAIRE.md
      WORK_LOG.QUESTIONNAIRE.md
      BRD_QUESTIONNAIRE.md
      PRD_QUESTIONNAIRE.md
      SRD_QUESTIONNAIRE.md
      OPEN_QUESTIONS_AND_DECISIONS_LOG_QUESTIONNAIRE.md
  repo/
```

Keep this layout exact. Do not create extra planning files unless the user explicitly asks for them.

## Resources

- `scripts/bootstrap_project.py`: deterministic bootstrapper
- `templates/`: source markdown templates copied into the target project
- `questionnaires/`: passive scaffold assets copied into `docs\questionnaires` and `docs\Data Documents` according to the fixed manifest

## Passive Assets

Questionnaires, role files, and templates remain in the scaffold as project assets, but this skill does not act on them after copying.

- Do not tell the user to fill questionnaires as part of this skill workflow.
- Do not read questionnaire answers during scaffold creation.
- Do not mutate any copied files during scaffold creation.

## Maintenance Rules

- Keep the skill narrow, deterministic, and easy to validate.
- Keep the current file inventory, template contents, and target placement unchanged unless the user explicitly asks for a scaffold change.
- Keep `scripts/bootstrap_project.py` script-first with a fixed explicit copy manifest.
- If you change a template or questionnaire path, update the file map in `scripts/bootstrap_project.py` in the same edit.
- If you change the scope again, update `agents/openai.yaml` so the UI metadata stays aligned with the skill behavior.
