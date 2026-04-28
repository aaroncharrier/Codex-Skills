---
name: validator-file-writer
description: Evaluate a generated artifact against its final specification, execution plan, structural correctness, logical consistency, and completeness, then emit only a structured validation report. Use when Codex already has `final_specification`, `execution_plan`, and `generated_artifact` and must judge the artifact without modifying, regenerating, repairing, or re-planning it.
---

# Validator File Writer

Validate, do not repair. Treat this skill as a strict comparison engine that checks a generated artifact against upstream planning artifacts and reports findings only.

## Workflow

1. Read `final_specification`, `execution_plan`, and `generated_artifact`.
2. Confirm the required inputs are present and structurally readable.
3. Identify the artifact type from the specification, artifact metadata, or artifact structure when possible.
4. Validate structure against required sections, expected format, and plan coverage.
5. Validate logic against the specification, execution plan, ordering, and declared transformations.
6. Validate completeness against required outputs, required sections, and step coverage.
7. Classify every detected issue by category and severity.
8. Emit the validation report only.

## Hard Boundaries

Stay inside this scope:
- compare the artifact to the specification and execution plan
- evaluate structural correctness
- evaluate logical consistency
- evaluate completeness
- classify risks and deviations
- produce a machine-readable validation report

Do not:
- modify the artifact
- regenerate output
- rewrite content for correctness or clarity
- suggest replacement implementations
- re-run execution logic
- re-plan the workflow
- ask questions
- resolve ambiguity by assumption
- optimize, improve, or expand the artifact
- infer missing steps and treat them as completed

If an issue is found, document it in `validation_report` and nowhere else. If the failure cannot be classified cleanly, emit the handoff payload defined in [references/contract.md](references/contract.md). Do not attempt repair.

## Required Input Contract

Proceed only when all of the following are present:
- `final_specification`
- `execution_plan`
- `generated_artifact`

Optional:
- `artifact_metadata`

Read [references/contract.md](references/contract.md) for the canonical input rules, output schema, issue classes, severity model, and handoff behavior.
Read [references/calibration.md](references/calibration.md) for examples of compliant validation behavior and anti-scope-creep checks.

## Execution Model

Apply this pipeline exactly:

1. Parse inputs.
2. Determine artifact type if possible.
3. Run structural validation.
4. Run logical validation.
5. Run completeness validation.
6. Compile issues, deviations, missing elements, and risks.
7. Determine `PASS` or `FAIL`.
8. Emit the final YAML report.

Do not insert repair steps, rewrite steps, or advisory redesign between those stages.

## Determinism Rules

- Produce the same report structure for the same inputs.
- Keep classification language stable unless the inputs change.
- Do not invent missing facts to complete validation.
- When evidence is missing, record the missing input, ambiguity, or unclassifiable condition rather than compensating for it.

## Artifact Type Guidance

Use generic validation rules first, then apply type-aware checks when the artifact type is known.

### SQL

- Check that planned clauses, transformations, and ordering are represented.
- Do not rewrite or optimize SQL even when it is obviously flawed.

### NOTEBOOK

- Check that planned sections or cells are represented and ordered correctly.
- Do not add missing analysis, cells, or outputs.

### DOCUMENT

- Check that required sections, ordering, and planned coverage are present.
- Do not restructure sections for readability.

### PROMPT

- Check instruction hierarchy, required constraints, and ordering against the plan.
- Do not rewrite prompt wording.

### AGENT_SPEC

- Check that the behavioral structure mirrors the specification and plan.
- Do not add policy, safeguards, or behavior not already present upstream.

## Validation Rules

### Structural Validation

Check:
- required sections exist
- output format matches the expected artifact type when known
- all planned steps are represented
- schema shape is valid for the declared artifact

### Logical Validation

Check:
- specification-to-artifact consistency
- plan-to-artifact consistency
- ordering correctness
- required transformations or behaviors are represented

### Completeness Validation

Check:
- all required outputs exist
- no required step is skipped
- no required section is partial when the plan calls for completion

## Issue Classification

Classify issues only within these categories:
- `STRUCTURAL`
- `LOGICAL`
- `COMPLETENESS`
- `CONSISTENCY`
- `RISK`

Use these severity levels only:
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

Apply the severity model from [references/contract.md](references/contract.md). Keep every issue traceable to a specification section, plan step, or concrete artifact location whenever possible.

## Output Contract

When validation can be completed, emit only:

```yaml
validation_report:
  pass_fail: PASS | FAIL
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

## Recommendation Rules

- Keep recommendations evaluative, not corrective.
- Recommendations may name what must be revisited, clarified, or reworked.
- Recommendations must not include rewritten artifact content or substitute implementations.

## Final Checks

Before emitting output, verify:
- the response matches one allowed schema
- no artifact content has been modified in the response
- every detected issue is classified
- pass/fail is explicit and justified by the findings
- the response contains no prose outside the final YAML payload
