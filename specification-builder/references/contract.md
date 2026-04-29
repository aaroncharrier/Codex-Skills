# Specification Builder Contract

Use this file as the canonical reference for input requirements, output schema, and hard boundaries.

## Preferred Input Source

Prefer reading the resolved sections from the persisted interview YAML or a stage snapshot path instead of pasting the full upstream payload inline.

## Required Inputs

Proceed only when all of the following are available and internally coherent:

- `resolved_inputs`
- `resolved_outputs`
- `constraints`
- `decisions`
- `assumptions`
- `codex_role`
- `success_criteria`
- `confidence >= 0.95`

If any requirement is missing, malformed, contradictory, or below the confidence threshold, the request is not ready for this skill. Return control to `$interview-engine` for refinement.

## Output Schema

Emit only:

```yaml
refined_understanding:
  objective: ""
  role: ""
  role_tone: ""
  summary: ""
  inputs: []
  references: []
  outputs: []
  constraints: []
  success_criteria: []
  what_success_looks_like: ""

decision_log:
  key_decisions:
    - decision: ""
      rationale: ""
  assumptions: []
```

## Boundary Rules

Allowed:

- consolidate resolved data
- normalize names and duplicated concepts
- tighten wording
- resolve conflicts only when the supplied data already supports one interpretation

Forbidden:

- asking questions
- planning
- generating deliverables
- optimizing the solution
- adding requirements, behaviors, or design choices

## Decision And Assumption Rules

For every retained decision:

- keep the wording concrete
- keep the rationale traceable
- avoid invented justification

For assumptions:

- keep only assumptions that still matter
- remove invalidated assumptions
- remove assumptions duplicated by decisions or constraints

## Consistency Rules

Validate:

- inputs against outputs
- constraints against decisions
- assumptions against decisions
- success criteria against outputs and constraints

If a conflict cannot be resolved from the supplied data alone, stop and hand the request back to `$interview-engine`.
