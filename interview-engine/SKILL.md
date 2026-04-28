---
name: interview-engine
description: Resolve ambiguity in a user request through a YAML-backed requirements interview stored in `.orchestrator-sessions/session-<session_id>/interview_questions.yaml`. Use when Codex needs to refine inputs before execution, especially after intent has been normalized by another skill such as Intent Interpreter. This version is append-only, delimiter-driven, and chat-minimized.
---

# Interview Engine

Conduct a structured requirements interview that reduces uncertainty quickly while keeping the YAML file as the single source of truth.

## Core Model

- The only interaction surface with the user is `interview_questions.yaml`.
- The only source of truth for interview state is `interview_questions.yaml`.
- Questions and answers exist only in `interview_questions.yaml`.
- Chat must be minimized to reduce token usage.
- Never output questions in chat.
- Never paste YAML into chat.
- Never explain the questions in chat.

## Hard Boundaries

Stay inside this scope:
- identify ambiguity, missing details, contradictions, and weak assumptions
- record structured clarifying questions in the YAML file
- keep the interview ready for downstream handoff

Do not:
- propose solutions
- generate code, plans, specs, documents, or roadmaps
- choose among business options for the user
- explain at length outside the file contract

## Workflow

1. Start from the current request and any upstream normalized intent.
2. Inspect only the active answer block in the YAML file.
3. Generate a larger internal pool of candidate questions.
4. Score candidates with the rubric in `Question Scoring`.
5. Append only the top 5-7 unresolved questions to the YAML file.
6. Update confidence and affected assumptions.
7. Emit the short chat confirmation.
8. When confidence reaches `0.95`, stop appending and hand off according to orchestrator behavior.

## File Contract

- File name: `interview_questions.yaml`
- File path: `.orchestrator-sessions/session-<session_id>/interview_questions.yaml`
- If the file does not exist, create it with the strict schema and the first active question block.
- If the file exists, patch it in place.
- Do not overwrite the file unless minimal repair is required.
- The schema is fixed and must not change.

### Strict Schema

```yaml
confidence: 0.0-1.0

assumptions:
  - id: A1
    statement: ""

themes:
  - theme_id: T1
    name: ""
    description: ""
    questions:
      - question_id: Q1
        question: ""
        type: one_of | multi_select | freeform | ranking | numeric
        context: ""
        why_it_matters: ""
        example_answers:
          - ""
        recommended_answer: ""
        your_answer: ""
```

## Append-Only Semantics

- Questions are immutable after creation.
- Do not modify existing questions.
- Do not delete existing questions.
- Do not reorder existing questions.
- Do not modify any existing `your_answer` values.
- Keep theme IDs, names, descriptions, and ordering stable.
- Do not create new themes after the file has been initialized.
- Append new questions only at the end of the file.
- Continue the global `question_id` sequence across the entire file (`Q1`, `Q2`, `Q3`, ...).
- Update only `confidence` and the assumptions affected by new answers.
- Preserve partial answers exactly as written.

## Delimiter Model

Use this exact marker:

```text
# === ACTIVE_ANSWER_BLOCK_START ===
```

### Read Rules

When reading the file:
- locate the marker
- only read `your_answer` fields that appear after the marker
- ignore all questions before the marker
- ignore all schema fields except `your_answer`
- ignore blank `your_answer` values
- accept partial answers as valid input
- do not reprocess historical context

### Write Rules

When more information is needed:
1. Remove the old marker.
2. Append new questions to the end of the file.
3. Insert the marker immediately before the first newly appended question.
4. Update `confidence`.
5. Update only assumptions affected by the new answers.

### Patch Strategy

- Use deterministic, surgical patching.
- Modify only the marker position, appended questions, affected assumptions, and confidence.
- Do not rewrite the entire file unless the YAML is irreparable.
- Preserve every existing `your_answer` value.
- Keep the file valid YAML at every patch step.

## Question Targets

Focus only on questions that materially improve one of these areas:
- requirements
- inputs
- constraints
- data
- output_format
- edge_cases
- success_criteria
- codexs_role
- external_framework_alignment

## Framework Alignment

When the request references any of the following, record explicit clarification questions in the YAML file before termination unless the needed details are already fully specified:
- a vendor or model provider prompt guide
- a screenshot, image, or visual template
- a best practices page
- an example prompt or artifact to emulate
- a named framework, taxonomy, or section order

For those cases, prioritize questions that capture:
- which source is authoritative when multiple references exist
- which sections are required, optional, or forbidden
- how strictly to preserve ordering, tag style, and formatting conventions
- whether examples, XML tags, conversation history, prefills, or reasoning instructions should appear
- which choices may be assumed and which must come from the user explicitly

## Question Scoring

Score each candidate question from 0-5 on:
- impact
- uncertainty
- dependency
- risk
- effort_to_answer

Use:

```text
score = (impact * 2 + uncertainty * 2 + dependency + risk * 2) - effort_to_answer
```

Select the final set using these rules:
- choose 5-7 questions by default
- absolute max is 10 only if unresolved risk is critical
- preserve theme diversity
- combine overlapping questions when possible
- prefer structured response types over freeform when they can capture the need

## Question Design

Every question must:
- resolve meaningful uncertainty
- be specific and actionable
- make the reason for asking visible
- reduce future questioning effort

Use these question types:
- `one_of` for mutually exclusive choices
- `multi_select` for multiple valid selections
- `freeform` for nuanced details
- `ranking` for prioritization
- `numeric` for measurable thresholds or limits

For each question, always provide:
- `context`
- `why_it_matters`
- `example_answers` with 2-5 high-quality examples
- `recommended_answer` as a best-practice default, not a personalized guess
- `your_answer` as an empty string

## Iteration Rules

After new answers arrive:
1. parse each answer
2. normalize answers into one or more of:
   - constraints
   - preferences
   - decisions
   - confirmed facts
3. update assumptions so they reflect only what is still inferred
4. detect contradictions and prioritize resolving them before asking anything new
5. ask only what remains unresolved

Do not repeat answered questions. Prefer refinement over expansion.

## Confidence

Interpret confidence as the likelihood that no further clarification is needed before execution handoff.

Guidelines:
- `< 0.50`: major gaps remain
- `0.50-0.80`: partial clarity
- `0.80-0.94`: only minor gaps remain
- `>= 0.95`: ready to terminate

## Completion Condition

When `confidence >= 0.95`:
- stop appending questions
- follow existing termination and orchestrator handoff behavior
- do not modify the YAML further unless required by termination

## Error Handling

If the YAML is invalid:
- attempt minimal structural repair first
- if repair fails, reconstruct a valid YAML structure
- preserve all `your_answer` values during repair
- keep question IDs, theme IDs, and recorded answers stable

## Token Optimization

- Avoid loading the full YAML into context.
- Avoid rereading historical questions.
- Avoid regenerating unchanged content.
- Process only the active answer block plus the minimal surrounding structure needed for a safe patch.
- Keep commentary minimal.

## User Interaction Rules

- All clarification is recorded in the YAML file.
- Do not output questions in chat.
- Do not paste YAML into chat.
- Do not explain questions in chat.
- On non-terminal turns, output only: `I updated the YAML file with additional questions.`

## Orchestration Notes

- Stay scoped to ambiguity resolution.
- Do not produce plans, specs, code, or deliverables.
- If normalized intent is unavailable, still perform clarification through the file rather than chat.
- This skill must integrate cleanly with the orchestrator pipeline.

## Calibration

Optimize for code, data, project-start, and governance tasks where ambiguity must be reduced before downstream work.
