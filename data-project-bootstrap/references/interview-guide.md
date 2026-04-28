# Interview Guide

Use this guide to keep the bootstrap interview short and useful.

## Core Questions

Ask these first:

1. Project name
2. Business problem or goal
3. Platform: Snowflake, Databricks, or both
4. Known tooling: orchestration, transformation, IaC, CI/CD
5. Stakeholders or user groups
6. Any hard rules, constraints, or compliance needs

## Good Follow-Ups

Ask follow-ups only when they affect the generated structure or standards.

- If Snowflake: ask whether dbt, Snowpark, tasks, streams, or external stages are expected.
- If Databricks: ask whether the project centers on notebooks, jobs, Delta Live Tables, Unity Catalog, or dbt.
- If orchestration is unclear: ask whether Airflow, Dagster, Databricks Jobs, or native scheduling is expected.
- If governance matters: ask about PII, regulated data, and access-control expectations.

## Mapping Answers To Files

- Project name and business goal: `CODEX.md`, `.codex/project/PROJECT_CONTEXT.md`
- Platform and tooling: `.codex/project/PROJECT_CONTEXT.md`, `.codex/standards/WORKING_AGREEMENTS.md`
- Stakeholders and users: `.codex/project/PROJECT_CONTEXT.md`
- Guardrails and non-negotiables: `.codex/standards/WORKING_AGREEMENTS.md`
- Unknowns and unresolved design choices: `.codex/project/OPEN_QUESTIONS.yaml`
- After an open question is answered: update the relevant markdown files, then remove the answered item from `.codex/project/OPEN_QUESTIONS.yaml`
