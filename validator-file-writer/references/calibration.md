# Validator File Writer Calibration

Use this file to keep validation behavior strict, traceable, and free of repair work.

## Calibration Rules

- Treat the validator as a mirror, not a mechanic.
- Prefer explicit traceability over broad commentary.
- Report only what the inputs support.
- If evidence is missing, record the missing evidence rather than inventing it.
- Keep the output machine-readable and limited to the required YAML schema.

## Anti-Scope-Creep Checks

Stop and correct course if you are about to:
- rewrite SQL for correctness
- add notebook cells
- repair document structure
- improve prompt wording
- add agent safeguards or policies that were not specified
- fill in missing requirements by assumption

If any of those impulses appear, convert them into issues or recommendations instead of edits.

## Classification Hints

### Structural

Use for missing sections, malformed wrappers, invalid schema shape, or wrong artifact format.

### Logical

Use for incorrect execution ordering, missing transformations, or plan-step mismatches.

### Completeness

Use for omitted outputs, partially implemented steps, or skipped required content.

### Consistency

Use for conflicts between specification and artifact or between plan and artifact.

### Risk

Use for ambiguity, fragile assumptions, or unsafe execution patterns that reduce confidence even when the artifact is otherwise present.

## Severity Hints

- `LOW`: visible but non-blocking deviation
- `MEDIUM`: usable artifact with meaningful gaps
- `HIGH`: correctness is materially compromised
- `CRITICAL`: artifact is fundamentally unusable for the intended contract

## Recommendation Style

Good recommendation style:
- "Rework the artifact section mapped to execution step 4 so the required transformation is actually represented."
- "Review the missing output tied to specification section 2.3 before regeneration."

Bad recommendation style:
- "Replace the SQL with: ..."
- "Add this notebook cell: ..."
- "Use this clearer prompt instead: ..."

## Clean PASS Criteria

A clean pass should mean:
- required inputs were available
- required structure was present
- plan coverage was complete
- no material inconsistency was found
- no repair work was performed in the response
