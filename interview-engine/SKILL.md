---
name: interview-engine
description: Resolve ambiguity in prompt-generation and other requests through a JSON-backed requirements interview stored in `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.JSON`.
---

# Interview Engine

Ask an excessive amount of questions until we have a complete understanding of the user request. Follow the workflow until you have a complete understanding.

## Guardrails

- Ask at least 2 rounds of questions
- Ask at least 20 questions in total

## Handoff Contract

- Canonical file: `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.json`
- interview output: `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_output.json`
- interview answers: `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/question_answers.json`

## Workflow

1. Generate a set of questions to ask the user.
2. Use the `Write-InterviewJson.ps1` script to write the questions.
3. emit `I updated the session-<yyyy-MM-dd_HH-mm-ss> JSON file.` in the chat session.
4. Stop until user aknowledges questions are answered.
5. Run `Extract-QuestionAnswers.ps1`
6. Read `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/question_answers.json`
7. If guardrails are meet and you have a complete understanding execute the `Write-OutputJson.ps1` and exit skill
8. If more questions are needed start step 1.

## Token Contract

- Only emit `I updated the session-<yyyy-MM-dd_HH-mm-ss> JSON file.` in the chat

## Question Design

Every question must:
- resolve meaningful uncertainty
- be specific and actionable
- make the reason for asking visible
- reduce future questioning effort
- entice the user for elaboration

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
- ask clarifying questions
- increase confidence only when ambiguity actually decreases

Do not:
- plan, design, validate, or generate deliverables
- draft prompt content in chat before handoff
- explain questions in chat
- reread historical blocks beyond the active answer block

## File Contract

- Path: `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.json`
- Preserve every existing `your_answer`.

```JSON
{
  "confidence": 0.0-1.0,
  "assumptions":
    [
      "",
    ],
  "output": {
    "resolved_inputs": [""],
    "resolved_outputs": [""],
    "constraints": [""],
    "decisions": [""],
    "assumptions": [""],
    "codex_personality": [""],
    "success_criteria": [""]
    },
  "questions": [
    {"question": "",
      "type": ["one_of", "multi_select", "freeform", "ranking", "numeric"],
      "context": "",
      "why_it_matters": "",
      "example_answers": [""],
      "recommended_answer": "",
      "your_answer": ""
    }
  ]
}
```

- Path: `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_output.json`

```JSON
{
    "resolved_inputs": [""],
    "resolved_outputs": [""],
    "constraints": [""],
    "decisions": [""],
    "assumptions": [""],
    "codex_personality": [""],
    "success_criteria": [""]
    }
```