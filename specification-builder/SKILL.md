---
name: specification-builder
description: Transform fully resolved requirements into a clear, consistent, and execution-ready specification. Use when Codex already has resolved inputs, outputs, constraints, decisions, assumptions, and high confidence from upstream clarification, and must emit strict YAML without planning or generating deliverables.
---

# Specification Builder

Compile resolved requirements into a minimal, internally consistent specification. Convert clarified data into requirements. Do not plan or generate.

## Token Contract

- Prefer normalized lists over narrative.
- Do not restate the user conversation.
- Keep only constraints, decisions, and assumptions that still matter downstream.

## Input Rule

Prefer reading the resolved sections from `.orchestrator-sessions/session-<session_id>/interview_questions.yaml` or a persisted interview snapshot instead of carrying the full interview payload inline.

Proceed only when the handoff includes:

- `resolved_inputs`
- `resolved_outputs`
- `constraints`
- `decisions`
- `assumptions`
- `codex_role`
- `success_criteria`
- `confidence >= 0.95`

If the handoff is incomplete, contradictory, or still structurally inferred, return control to `$interview-engine`.

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

- `objective`: one clear outcome statement
- `role`: one or two short sentences
- `role_tone`: one sentence
- `summary`: no more than three short sentences
- `inputs`, `references`, `outputs`, `constraints`, `success_criteria`: deduplicated, traceable items only
- `what_success_looks_like`: no more than two short sentences
- `decision_log.key_decisions`: keep each decision concrete and the rationale traceable
- `decision_log.assumptions`: keep only active assumptions that still affect downstream execution

## Consistency Rules

- Merge duplicate concepts.
- Standardize naming.
- Remove assumptions invalidated by decisions or constraints.
- Stop instead of inventing missing structure.

## Guardrails

- Do not ask questions.
- Do not add requirements, preferences, or implementation details.
- Do not generate plan steps or deliverable content.
- Do not emit prose outside the YAML.

Read [references/contract.md](references/contract.md) only when you need the canonical contract. Read [references/calibration.md](references/calibration.md) only when normalization or trimming is unclear.
