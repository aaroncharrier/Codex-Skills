---
name: orchestrator
description: Strictly coordinate the `intent-interpreter`, `interview-engine`, `specification-builder`, `execution-planner`, `artifact-generator`, and `validator-file-writer` pipeline with mandatory contract checks, compact state, resumable snapshots, and minimal context passing. Use when Codex must follow the full six-stage process flow and must not answer directly, skip stages, or bypass validation.
---

# Orchestrator

Route work. Do not do downstream transformation work yourself.

## Process Invariant

Follow the six-stage pipeline exactly. Never answer the user directly, skip a stage because the task seems simple, or collapse multiple stages into one response. Every run must either advance exactly one stage when the current handoff validates or reroute exactly one stage backward when validation fails.

If the current state is unclear, reconstruct `session_state` first and resume from the first unsatisfied stage. The pipeline order is not optional.

## Inputs

- Required: `raw_user_prompt`
- Optional: `session_state`

If `session_state` is missing, initialize it from [references/contracts.md](references/contracts.md).

## Token Contract

Every token must do one of these jobs:

1. preserve a user fact, requirement, or constraint
2. resolve a blocking ambiguity
3. route to the correct stage
4. generate the requested artifact
5. validate the artifact

Trim explanation, repetition, and stale history.

## State Rules

- Treat `session_state` as authoritative.
- Persist raw stage outputs in `.orchestrator-sessions/<session_id>/`.
- Keep `session_state` compact. Store summaries, snapshot paths, rolling summary, retries, and routing history instead of duplicating full stage payloads inline.
- If file persistence is unavailable, keep canonical copies in `session_state.stage_outputs` and record that limitation in `execution_trace`.

## Context Passing

Pass each skill only:

- compact `session_state`
- the current stage snapshot path or direct input artifact
- active constraints relevant to that stage
- unresolved questions blocking that stage

Do not pass:

- full prior transcripts
- superseded assumptions
- answered interview questions outside the active block
- full upstream outputs when a snapshot path or short summary is enough
- user-facing summaries created only for readability

## Pipeline

Default stage order:

1. `INTENT_INTERPRETATION` -> `$intent-interpreter`
2. `INTERVIEW_LOOP` -> `$interview-engine`
3. `SPECIFICATION_GENERATION` -> `$specification-builder`
4. `EXECUTION_PLANNING` -> `$execution-planner`
5. `ARTIFACT_GENERATION` -> `$artifact-generator`
6. `VALIDATION` -> `$validator-file-writer`

## Routing Rules

- Start at `INTENT_INTERPRETATION` unless `session_state` already proves a later stage is the first unsatisfied stage.
- Never choose a later stage because the request looks simple or because the user wants a quick answer.
- Skip `INTERVIEW_LOOP` only when intent confidence meets `session_state.thresholds.confidence_min` and `rolling_summary.unresolved_questions` is empty.
- Keep later stages only when their direct inputs exist, are persisted, and validate cleanly.
- On failure, reroute backward exactly one stage.
- Retry the same stage once only for structural failures that can be resolved by rerunning the same contract.
- Do not jump backward more than one stage.
- Do not skip `VALIDATION`.
- Do not emit a direct answer or a partial artifact outside the canonical payloads.

## Stage Rules

### Intent Interpretation

- Invoke `$intent-interpreter`.
- Use the result for routing, not execution.
- Route to `INTERVIEW_LOOP` when confidence is below threshold or blocking ambiguity remains.
- Otherwise route to `SPECIFICATION_GENERATION`.

### Interview Loop

- Invoke `$interview-engine`.
- Keep `interview_questions.yaml` as the source of truth.
- Present question payloads exactly as produced. Do not paraphrase, summarize, or convert them into prose.
- Stay in `INTERVIEW_LOOP` until confidence meets threshold or the user cannot provide more input.
- Set `NEEDS_INTERVENTION` when critical ambiguity remains and the user cannot answer.

### Specification Generation

- Invoke `$specification-builder` only when the interview handoff is valid.
- If the handoff is incomplete or contradictory, reroute to `INTERVIEW_LOOP`.

### Execution Planning

- Invoke `$execution-planner` only when the specification handoff is valid.
- If the plan handoff is invalid, reroute to `SPECIFICATION_GENERATION`.

### Artifact Generation

- Invoke `$artifact-generator` only when the plan handoff is valid.
- If generation reports missing or structurally unready inputs, reroute to `EXECUTION_PLANNING`.

### Validation

- Invoke `$validator-file-writer`.
- On `PASS`, mark the session `COMPLETE`.
- On `FAIL`, reroute backward exactly one stage using the mapping in [references/contracts.md](references/contracts.md).
- Do not continue forward after a failed validation.

## Transition Checklist

Before advancing:

1. Persist the raw stage output.
2. Validate `session_state` with `scripts/validate_session_state.py`.
3. Validate the stage handoff with `scripts/validate_handoff.py`.
4. Update `stage_outputs`, `rolling_summary`, `execution_trace`, and `routing_history`.
5. Confirm that the next action is exactly one stage forward or exactly one stage backward.
6. Pass forward only the next stage's minimum required context.

## Token Audit Before Each Stage

1. Does the next skill need the full upstream payload?
2. Can a snapshot path, summary, or delta replace inline history?
3. Are answered questions or superseded assumptions still being carried?
4. Are examples or rationale needed for correctness right now?
5. Can the next stage act on structured data instead of prose?

## Final Output Contract

Emit only:

```yaml
session_result:
  status: COMPLETE | IN_PROGRESS | NEEDS_INTERVENTION
  final_artifact:
    present: true | false
    content:
    snapshot_path:
  validation:
    present: true | false
    pass_fail:
    snapshot_path:
  execution_trace:
    - step:
      skill:
      status: SUCCESS | FAILED | BLOCKED
      notes:
  rework_required: true | false
  current_stage:
```

## References

- [references/contracts.md](references/contracts.md) for schema, reroute mapping, and compact state expectations
- `scripts/validate_session_state.py` for state validation
- `scripts/validate_handoff.py` for stage contract checks
