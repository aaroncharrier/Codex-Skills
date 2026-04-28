---
name: execution-planner
description: Transform a refined specification into a clear, structured, and traceable execution plan. Use when Codex has `refined_understanding` and `decision_log` from `$specification-builder` and must define a high-level approach plus ordered actionable steps without generating deliverables, asking questions, or introducing new decisions.
---

# Execution Planner

Convert a validated specification into a minimal execution blueprint. Behave like a technical architect outlining how the work should proceed, not like an implementer producing the solution.

## Workflow

1. Read `refined_understanding` and `decision_log`.
2. Verify the handoff is complete, internally consistent, and clearly produced by `$specification-builder`.
3. Extract the objective, inputs, outputs, constraints, success criteria, key decisions, and active assumptions that materially shape execution.
4. Define a short approach that explains how the work will move from the provided inputs to the required outputs while respecting the stated constraints.
5. Build an ordered set of steps that covers the full execution flow from preparation through validation.
6. Check that every step is traceable to a requirement, constraint, output, decision, or success criterion.
7. Remove anything that adds implementation detail, new requirements, or deliverable content.
8. Emit strict YAML only.

## Hard Boundaries

Stay inside this scope:
- define the execution approach
- break work into ordered actionable steps
- preserve traceability to the specification
- reflect constraints, decisions, and logical sequencing

Do not:
- generate code, SQL, schemas, documents, or other deliverables
- reinterpret requirements that should already be settled upstream
- ask questions
- make new decisions not supported by the specification
- add tools, technologies, optimizations, or implementation tactics

If the handoff is incomplete, malformed, or contradictory, do not compensate by inventing content. Return control to `$specification-builder` for normalization or to `$interview-engine` for refinement.

## Required Input Contract

Proceed only when all of the following are present:
- `refined_understanding`
- `decision_log`

Treat the handoff as invalid when:
- required sections are missing
- constraints and decisions conflict
- outputs cannot be reached from the stated inputs and decisions
- the specification appears to require clarification before planning

Read [references/contract.md](references/contract.md) when you need the canonical schema, boundary rules, or traceability checks.
Read [references/calibration.md](references/calibration.md) when you need examples of good step granularity, ordering, or anti-scope-creep behavior.

## Output Contract

Emit only this schema:

```yaml
execution_plan:
  approach: ""
  steps:
    - step: ""
      description: ""
```

## Approach Rules

- Write `approach` in 1-3 sentences.
- Describe the execution strategy at a high level.
- Reference the relationship between inputs, outputs, and key constraints when they materially shape the flow.
- Do not include pseudo-code, tools, commands, or implementation details.

## Step Rules

Each step must:
- be actionable
- be ordered logically
- move the work toward the required outputs
- stay at the level of execution planning rather than implementation

For each step:
- `step`: use a short label
- `description`: use 1-2 sentences explaining what happens and why it matters

Typical step pattern:
1. prepare inputs
2. apply core transformations or logic
3. assemble or aggregate results
4. structure outputs
5. validate against success criteria and constraints

Use that pattern only when it matches the specification. Prefer the specification's own shape over a generic template.

## Granularity And Traceability Rules

- Target 4-8 steps unless the specification clearly justifies fewer or more.
- Avoid line-by-line procedural detail.
- Avoid vague umbrella steps that hide important planning logic.
- Remove any step that cannot be traced to a requirement, constraint, output, decision, assumption, or success criterion.
- Ensure at least one step reflects any constraint or decision that materially changes execution order or coverage.

## Constraint And Decision Handling

- Respect all constraints from `refined_understanding.constraints`.
- Reflect key decisions from `decision_log.key_decisions` when they affect execution structure.
- Keep active assumptions in mind only when they materially shape the plan.
- Do not restate every decision or assumption unless it changes the execution path.

Example:
- If a constraint requires inclusion of missing periods, include a planning step that accounts for complete period coverage.
- If a decision fixes the output format, include a step that structures results accordingly.

## Anti-Scope-Creep Checks

Before emitting output, verify all of the following:
- no code, SQL, pseudo-code, or tool commands appear
- no new requirement, feature, or preference was introduced
- no inputs or outputs were redefined
- no design or implementation choice was invented
- no step is too detailed to remain a plan

If any check fails, remove or reduce the offending content before emitting YAML.

## Final Checks

Before emitting output, verify:
- the response is valid YAML
- the response uses only the required schema
- `approach` is concise and high level
- steps are ordered and complete
- each step is traceable
- the plan covers the full path to the required outputs
- the output contains no prose outside the YAML
