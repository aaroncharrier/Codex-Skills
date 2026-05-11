---
name: project-bootstrap
description: Bootstrap lightweight, one-person analytics and data-engineering projects with a deterministic local script, role-specific agent guidance, and questionnaire-driven project docs. Use when Codex needs to initialize a new Codex project folder with `README.md`, `AGENTS.md`, role files, `docs/PROJECT_PLAN.md`, `docs/WORK_LOG.md`, `docs/questionnaires/`, and an empty `repo/`, then update those generated documents after the user fills in the questionnaires.
---

# Project Bootstrap

## Overview

Use this skill to initialize a lightweight analytics or data-engineering project without turning the setup into a heavyweight process. Start with the deterministic bootstrap script, then use the copied questionnaires to gather real project details before updating the generated documents.

Version 1 is Windows-only.

## Required Workflow

1. Run `scripts/bootstrap_project.py` first. Do not hand-create the target project files when the script can create them deterministically.
2. Pass an explicit output directory. Use `--project-name` and `--owner` when the user already knows them.
3. Review the `CREATED` and `SKIPPED` summary to confirm the expected root-versus-`docs` layout.
4. Tell the user to fill in the copied questionnaires under `docs\questionnaires`.
5. After the user confirms the questionnaires are complete, read the answers and update the generated documents in the same invocation.
6. When editing generated documents later, set a real current date in that document's `Last updated` metadata.

## Bootstrap Command

Use PowerShell-style examples when showing the command:

```powershell
python .\scripts\bootstrap_project.py C:\path\to\project --project-name "My Project" --owner "Owner Name"
```

Use `--force` only when the user explicitly wants existing files overwritten:

```powershell
python .\scripts\bootstrap_project.py C:\path\to\project --force
```

## What the Script Does

`scripts/bootstrap_project.py` is standard-library only and deterministic. It:

- Creates `docs\`, `docs\questionnaires\`, `docs/BRD PRD SRD`, `docs/Data Documents`, and `repo\` if they do not already exist.
- Copies template files into the project root and `docs\`.
- Copies questionnaire working copies into `docs\questionnaires\`.
- Copies data and metric documents into `docs/Data Documents`.
- Copies the BRP, PRD, and SRP templates into `docs/BRD PRD SRD`.
- Refuses to overwrite existing files unless `--force` is provided.
- Prints stable plain-text summary lines labeled `CREATED` or `SKIPPED`.

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
    BRD PRD SRP/
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
      AGENTS.questionnaire.md
      WORK_LOG.questionnaire.md
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
- `questionnaires/`: working questionnaire copies placed under `docs\questionnaires`

## Questionnaire Update Pass

After the user fills in the questionnaires:

1. Read the seven files under `docs\questionnaires`.
2. Update `README.md` with factual business context, setup, data sources, outputs, environments, ownership, and links.
3. Update `AGENTS.md` with the real tech stack, commands, guardrails, and workflow expectations.
4. Update `docs\PROJECT_PLAN.md` with the actual goal, scope, phases, milestones, dependencies, risks, decisions, open questions, and acceptance criteria.
4. Update `docs\BRD_TEMPLATE.md`, `docs\PRD_TEMPLATE.md`, and `docs\SRD_TEMPLATE.md` with the actual goal, scope, phases, milestones, dependencies, risks, decisions, open questions, and acceptance criteria.
5. Update `docs\WORK_LOG.md` only if the user has supplied a real work-log entry. Otherwise leave the starter placeholder intact.
6. Keep `README.md` human-facing, `AGENTS.md` agent-facing, and `docs\WORK_LOG.md` append-only.

## Maintenance Rules

- Keep the skill small, deterministic, and easy to maintain.
- Keep decisions and open questions inside `docs\PROJECT_PLAN.md`.
- Do not add `DECISIONS.md`, `OPEN_QUESTIONS.md`, `CODING_AGENT.md`, or other extra bootstrap artifacts unless the user explicitly requests them.
- If you change a template or questionnaire path, update the file map in `scripts/bootstrap_project.py` in the same edit.
