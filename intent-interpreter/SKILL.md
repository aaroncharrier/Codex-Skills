---
name: "intent-interpreter"
description: "Normalize a raw user request into a compact YAML intent snapshot with outputs, references, ambiguity notes, and confidence. Use when Codex needs routing-ready intent before clarification or downstream execution."
---

# Intent Interpreter

Convert the raw request into a routing-ready YAML snapshot. Normalize the task. Do not interview, plan, validate, or generate the solution.

## Token Contract

- Keep prose short.
- Prefer grounded lists over explanation.
- Do not restate the prompt.
- Record only ambiguity that could change the artifact, file targets, validation, or execution path.

## Workflow

1. Extract explicit facts, requested outputs, references, and constraints.
2. Infer the most likely artifact type from `sql`, `notebook`, `document`, `prompt`, `agent_spec`, or `other`.
3. Record only blocking gaps across objective, artifact shape, inputs, constraints, output format, and validation criteria.
4. Add minimal assumptions only when they are needed to interpret the request.
5. Emit strict YAML only.

## Output Contract

Emit only this schema:

```yaml
intent:
  objective: ""
  role: ""
  role_tone: ""
  summary: ""
  inputs: []
  references: []
  outputs: []
  what_success_looks_like: ""
  inferred_artifact_type: ""
  ambiguity_notes: []

assumptions:
  - ""

confidence: 0.0
```

## Field Rules

- `objective`: one concrete sentence
- `role`: one or two short sentences
- `role_tone`: one sentence
- `summary`: no more than two short sentences
- `inputs`, `references`, `outputs`: grounded items only
- `what_success_looks_like`: no more than two short sentences
- `ambiguity_notes`: one concrete gap per item
- `assumptions`: minimal and uncertainty-aware
- `confidence`: `0.0` to `0.4`

## Guardrails

- Do not ask questions.
- Do not propose execution steps.
- Do not generate solution content.
- Do not introduce fields beyond the schema.
- Do not turn common defaults into confirmed facts.

Read [references/heuristics.md](references/heuristics.md) only when artifact classification or confidence calibration is unclear.
