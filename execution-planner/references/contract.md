# Execution Planner Contract

Use this file as the canonical reference for input requirements, output schema, scope boundaries, and traceability checks. Do not quote it in the final response. Apply it.

## Required Inputs

Proceed only when all of the following are available and internally coherent:
- `refined_understanding`
- `decision_log`

If either section is missing, malformed, contradictory, or clearly under-refined, the request is not ready for this skill. Return control upstream instead of inventing missing structure.

## Output Schema

Emit only:

```yaml
execution_plan:
  approach: ""
  steps:
    - step: ""
      description: ""
```

## Boundary Rules

Allowed:
- define a high-level execution approach
- produce ordered actionable steps
- preserve traceability to requirements, constraints, outputs, decisions, assumptions, and success criteria
- tighten wording and remove redundant steps

Forbidden:
- asking questions
- generating code or deliverables
- redefining the specification
- introducing new requirements or decisions
- adding tool-specific or implementation-level detail

## Traceability Rules

For every step:
- identify what requirement, constraint, output, decision, assumption, or success criterion it supports
- remove the step if no such mapping exists

For the plan as a whole:
- cover the full path from input preparation to output validation
- ensure material constraints and key decisions are reflected in the plan

## Failure Conditions

Do not proceed when:
- constraints conflict with decisions
- outputs cannot be reached from the stated inputs and decisions
- the specification still needs clarification or normalization

In those cases, hand the request back to `$specification-builder` or `$interview-engine` as appropriate.
