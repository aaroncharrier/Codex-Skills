---
name: artifact-generator
description: Render a final user-facing artifact from a completed specification and execution plan using a deterministic translation flow. Use when Codex already has a final specification plus an execution plan and must produce only the final artifact output with metadata, without asking questions, changing upstream logic, or improving the design.
---

# Artifact Generator

Render, do not redesign. Treat this skill as a strict translation layer from upstream planning artifacts into a final user-facing artifact.

## Workflow

1. Read `final_specification` and `execution_plan`.
2. Confirm the required inputs are present and identify `artifact_type` from the specification or explicit input.
3. If local files exist for the specification and plan, run `scripts/compute-hashes.ps1` to compute deterministic SHA-256 hashes for `source_spec_hash` and `execution_plan_hash`.
4. Map execution steps directly to the target artifact structure.
5. Preserve ordering exactly as provided in the execution plan.
6. Render the artifact in the required syntax for the declared artifact type.
7. Assemble the final output object with metadata and validation flags.
8. Emit the final output only.

## Hard Boundaries

Stay inside this scope:
- translate specification plus execution plan into a final artifact
- preserve execution-plan ordering exactly
- attach metadata and validation flags
- halt and redirect upstream when inputs are missing or structurally unready

Do not:
- ask questions
- modify the specification
- modify the execution plan
- add new steps, logic, assumptions, or optimizations
- reorder, merge, or split execution steps
- validate for business correctness beyond contract readiness
- suggest improvements
- debug upstream decisions
- perform self-correction

If the request is incomplete, malformed, or structurally inconsistent, do not compensate. Return control to `$execution-planner` for refinement and emit the handoff payload defined in [references/contract.md](references/contract.md).

## Required Input Contract

Proceed only when all of the following are present:
- `final_specification`
- `execution_plan`

Optional:
- `artifact_type` when it is not embedded clearly in the specification

Treat the handoff as not ready when:
- the specification is missing
- the execution plan is missing
- the artifact type cannot be identified
- execution steps are absent or malformed
- the specification and execution plan conflict structurally

Read [references/contract.md](references/contract.md) for the canonical input rules, output schemas, and failure behavior.
Read [references/calibration.md](references/calibration.md) for examples of compliant rendering behavior and anti-scope-creep checks.

## Execution Model

Apply this pipeline exactly:

1. Parse inputs.
2. Identify artifact type.
3. Map plan steps to artifact structure.
4. Render each step into final artifact syntax.
5. Assemble the final output object.

Do not insert any intermediate reasoning, commentary, or redesign work between those stages.

## Determinism Rules

- Produce the same output for the same inputs.
- Keep wording stable unless the specification or plan changes.
- Do not introduce stylistic creativity beyond required formatting.
- Prefer computed hashes from `scripts/compute-hashes.ps1` when local file paths or raw text are available.
- If hashes cannot be computed because no local file or text payload is available, preserve the field and set a stable sentinel value that truthfully reflects the missing hash input rather than inventing one.

## Artifact Type Rules

### SQL

- Follow execution plan ordering exactly.
- Do not add joins, filters, transformations, or optimizations not present in the plan or specification.

### NOTEBOOK

- Render one section per execution step.
- Do not add analysis, commentary, or extra cells outside the planned structure.

### DOCUMENT

- Preserve the ordered flow exactly.
- Do not expand scope or restructure sections for clarity.

### PROMPT

- Preserve instruction hierarchy exactly.
- Do not reword instructions in ways that change meaning.

### AGENT_SPEC

- Mirror the execution plan structure exactly.
- Do not introduce behavioral enhancements or policy additions not already specified.

## Output Contract

When inputs are ready, emit only:

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

When inputs are not ready, emit only the halt payload defined in [references/contract.md](references/contract.md). Redirect to `$execution-planner` for refinement. Do not also emit a partial artifact wrapper.

## Validation Flag Rules

- `missing_inputs`: list only genuinely missing required inputs
- `ambiguities_detected`: record ambiguities as metadata only; never resolve them here
- `plan_deviation`: mark `true` only when the requested rendering would require deviating from the plan
- `spec_conflict`: mark `true` only when the specification and plan cannot both be followed as given

Validation flags are reporting fields, not permission to change behavior.

## Final Checks

Before emitting output, verify:
- the response matches one allowed schema
- the artifact structure follows the execution plan exactly
- no step was added, removed, merged, split, or reordered
- metadata fields are present
- the response contains no prose outside the final YAML payload
