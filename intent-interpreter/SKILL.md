---
name: "intent-interpreter"
description: "Convert a raw user prompt into a structured, minimal, and uncertainty-aware interpretation of intent. Use when Codex needs to normalize an initial request before clarification, extract explicit inputs and outputs, identify ambiguity, infer a probable artifact type, and emit strict YAML without asking questions, planning execution, or generating deliverables."
---

# Intent Interpreter

Convert a raw user request into a strict YAML interpretation that is minimal, neutral, and explicit about uncertainty. Stop at intent translation. Do not ask questions, propose a plan, or generate any part of the solution.

The primary goal of this skill is not only to summarize intent, but to surface the most complete possible list of ambiguities before the request reaches `$interview-engine`.

## Workflow

1. Read the raw prompt and isolate only information that is explicit or reasonably implied.
2. Derive a concrete, outcome-focused `objective`.
3. Write a 2-4 sentence `summary` covering context, likely use case, and implied expectations.
4. Extract grounded `inputs`, `references`, and `outputs`.
5. Infer `inferred_artifact_type` from the allowed set: `sql`, `notebook`, `document`, `prompt`, `agent_spec`, `other`.
6. Evaluate ambiguity across all six required context lenses:
   - objective context
   - artifact context
   - input context
   - execution constraints
   - output contract
   - validation criteria
7. List unresolved gaps in `ambiguity_notes`.
8. Write minimal, neutral `assumptions`.
9. Assign a confidence score from `0.0` to `0.4` only.
10. Emit strict YAML matching the contract exactly.

## Ambiguity Lenses

Before finalizing `ambiguity_notes`, explicitly check whether the raw prompt sufficiently defines each of the following:

### 1. Objective Context

This anchors the request in intent rather than mechanics.

Check for:
- what is being built, changed, or analyzed
- why it matters or who it serves
- what success looks like at the outcome level

### 2. Artifact Context

This defines the concrete artifact Codex is expected to produce or modify.

Check for:
- file or artifact type
- naming conventions
- output structure
- where the artifact lives
- whether the task is create vs modify

### 3. Input Context

This defines what source material Codex is allowed or expected to rely on.

Check for:
- existing code, files, schemas, tables, interfaces, APIs, or documents
- reference examples, screenshots, prompt guides, or style guides
- whether the available inputs are complete enough to avoid hallucinated dependencies

### 4. Execution Constraints

This defines how the work must be carried out.

Check for:
- language, framework, platform, or dialect requirements
- performance, scale, or safety constraints
- tooling constraints
- style rules
- anti-patterns or forbidden approaches

### 5. Output Contract

This defines what the response itself must look like.

Check for:
- response format such as code, JSON, YAML, markdown, or mixed output
- required sections
- ordering requirements
- wrapping requirements such as code blocks, tags, or headings

### 6. Validation Criteria

This defines how correctness will be judged.

Check for:
- conditions that must be true for the output to count as correct
- edge cases
- testability expectations
- acceptance criteria or business rules

If any lens is materially underspecified, capture that gap in `ambiguity_notes` instead of silently compensating for it.

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

- `objective`: Write one sentence describing the requested outcome concretely.
- `role`: Write 2-4 sentence that establishes perspective and expertise to apply reasoning patterns and domain assumptions.
- `role_tone`: Write one sentence describing the tone that codex should use as a voice.
- `summary`: Write 2-4 sentences with context, likely use case, and implied expectations.
- `inputs`: List required inputs that are explicit or clearly implied by the request. Do not invent speculative dependencies.
- `outputs`: List the expected deliverables. If the output is unclear, make a cautious best guess and reflect uncertainty in `ambiguity_notes` and `confidence`.
- `references`: List any reference documents for the task.
- `what_success_looks_like`: Write 2-4 sentences describing what a successful output looks like.
- `inferred_artifact_type`: Use exactly one allowed value. If unclear, use `other`.
- `ambiguity_notes`: List specific missing constraints, undefined outputs, unclear scope boundaries, and missing context discovered through the six ambiguity lenses. Make the notes concrete enough that `$interview-engine` can turn them into focused questions.
- `assumptions`: Keep assumptions neutral, minimal, and uncertainty-aware.
- `confidence`: Never exceed `0.4`.

If the output is unclear for any field, make a cautious best guess and reflect uncertainty in `ambiguity_notes` and `confidence`.

## Guardrails

- Do not ask follow-up questions.
- Do not propose execution steps.
- Do not generate part of the requested deliverable.
- Do not resolve ambiguity; only describe it.
- Do not introduce fields beyond the schema.
- Do not over-assume details that are absent from the request.
- Do not collapse multiple ambiguity categories into one vague note when separate notes would make downstream interviewing more precise.
- Do not treat common defaults as resolved facts when the prompt leaves them open.

## Confidence Bands

- `0.1-0.2`: Highly ambiguous request with major missing details.
- `0.2-0.3`: Partially clear request with identifiable direction but important gaps.
- `0.3-0.4`: Mostly clear request that still needs validation before downstream work.

## Artifact And Confidence Heuristics

Read [references/heuristics.md](references/heuristics.md) when artifact type classification or confidence calibration is not obvious.

## Final Checks

Before emitting output, verify all of the following:

- The response is valid YAML.
- The response uses only the required schema.
- The response contains no questions.
- The response contains no plan.
- The response contains no generated solution content.
- The confidence score is between `0.0` and `0.4`.
- `ambiguity_notes` reflects all materially unresolved gaps found across objective context, artifact context, input context, execution constraints, output contract, and validation criteria.
