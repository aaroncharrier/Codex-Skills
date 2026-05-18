---
name: project-initiation-pm
description: Run conversation-first project initiation after project-bootstrap creates the scaffold. Use when Codex should read referenced project docs first, classify the work, interview the user 3 questions at a time, directly populate PROJECT_PLAN/WORK_LOG docs, create only justified supporting data docs, escalate to BRD/PRD/SRD only when the project is expected to exceed 6 weeks, and deterministically delete the six unused BRD/PRD/SRD template/questionnaire files for shorter projects.
---

# Project Initiation PM

## Overview

This skill is for startup discovery and first-draft project definition. It is not the execution PM workflow.

## Resources

- `references/INTERVIEW_FLOW.md`
- `references/PROJECT_CLASSIFICATION_RULES.md`
- `references/PROJECT_PLAN_POPULATION_RULES.md`
- `references/TECHNICAL_CHALLENGE_RULES.md`
- `references/FILE_SELECTION_RULES.md`
- `references/QUESTION_BANK/`
- `scripts/cleanup_unused_docs.py`

## Required Workflow

1. Read any user-referenced documents before asking questions.
2. Classify the project into one primary branch.
3. Ask the user to confirm or correct the classification.
4. Ask exactly 3 high-value questions at a time.
5. Use branch-specific questioning from `references/QUESTION_BANK/`.
6. Always ask adjacent-scope questions so related work is not missed.
7. Avoid silent inference. Record unknown required items as `TBD`.
8. Challenge weak technical decisions and recommend stronger practices.
9. Populate the existing scaffold files directly.
10. Stop when additional questions are no longer adding material value and a credible first draft exists.
11. Run `scripts/cleanup_unused_docs.py` at the end to delete the six BRD/PRD/SRD files when the project is expected to take 6 weeks or less.

## User Assumption

Treat the user as a junior data engineer seeking principal engineer practices.

## Scope

This skill should update the bootstrap-generated project package directly.

It should not create a parallel planning system.

## Primary Branches

- New data pipeline
- Existing pipeline enhancement / optimization
- Snowflake semantic layer / analytics modeling
- MicroStrategy reporting development
- Multi-domain initiative

After classification, always ask:

`I classify this as [TYPE]. Confirm or correct?`

Do not proceed deeply until the user confirms or corrects the classification.

## Core Rules

- Ask exactly 3 questions at a time.
- Read referenced documents first.
- Do not invent missing facts.
- Use `TBD` for unknown required answers.
- Keep the process lightweight for one-person execution.
- Balance technical design and delivery planning.
- Prefer updating existing files over creating new ones.
- Stop when answers are no longer providing material value.

## Escalation Rule

Default to a project-plan-centered workflow.

Only retain and complete BRD / PRD / SRD when the expected project duration is greater than 6 weeks.

If the project duration is 6 weeks or less, do not keep BRD / PRD / SRD artifacts.

## Always Update

- `docs/PROJECT_PLAN.md`
- `docs/WORK_LOG.md`

## Large-Project-Only Files

Retain and complete only when expected duration is greater than 6 weeks:

- `docs/BRD PRD SRD/BRD_TEMPLATE.md`
- `docs/BRD PRD SRD/PRD_TEMPLATE.md`
- `docs/BRD PRD SRD/SRD_TEMPLATE.md`
- `docs/questionnaires/BRD_QUESTIONNAIRE.md`
- `docs/questionnaires/PRD_QUESTIONNAIRE.md`
- `docs/questionnaires/SRD_QUESTIONNAIRE.md`

## Deterministic Cleanup Rule

For projects expected to take 6 weeks or less, directly delete these six files:

- `docs/BRD PRD SRD/BRD_TEMPLATE.md`
- `docs/BRD PRD SRD/PRD_TEMPLATE.md`
- `docs/BRD PRD SRD/SRD_TEMPLATE.md`
- `docs/questionnaires/BRD_QUESTIONNAIRE.md`
- `docs/questionnaires/PRD_QUESTIONNAIRE.md`
- `docs/questionnaires/SRD_QUESTIONNAIRE.md`

Use `scripts/cleanup_unused_docs.py` for cleanup instead of ad hoc deletion.

## Final Output Contract

At the end, summarize:
- confirmed project type
- files updated
- supporting docs retained
- files deleted by cleanup
- major `TBD` items
- whether BRD / PRD / SRD were skipped or completed
