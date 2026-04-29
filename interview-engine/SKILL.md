---
name: interview-engine
description: Resolve ambiguity in a user request through a YAML-backed requirements interview stored in `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`. Use when Codex needs only the highest-impact clarifications before downstream execution.
---

# Interview Engine

Resolve only the ambiguity that would change the artifact. Keep `interview_questions.yaml` as the canonical record and mirror the current state into a compact snapshot for downstream prompt building.

## Handoff Contract

- Canonical file: `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`
- Compact snapshot: `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_state.json`
- Downstream prompt files: `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_prompts/prompt.md` and `follow-up.md`
- The snapshot must contain only the current active answer block plus the resolved summary fields needed by the builder.

```json
{
  "session_name": "session-<yyyy-MM-dd_HH-mm-ss>",
  "source": ".../interview_questions.yaml",
  "confidence": 0.0,
  "ready_for_handoff": false,
  "assumption_lines": [],
  "output_lines": [],
  "questions": [
    {
      "question_id": "Q1",
      "question": "",
      "your_answer": ""
    }
  ]
}
```

## Token Contract

- Do not load the full YAML into context.
- Do not reread historical questions once they have been resolved into `session_state.json`.
- Only inspect the active answer block after `# === ACTIVE_ANSWER_BLOCK_START ===` plus the minimal surrounding structure needed for a safe patch.
- Keep commentary minimal.

## Workflow

1. Identify missing or weakly defined information in:
   - requirements
   - inputs
   - outputs
   - references
   - constraints
   - success criteria
   - Codex personality
   - external framework or template alignment
2. Generate an internal pool of candidate questions.
3. Ask only the smallest useful batch of high-leverage questions.
4. After the user responds, patch only the active answer block and the derived summary fields.
5. Run `scripts/sync_session_state.ps1` to refresh `session_state.json` from the YAML file. If the shell blocks `.ps1` execution, invoke it with `powershell -ExecutionPolicy Bypass -File`.
6. Recalculate confidence after every answer batch.
7. Stop the interview at `confidence >= 0.95` once blocking ambiguity is resolved, then hand off to `interview-prompt-builder` using the snapshot.

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

- capture missing requirements, inputs, outputs, references, constraints, success criteria, Codex personality, or external reference rules
- record questions and answers in the YAML file
- keep `session_state.json` current as the compact handoff artifact
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
# === ACTIVE_ANSWER_BLOCK_START ===
```

## Write Rules

- Move the marker to the first newly appended question.
- Append only new questions.
- Update only `confidence`, affected assumptions, and `output` fields derived from new answers.
- Keep question ids monotonic.
- Keep the snapshot file in lockstep with the YAML file.

## Question Rules

Ask only if the answer could change:

- artifact structure or file targets
- required inputs or references
- constraints or acceptance criteria
- validation behavior
- how success is measured
- personality Codex should assume
- external template or framework alignment

Prefer `one_of`, `multi_select`, or `numeric` when they fit. Defer lower-impact questions.

## Completion

Stop when `confidence >= 0.95` and blocking ambiguity is resolved.

On non-terminal turns, output only:

`I updated the session-<yyyy-MM-dd_HH-mm-ss> YAML file and session_state.json with additional questions.`
