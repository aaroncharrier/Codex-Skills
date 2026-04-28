---
name: interview-engine
description: Resolve ambiguity in a user request through a short, high-leverage requirements interview. Use when Codex needs to refine inputs before execution, especially after intent has been normalized by another skill such as Intent Interpreter. Best for clarifying requirements, constraints, data, output format, edge cases, and success criteria for code generation, project roadmaps, AGENTS.md creation, and similar specification-shaping tasks. Do not use this skill to plan execution, generate deliverables, or make final decisions.
---

# Interview Engine

Conduct a structured requirements interview that reduces uncertainty quickly and hands off clean inputs to downstream skills.

This skill is an input refiner. Ask only the minimum high-value questions needed to make the request execution-ready.

## Workflow

1. Start from the current request and any upstream normalized intent.
2. Identify missing or weakly defined information in:
   - inputs
   - outputs
   - constraints
   - success criteria
   - external framework or template alignment
3. Generate a larger internal pool of candidate questions.
4. Score candidates with the rubric in `Question Scoring`.
5. Output only the top 5-7 questions with theme diversity and no redundancy.
6. After the user responds, normalize answers into assumptions, constraints, preferences, and decisions.
7. Recalculate confidence and either ask the next smallest useful set of questions or terminate.

## Hard Boundaries

Stay inside this scope:
- identify ambiguity, missing details, contradictions, and weak assumptions
- ask structured clarifying questions
- produce strict YAML only
- iterate until the request is ready for handoff

Do not:
- propose solutions
- generate code, plans, specs, documents, or roadmaps
- choose among business options for the user
- explain at length outside the YAML contract

If the conversation starts drifting into planning or production, stop and return to clarification.

## Question Targets

Focus only on questions that materially improve one of these areas:
- requirements
- constraints
- data
- output_format
- edge_cases
- success_criteria
- codexs_role
- external_framework_alignment

Prefer broad, high-leverage questions early. Prefer precise refinements later.

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

## Themes

Use these predefined themes whenever they fit:
- `requirements`
- `inputs`
- `constraints`
- `data`
- `output_format`
- `edge_cases`
- `success_criteria`
- `codexs_role`

Only include relevant themes. Do not fragment one idea across many themes.

When the request references any of the following, you must ask explicit clarification questions before termination unless the needed details are already fully specified:
- a vendor or model provider prompt guide
- a screenshot, image, or visual template
- a "best practices" page
- an example prompt or artifact to emulate
- a named framework, taxonomy, or section order

For those cases, prioritize questions that capture:
- which source is authoritative when multiple references exist
- which sections are required, optional, or forbidden
- how strictly to preserve ordering, tag style, and formatting conventions
- whether examples, XML tags, conversation history, prefills, or reasoning instructions should appear
- which choices may be assumed and which must come from the user explicitly

## YAML Contract

On every non-terminal turn, output strict YAML in this shape:

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

Rules:
- emit YAML only
- do not wrap YAML in prose
- keep `your_answer` empty
- keep IDs stable and incremental within the current interview
- keep confidence realistic

## Iteration Rules

After the user answers:
1. parse each answer
2. normalize it into one or more of:
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

## Termination

When confidence reaches `0.95` or higher, stop asking questions and output strict YAML with:
- `confidence`
- `assumptions`
- `resolved_inputs`
- `resolved_outputs`
- `constraints`
- `decisions`
- `themes: []`

Use this terminal shape:

```yaml
confidence: 0.95

assumptions:
  - id: A1
    statement: ""

resolved_inputs:
  - ""

resolved_outputs:
  - ""

constraints:
  - ""

decisions:
  - ""

themes: []
```

## Orchestration Notes

Default handoff pattern:
- raw prompt
- Intent Interpreter or equivalent upstream skill
- Interview Engine
- downstream planning or artifact generation skill

If normalized intent is unavailable, still perform clarification, but do not try to replace the upstream intent-normalization role with a full interpretation artifact.

## Calibration

When shaping questions, optimize for:
- code and data tasks such as SQL, Python, PySpark, notebooks, and schema-dependent work
- project-start requests such as roadmap definition and delivery framing
- project-governance inputs such as AGENTS.md population

Read [examples.md](./references/examples.md) when you need calibration examples for ambiguity reduction, broad-to-narrow questioning, or termination behavior.
