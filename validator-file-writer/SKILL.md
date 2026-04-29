---
name: validator-file-writer
description: Evaluate a generated artifact against its specification, execution plan, structural correctness, logical consistency, and completeness, then emit only a structured validation report. Use when Codex must judge the artifact without modifying, regenerating, or re-planning it.
---

# Validator File Writer

Validate, do not repair. Compare the artifact to upstream requirements and report only the findings that matter.

## Token Contract

- Prefer findings over commentary.
- If validation passes, emit a compact pass result and stop.
- Do not rewrite or restate artifact content.

## Input Rule

Prefer reading persisted stage snapshots instead of carrying full upstream payloads inline.

Proceed only when you have:

- `execution_plan`
- either `final_specification` or the pair `refined_understanding` and `decision_log`
- either `generated_artifact` or the `artifact` payload

If the inputs are too incomplete or contradictory to classify reliably, emit the handoff payload defined in [references/contract.md](references/contract.md).

## Workflow

1. Parse the minimum required inputs.
2. Determine artifact type if possible.
3. Validate structure.
4. Validate logic and plan alignment.
5. Validate completeness.
6. Emit the final YAML report only.

## Output Contract

When validation can be completed, emit only:

```yaml
validation_report:
  pass_fail: PASS | FAIL
  routing_hint: spec_issue | plan_issue | artifact_issue | structural_issue | none
  schema_compliance: PASS | FAIL
  logical_consistency: PASS | FAIL
  completeness: PASS | FAIL

  issues_detected:
    - issue_id:
      category:
      severity: LOW | MEDIUM | HIGH | CRITICAL
      description:
      location_in_artifact:
      related_spec_section:
      related_plan_step:

  missing_elements:
    - element:

  deviations_from_plan:
    - deviation:

  risk_assessment:
    risk_level: LOW | MEDIUM | HIGH | CRITICAL
    summary:

  recommendations:
    - recommendation:

rework_required: true | false
```

When validation cannot be classified cleanly, emit only the handoff payload defined in [references/contract.md](references/contract.md).

## Guardrails

- Do not modify the artifact.
- Do not regenerate outputs.
- Do not supply replacement implementations.
- Do not add new plan steps or assumptions.
- Do not emit prose outside the final YAML payload.

Read [references/contract.md](references/contract.md) only when you need the canonical contract. Read [references/calibration.md](references/calibration.md) only when classification or severity is unclear.
