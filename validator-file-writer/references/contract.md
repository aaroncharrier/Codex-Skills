# Validator File Writer Contract

Use this file as the canonical reference for input requirements, output schemas, scope boundaries, issue classification, severity rules, and handoff behavior.

## Preferred Input Source

Prefer persisted stage snapshots over duplicated inline payloads.

## Required Inputs

Proceed only when all of the following are available and structurally readable:

- `execution_plan`
- one of:
  - `final_specification`
  - `refined_understanding` and `decision_log`
  - a persisted specification snapshot containing those sections
- one of:
  - `generated_artifact`
  - `artifact`

Optional:

- `artifact_metadata`

If any required section is missing, malformed, contradictory, or too incomplete to validate, the request is not ready for this skill.

## Ready-State Output Schema

Emit only:

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

## Unclassifiable-State Output Schema

Emit only:

```yaml
status: validation_handoff_required
action: "halt_validation"
handoff_required:
  target_skill: artifact-generator OR execution-planner
  reason: "artifact does not match specification or execution plan"
  context:
    - observed_issue:
    - affected_section:
```

Use this schema only when validation cannot be classified cleanly inside the required report structure.

## Boundary Rules

Allowed:

- compare the artifact against the specification and execution plan
- evaluate structure, logic, consistency, completeness, and risk
- document issues, missing elements, and deviations
- determine pass or fail and rework requirement
- halt and hand off when the failure cannot be classified cleanly

Forbidden:

- asking questions
- modifying the artifact
- regenerating outputs
- rewriting content
- supplying missing assumptions
- improving, optimizing, or repairing the artifact
- re-planning or re-running the workflow

## Issue Classification Rules

Use only these categories:

1. `STRUCTURAL`
2. `LOGICAL`
3. `COMPLETENESS`
4. `CONSISTENCY`
5. `RISK`

## Severity Model

- `LOW`: cosmetic or formatting deviation
- `MEDIUM`: partial mismatch but usable output
- `HIGH`: missing or incorrect logic affecting correctness
- `CRITICAL`: unusable or fundamentally invalid artifact

## Pass Or Fail Rules

- Mark `pass_fail: PASS` only when the artifact is structurally compliant, logically consistent, and complete enough to satisfy the declared requirements.
- Mark `pass_fail: FAIL` when any `HIGH` or `CRITICAL` issue exists, or when combined `MEDIUM` issues materially block correctness or completeness.
- Mark `schema_compliance: FAIL` when required structure or expected formatting is missing or malformed.
- Mark `logical_consistency: FAIL` when the artifact conflicts with the specification or execution plan.
- Mark `completeness: FAIL` when required outputs, sections, or plan coverage are missing.
- Set `rework_required: true` whenever `pass_fail: FAIL`.

## Routing Hint Rules

Use `routing_hint` when the failure maps cleanly:

- `spec_issue`: the specification is wrong, incomplete, or contradictory
- `plan_issue`: the plan is wrong, incomplete, or out of order
- `artifact_issue`: the artifact failed despite ready upstream inputs
- `structural_issue`: the same stage should be retried once because the failure is purely structural
- `none`: pass result or no clean routing signal

## Recommendation Rules

Recommendations may:

- identify what needs review or rework
- point to the affected section, step, or requirement
- describe the type of corrective work needed at a high level

Recommendations must not:

- contain rewritten artifact content
- supply replacement implementations
- provide new plan steps
- silently resolve ambiguity

## Handoff Rules

Hand off only when:

- the artifact cannot be validated cleanly because the failure mode does not fit the report structure
- upstream planning artifacts are too incomplete or contradictory to support classification
- the artifact is missing to the point that issue classification would be mostly speculative

Target selection:

- hand off to `$execution-planner` when the specification or plan needs refinement
- hand off to `$artifact-generator` when the artifact needs regeneration from already-ready upstream inputs

Do not repair the issue inside this skill.
