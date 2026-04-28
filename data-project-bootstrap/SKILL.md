---
name: data-project-bootstrap
description: Create a Codex-ready project context pack for a new or lightly populated data engineering repository. Use when starting a new data project, creating `CODEX.md` and `.codex/` documentation, or standardizing project bootstrap docs with an interview-first workflow. Especially useful when the repo has little or no code yet and Codex needs help gathering business context, platform details, standards, and task templates before implementation begins.
---

# Data Project Bootstrap

Use this skill to bootstrap Codex-facing project documentation for data engineering work. Use an interview-first workflow: gather concise business and platform context from the user, inspect the repo only if useful, then generate `CODEX.md` and the `.codex/` directory with the smallest opinionated starter pack that fits the project.

## Non-Negotiables

- Treat the short interview as required, not optional.
- Do not generate or modify project docs until the interview answers are collected.
- The only exception is when the user explicitly says to skip questions, use placeholders, or scaffold immediately.
- If proceeding without full answers, say that you are doing so at the user's request and keep unresolved fields as `TODO:`.
- Do not infer business goals, stakeholders, platform, or guardrails from the repo name alone.
- Always generate `.codex/project/OPEN_QUESTIONS.yaml` as the working list of unresolved project decisions.
- Keep `OPEN_QUESTIONS.yaml` broad enough to drive future updates to the markdown docs.
- When a question is answered, update the relevant markdown files first, then remove that item from `OPEN_QUESTIONS.yaml` instead of leaving answered questions behind.

## Workflow

### 1. Confirm the target path

Ask where the docs should be created if the destination is unclear.

- Use the current workspace by default.
- If the user wants a reusable starter elsewhere, confirm before writing outside the workspace.

### 2. Run a short interview

Repos are often empty at creation time, so do not depend on code inspection. Ask only the smallest set of questions needed to produce useful files.

This step is a gate. Stop and ask these questions before creating files unless the user explicitly asks you to skip the interview.

Start with these:

1. What is the project name and what business problem does it solve?
2. Which platform should the docs assume: Snowflake, Databricks, or both?
3. What tooling is expected, if known: orchestration, transformations, CI/CD, IaC?
4. Who are the main users or stakeholders of the data product?
5. Are there any non-negotiable standards or guardrails to capture now?

Ask follow-ups only if the answers materially affect the generated docs.

If the user has already provided some of the answers in their request, do not re-ask those parts. Ask only for the missing pieces.

### 3. Inspect the repo when it can add value

If the repo contains files, look for signals that can improve the generated docs:

- `dbt_project.yml`, `packages.yml`
- `airflow/`, `dags/`, `dagster/`
- `terraform/`, `.tf` files
- `.github/workflows/`
- `Dockerfile`, `docker-compose.yml`
- warehouse or platform indicators such as `snowflake`, `databricks`, `spark`, `notebooks`

If the repo is mostly empty, skip deep inspection and proceed from the interview.

### 4. Generate the starter pack

Use `scripts/init_codex_docs.py` to scaffold the files from `assets/templates/`.

- Pass the target directory and the interview answers as arguments.
- Prefer filling unknown fields with `TODO:` markers rather than inventing business facts.
- Keep the templates concise and practical.
- If the user explicitly chose to skip the interview, preserve that decision and scaffold with `TODO:` markers instead of guessing.
- Generate `OPEN_QUESTIONS.yaml` with a broad set of unresolved questions across platform, tooling, ingestion, modeling, operations, governance, and validation.
- Remove questions from `OPEN_QUESTIONS.yaml` only after their answers have been reflected in the markdown docs.

### 5. Do a quick quality pass

After generation:

- verify the expected files exist
- spot-check `CODEX.md`
- ensure the selected platform sections match the user's stack
- confirm the docs clearly separate inferred content from unresolved TODOs
- confirm `OPEN_QUESTIONS.yaml` exists and contains only still-open questions

## Platform references

Read these only when relevant:

- For Snowflake-specific defaults and prompts: `references/snowflake.md`
- For Databricks-specific defaults and prompts: `references/databricks.md`
- For the interview checklist and answer-to-template mapping: `references/interview-guide.md`

## Output shape

Generate this structure unless the user asks for a different layout:

- `CODEX.md`
- `.codex/README.md`
- `.codex/project/PROJECT_CONTEXT.md`
- `.codex/project/NEW_PROJECT_CHECKLIST.md`
- `.codex/project/OPEN_QUESTIONS.yaml`
- `.codex/standards/WORKING_AGREEMENTS.md`
- `.codex/rules/sql-modeling.md`
- `.codex/rules/pipelines-and-orchestration.md`
- `.codex/rules/reviews.md`
- `.codex/templates/TASK_TEMPLATE.md`
- `.codex/commands/start-task.md`
- `.codex/commands/review-task.md`

## Implementation notes

- Use the templates in `assets/templates/` instead of rewriting the files from scratch.
- Use the script for deterministic scaffolding and token efficiency.
- Preserve existing files unless the user explicitly wants them replaced.
- Mark unresolved sections with clear `TODO:` placeholders.
- Treat `OPEN_QUESTIONS.yaml` as a temporary open-decisions queue, not a permanent decision log.
- Before generating, briefly summarize whether you are using interview answers or proceeding with placeholders at the user's explicit request.
- Mention assumptions in the final response.
