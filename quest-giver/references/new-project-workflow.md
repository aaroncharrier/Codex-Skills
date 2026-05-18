# New Project Workflow

Use this reference only for `new project quest`.

## Required phases

Keep the workflow as three distinct phases:

1. bootstrap the project with `project-bootstrap`
2. guide completion of `docs\questionnaires\AGENTS.QUESTIONNAIRE.md` and update `AGENTS.md`
3. run `project-initiation-pm`

Do not collapse these into one improvised setup pass.

## Phase 1: Bootstrap

- Instruct the user to run the bootstrap script first instead of hand-creating the scaffold.

## Phase 2: AGENTS handoff

- Share a prompt with the user that will guide the user through answering `docs\questionnaires\AGENTS.QUESTIONNAIRE.md`.
- Provide a prompt for the user to ask Codex to update `AGENTS.md` from the completed answers.

## Phase 3: Project initiation

- Instruct the user to run `project-initiation-pm` only after `AGENTS.md` is tailored.
- Share with the user a detailed overview of the project to assist with answering the questions.

## Naming and location

- Create new tutorial-driven projects under `Codex Improvement`.
- Use the folder naming pattern `<tutorial name> yyyy_mm_dd`.

Example:

`Codex Improvement\Data Quality Tutorial 2026_05_17`

## Threshold rule

Use this workflow when the quest is multi-session, multi-file, or intended to produce a reusable project asset.
