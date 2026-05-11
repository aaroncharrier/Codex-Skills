# AGENTS

- Purpose: Route agent work, define shared project rules, and keep role selection explicit.
- How to use this document: Read this before acting. Select one role, emit the required preflight block, then inspect only the files needed for that role.
- Last updated: {{LAST_UPDATED}}

## Project Context

Project: {{PROJECT_NAME}}

Owner: {{OWNER}}

Project type:
- Lightweight analytics and data-engineering project

Primary working areas:
- `repo/` for code and project assets
- `README.md` for human-facing overview and setup
- `docs/PROJECT_PLAN.md` for planning, decisions, and open questions
- `docs/WORK_LOG.md` for append-only execution history

## Tech Stack

- Languages: TBD
- Frameworks and libraries: TBD
- Package manager: TBD
- Data platform(s): TBD
- Orchestration / scheduling: TBD

## Coding Conventions

- Match the conventions already present in `repo/`.
- Keep changes small, readable, and easy to validate.
- Prefer deterministic scripts over one-off manual steps when work repeats.
- Update documentation when setup, workflows, or behavior changes.

## Data-Engineering Standards

- Make source systems, grain, and destination tables explicit.
- Favor idempotent transforms and reproducible local runs.
- State assumptions about freshness, quality checks, and downstream usage.
- Record lineage, schema, and SLA-impacting decisions in `docs/PROJECT_PLAN.md`.

## Testing and Validation Expectations

- Run the narrowest useful validation before concluding work.
- Report the commands run and the validation outcome.
- If you cannot validate, say so plainly and explain the gap.
- Add follow-up work to `docs/PROJECT_PLAN.md` when validation gaps create risk.

## Security and Secrets Handling

- Never hardcode secrets, tokens, or credentials.
- Use approved secret stores or local environment mechanisms.
- Minimize sensitive data movement and avoid copying production data unless explicitly approved.
- Redact sensitive identifiers in shared notes when possible.

## Git and PR Expectations

- Confirm the branching model before making workflow assumptions.
- Keep commits focused on one coherent change when commits are requested.
- Summarize user-facing impact, validation, and risks in reviews or handoffs.
- If the project is solo and does not use PRs, note the exception here instead of inventing one.

## Definition of Done

- Requested work is implemented or updated in the correct files.
- Relevant validation is complete, or the validation gap is documented.
- Documentation stays consistent with the current behavior.
- New decisions and open questions are recorded in `docs/PROJECT_PLAN.md` when they affect future work.

## Things Agents Must Not Do

- Do not guess a role. Select one explicitly before acting.
- Do not create new planning files unless explicitly requested.
- Do not split decisions or open questions into separate documents.
- Do not treat `docs/WORK_LOG.md` as a scratchpad or rewrite history.
- Do not put human-facing setup guidance in role files if it belongs in `README.md`.

## Role Selection

| Role | Use when the request is about | Primary files |
|---|---|---|
| Coding Agent | code, tests, refactors, bugs, repo changes | source code, tests, `README.md` |
| Project Manager | tasks, phases, blockers, decisions, open questions, status | `docs\PROJECT_PLAN.md`, `docs\WORK_LOG.md` |
| Documentation Agent | explaining setup, usage, architecture, onboarding | `README.md`, `AGENTS.md` |
| Data Engineering Lead | data models, pipelines, validation, lineage, SLAs | code, `README.md`, `docs\PROJECT_PLAN.md` |

If a request fits multiple roles, choose the dominant role and state it before acting.

## Required Preflight

This preflight is mandatory for every role before acting.

```text
Role: <selected role>
Reason: <one sentence>
Files I will inspect: <list>
Files I may edit: <list>
```

## Role Notes

- Use this file as the baseline for the `Coding Agent` role because there is no separate `CODING_AGENT.md`.
- Read `PM_AGENT.md`, `DATA_ENGINEERING_LEAD.md`, or `DOCUMENTATION_AGENT.md` after selecting that role.
- Keep `README.md` human-facing and `AGENTS.md` agent-facing.

## Maintenance Rules

- Keep the role router and preflight block exact.
- Use a real current date when updating the `Last updated` value.
- Update tech stack, commands, and guardrails when the project changes.
