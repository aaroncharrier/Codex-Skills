---
name: specification-builder
description: Transform fully resolved requirements into a clear, consistent, and execution-ready specification. Use when Codex already has resolved_inputs, resolved_outputs, constraints, decisions, assumptions, and confidence of at least 0.95 from an upstream clarification step such as Interview Engine, and must emit strict YAML without planning, generating deliverables, or introducing new requirements.
---

# Specification Builder

Convert resolved requirements into a strict YAML specification that is clear, internally consistent, and ready for downstream execution. Act like a compiler for clarified inputs, not a planner, designer, or generator.

## Workflow

1. Read the provided `resolved_inputs`, `resolved_outputs`, `constraints`, `decisions`, `assumptions`, and `confidence`.
2. Verify that all required inputs are present and that `confidence` is at least `0.95`.
3. Check for contradictions, invalidated assumptions, or missing logical links across inputs, outputs, constraints, and decisions.
4. Normalize naming, merge duplicate concepts, and remove redundant items using only the supplied data.
5. Build `refined_understanding` so it reflects the resolved request precisely and minimally.
6. Build `decision_log` so every retained decision and assumption is traceable to the supplied data.
7. Emit strict YAML only.

## Hard Boundaries

Stay inside this scope:
- build a structured specification from resolved data
- normalize inputs, outputs, constraints, decisions, and assumptions
- remove duplication and internal inconsistency using only supplied information
- produce strict YAML only

Do not:
- ask questions
- plan execution steps
- generate code, pseudo-code, documents, or other deliverables
- introduce new requirements, features, or preferences
- optimize or improve the requested solution

If the handoff is incomplete or inconsistent, do not compensate by inventing content. The request must return to `$interview-engine` for refinement before this skill is used again.

## Required Input Contract

Proceed only when all of the following are present:
- `resolved_inputs`
- `resolved_outputs`
- `constraints`
- `decisions`
- `assumptions`
- `confidence >= 0.95`

If the request depends on matching an external prompt framework, style guide, template, screenshot, or example artifact, treat unresolved assumptions about structure, section ordering, tags, examples, or formatting conventions as an invalid handoff from the upstream clarification stage.

Treat missing fields, malformed structure, unresolved contradictions, or low confidence as an invalid handoff from the upstream clarification stage.

## Output Contract

Emit only this schema:

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

## Field Rules

- `objective`: Write one clear, outcome-focused statement aligned to the resolved outputs.
- `role`: Write 2-4 sentence that establishes perspective and expertise to apply reasoning patterns and domain assumptions.
- `role_tone`: Write one sentence describing the tone that codex should use as a voice.
- `summary`: Write 2-5 sentences covering what is being built, how it behaves at a high level, and the key constraints that materially shape it.
- `inputs`: Keep this a clean, deduplicated list that matches the resolved inputs after normalization.
- `references`: List any reference documents for the task.
- `outputs`: Reflect the final expected deliverables only.
- `constraints`: Keep only explicit or validated constraints that still apply after decisions are considered.
- `success_criteria`: State concrete completion conditions that are testable and directly supported by the supplied information.
- `what_success_looks_like`: Write 2-4 sentences describing what a successful output looks like.
- `decision_log.key_decisions[].decision`: State what was chosen.
- `decision_log.key_decisions[].rationale`: State why it was chosen using only user answers, explicit constraints, or unavoidable broadly accepted practice already implied by the handoff.
- `decision_log.assumptions`: Keep only active assumptions that still matter for downstream execution.

## Normalization Rules

- merge duplicate concepts
- standardize naming to one consistent convention such as `customer_id`
- collapse overlapping items when they express the same meaning
- remove trivial or redundant assumptions
- remove assumptions invalidated by constraints or decisions
- preserve original intent while tightening phrasing

Do not use normalization as a reason to add information that was not present in the handoff.

## Consistency Checks

Before emitting output, verify all of the following:
- inputs and outputs are logically compatible
- constraints do not conflict with decisions
- assumptions are not invalidated by decisions
- success criteria are supported by the resolved outputs and constraints
- summary does not introduce information absent from the handoff

If a conflict cannot be resolved using existing data alone, stop using this skill and return the request to `$interview-engine`.

Also return the request to `$interview-engine` if any material part of the artifact structure is still being inferred rather than confirmed.

## Assumption Rules

Keep an assumption only when it:
- still holds after clarification
- materially affects downstream execution
- is not already restated as a decision or constraint

Remove assumptions that are:
- trivial
- redundant
- invalidated
- purely speculative

## Anti-Scope-Creep Checks

Before finalizing output, verify:
- no new requirement was introduced
- no new design decision was created
- no execution plan was added
- no solution content was generated

If any check fails, remove the offending content before emitting YAML.

## Final Checks

Before emitting output, verify all of the following:
- the response is valid YAML
- the response uses only the required schema
- every required field is populated
- naming is internally consistent
- the output contains no prose outside the YAML
- the output introduces zero new ideas

Read [references/contract.md](references/contract.md) when you need the canonical schema or boundary rules.
Read [references/calibration.md](references/calibration.md) when you need examples of good normalization, consistency handling, or assumption trimming.
