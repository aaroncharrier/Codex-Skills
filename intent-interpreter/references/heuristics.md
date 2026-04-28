# Intent Interpreter Heuristics

Use this file only when the prompt is ambiguous enough that artifact classification or confidence scoring needs a tighter calibration.

## Artifact Type Heuristics

- `sql`: The request asks for a query, mentions SQL dialects such as Snowflake or BigQuery, or clearly expects executable SQL.
- `notebook`: The request asks for a notebook, analysis notebook, exploratory workflow, or a stepwise data-analysis artifact.
- `document`: The request asks for a report, memo, brief, proposal, write-up, or other prose-first deliverable.
- `prompt`: The request asks for a prompt, system prompt, assistant instructions, or reusable prompt text.
- `agent_spec`: The request asks for an agent definition, skill spec, orchestration contract, or structured agent behavior description.
- `other`: The deliverable type is unclear, mixed, or not represented by the allowed set.

## Confidence Calibration

- Use `0.10-0.18` when the goal is broad and the output form is unclear.
- Use `0.18-0.26` when the goal is recognizable but scope or inputs are underdefined.
- Use `0.26-0.34` when the artifact type is clear and the main gaps are constraints or source details.
- Use `0.34-0.40` when the request is mostly specific but still requires clarification before execution.

## Assumption Quality

Prefer assumptions that expose uncertainty:

- "The source dataset is not specified."
- "The preferred output format is not stated."
- "The level of production readiness is not defined."

Avoid assumptions that silently decide the task:

- "The user wants a production-grade pipeline."
- "The request should be implemented in Python."
- "The SQL should be optimized for large-scale workloads."

## Output Hygiene

- Preserve business language from the prompt when it carries meaning.
- Favor shorter lists over speculative completeness.
- If the output form is unclear, use `other` instead of forcing a category.
- If an output is guessed, make the guess modest and surface the uncertainty in `ambiguity_notes`.

