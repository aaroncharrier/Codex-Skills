---
name: interview-engine
description: Resolve ambiguity in a user request through a YAML-backed requirements interview stored in `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`. Use when Codex needs only the highest-impact clarifications before downstream execution.
---

# Interview Engine

Resolve only the ambiguity that would change the artifact. Keep `interview_questions.yaml` as the source of truth.

## Token Contract

- Avoid loading the full YAML into context.
- Avoid rereading historical questions.
- Avoid regenerating unchanged content.
- Process only the active answer block plus the minimal surrounding structure needed for a safe patch.
- Keep commentary minimal.

## Workflow

1. Identify missing or weakly defined information in:
   - requirements
   - inputs
   - outputs
   - references
   - constraints
   - success criteria
   - codex personality
   - external framework or template alignment
2. Generate a larger internal pool of candidate questions.
3. Output only the top 10 questions.
4. After the user responds read only the active answer block after `# === ACTIVE_ANSWER_BLOCK_START ===`.
5. After the user responds, normalize answers into resolved_inputs, resolved_outputs, constraints, decisions, assumptions, codex_personality, and success_criteria.
6. Resolve contradictions before asking anything new.
7. Recalculate confidence and either ask the next smallest useful set of questions or terminate.

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

## Scope

Do:

- capture missing requirements, inputs, outputs, references, constraints, success criteria, codex personality, or external reference rules
- record questions and answers in the YAML file
- increase confidence only when ambiguity actually decreases

Do not:

- plan, design, validate, or generate deliverables
- explain questions in chat
- reread historical blocks beyond the active answer block

## File Contract

- Path: `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`
- Create the file if it is missing.
- Patch in place otherwise.
- Keep the file valid YAML.
- Preserve every existing `your_answer`.

```yaml
confidence: 0.0-1.0
assumptions:
  - id: A1
    statement: ""
output:
  resolved_inputs: []
  resolved_outputs: []
  constraints: []
  decisions: []
  assumptions: []
  codex_personality: []
  success_criteria: []
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

## Write Rules

- Use the active marker exactly: `# === ACTIVE_ANSWER_BLOCK_START ===`
- Move the marker to the first newly appended question.
- Append only new questions.
- Update only `confidence`, affected assumptions, and `output` fields derived from new answers.
- Keep question ids monotonic.

## Question Rules

Ask only if the answer could change:

- artifact structure or file targets
- required inputs or references
- constraints or acceptance criteria
- validation behavior
- how success is measured
- personality codex should assume
- external template or framework alignment

Prefer `one_of`, `multi_select`, or `numeric` when they fit. Defer lower-impact questions.

## Completion

Stop when `confidence >= 0.95` and blocking ambiguity is resolved.

On non-terminal turns, output only:

`I updated the session-<yyyy-MM-dd_HH-mm-ss> YAML file with additional questions.`
