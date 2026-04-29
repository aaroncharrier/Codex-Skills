---
name: execution-planner
description: Transform a refined specification into a clear, structured, and traceable execution plan. Use when Codex has a validated specification from `$specification-builder` and must define ordered actionable steps without generating deliverables or introducing new decisions.
---

# Execution Planner

Convert a validated specification into a minimal execution blueprint. Plan the work. Do not implement it.

## Token Contract

- Keep the approach short.
- Use only the steps needed to reach the required outputs.
- Remove planning detail that belongs in implementation.

## Input Rule

Prefer reading a persisted specification snapshot or the `refined_understanding` and `decision_log` pair instead of carrying duplicated spec prose inline.

Proceed only when:

- `refined_understanding` is present
- `decision_log` is present
- the handoff is internally consistent

If the specification is missing, contradictory, or still needs clarification, return upstream instead of inventing structure.

## Output Contract

Emit only this schema:

```yaml
execution_plan:
  approach: ""
  steps:
    - step: ""
      description: ""
```

## Plan Rules

- `approach`: one to three short sentences
- Default step count: four to eight
- Each step must be ordered, actionable, and traceable to a requirement, constraint, output, decision, assumption, or success criterion
- Prefer the specification's natural workflow over a generic template

## Guardrails

- Do not generate code, commands, pseudo-code, or deliverables.
- Do not redefine the specification.
- Do not introduce tools, technologies, or new decisions.
- Do not emit prose outside the YAML.

Read [references/contract.md](references/contract.md) only when you need the canonical contract. Read [references/calibration.md](references/calibration.md) only when step granularity or ordering is unclear.
