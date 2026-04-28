# Artifact Generator Contract

Use this file as the canonical reference for input requirements, output schemas, scope boundaries, deterministic rendering rules, and failure behavior. Do not quote it in the final response. Apply it.

## Required Inputs

Proceed only when all of the following are available and structurally ready:
- `final_specification`
- `execution_plan`

Optional:
- `artifact_type` when it is not unambiguously embedded in `final_specification`

If any required section is missing, malformed, contradictory, or under-refined, the request is not ready for this skill.

## Ready-State Output Schema

Emit only:

```yaml
artifact:
  type: <SQL | NOTEBOOK | DOCUMENT | PROMPT | AGENT_SPEC>
  content: |
    <final rendered artifact ONLY>

artifact_metadata:
  artifact_type:
  source_spec_hash:
  execution_plan_hash:
  generation_mode: deterministic

validation_flags:
  missing_inputs: []
  ambiguities_detected: []
  plan_deviation: false
  spec_conflict: false
```

## Incomplete-State Output Schema

Emit only:

```yaml
status: incomplete_inputs
missing: []
action: "halt_generation"
handoff_required:
  target_skill: execution-planner
  reason: "input refinement required before deterministic artifact rendering"
  details: []
```

List only the missing or structurally unready inputs in `missing`.

## Boundary Rules

Allowed:
- map execution steps to artifact structure
- preserve plan ordering exactly
- render the final artifact in the required target format
- attach deterministic metadata and validation flags
- halt and hand off upstream when the contract is not met

Forbidden:
- asking questions
- modifying the specification
- modifying the execution plan
- adding logic, assumptions, optimizations, or clarifications
- restructuring steps
- filling missing values
- self-correcting upstream decisions

## Determinism Rules

- same inputs must yield the same outputs
- do not vary structure or wording except where formatting rules require it
- do not optimize or reinterpret content
- use stable SHA-256 hashes for `source_spec_hash` and `execution_plan_hash` when the input text or files are available

## Handoff Rules

Hand off to `$execution-planner` when:
- required inputs are missing
- artifact type cannot be identified
- execution steps are absent or malformed
- the plan and specification conflict structurally
- any deterministic rendering would require plan deviation

Do not repair the inputs inside this skill.
