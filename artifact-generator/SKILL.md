---
name: artifact-generator
description: Render a final user-facing artifact from a completed specification and execution plan using a deterministic translation flow. Use when Codex already has a ready specification plus an execution plan and must produce only the final artifact output with minimal metadata.
---

# Artifact Generator

Render, do not redesign. Translate ready upstream artifacts into the final artifact.

## Token Contract

- Generate only the artifact and the metadata required to place or validate it.
- Do not restate the full specification or plan.
- Keep non-artifact text out of the output.

## Input Rule

Prefer reading persisted stage snapshots instead of carrying full upstream payloads inline.

Proceed only when you have:

- `execution_plan`
- either `final_specification` or the pair `refined_understanding` and `decision_log`
- `artifact_type` when it is not already obvious from the specification

If the handoff is missing, malformed, contradictory, or structurally unready, halt and route upstream instead of compensating.

## Workflow

1. Parse the minimum required inputs.
2. Identify the artifact type.
3. Map execution steps directly to artifact structure.
4. Render the artifact in the required syntax.
5. Emit the final YAML payload only.

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

When inputs are not ready, emit only the halt payload defined in [references/contract.md](references/contract.md).

## Guardrails

- Do not ask questions.
- Do not modify the specification or execution plan.
- Do not add logic, assumptions, or optimizations.
- Do not reorder, merge, or split planned steps.
- Do not emit prose outside the final YAML payload.

Read [references/contract.md](references/contract.md) only when you need the canonical contract. Read [references/calibration.md](references/calibration.md) only when rendering behavior is unclear.
