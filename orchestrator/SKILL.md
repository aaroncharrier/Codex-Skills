---
name: orchestrator
description: Control a strict six-skill delivery pipeline from raw user prompt through validated artifact. Use when Codex must coordinate `intent-interpreter`, `interview-engine`, `specification-builder`, `execution-planner`, `artifact-generator`, and `validator-file-writer` in a fixed order, enforce handoff contracts, preserve resumable session state, persist each stage output for later reference, and reroute failures without doing transformation work itself.
---

# Orchestrator

## Overview

Use this skill as the control layer for the six-skill pipeline. Route work, validate transitions, preserve state, and persist outputs, but never perform the work delegated to the downstream skills.

## Core Rule

The Orchestrator does not do work. Ensure the right work happens in the right place.

## Responsibilities

- Accept `raw_user_prompt` and optional `session_state`.
- Invoke the six skills by explicit skill name.
- Enforce pipeline order and state transitions.
- Validate every handoff before advancing.
- Persist the output of every skill invocation for future reference.
- Maintain authoritative `session_state`, `current_stage`, retry history, and routing decisions.
- Return a final orchestration result in the required YAML structure.

## Non-Scope

Never:

- interpret user intent directly
- ask interview questions directly
- build specifications
- create execution plans
- generate artifacts
- validate artifacts yourself
- rewrite or merge downstream outputs
- skip a pipeline step unless an explicit reroute rule allows it
- jump backward more than one stage on failure
- "help" a downstream skill by repairing its content

## Required Inputs

Input:

- `raw_user_prompt`

Optional input:

- `session_state`

If `session_state` is missing, initialize it using the schema in [references/contracts.md](references/contracts.md).

## Session State Rules

Treat `session_state` as authoritative. Preserve and update it after every stage attempt.

Minimum required behavior:

- Generate or preserve `session_id`.
- Track `current_stage`.
- Record `status` as `IN_PROGRESS`, `COMPLETE`, or `NEEDS_INTERVENTION`.
- Store every successful or failed skill output under `session_state.stage_outputs`.
- Append every attempt to `session_state.execution_trace`.
- Record reroutes and reasons under `session_state.routing_history`.
- Preserve the latest valid artifact and latest validation result.

Persist stage outputs in two places whenever feasible:

1. In-memory under `session_state.stage_outputs`.
2. In a local session folder for resumability, using `.orchestrator-sessions/<session_id>/`.

Use this file naming pattern for persisted snapshots:

- `01-intent-interpreter.yaml`
- `02-interview-engine.yaml`
- `03-specification-builder.yaml`
- `04-execution-planner.yaml`
- `05-artifact-generator.yaml`
- `06-validator-file-writer.yaml`

On retries, append `-retry-N` before `.yaml`.

If local file persistence is not possible in the current environment, keep the canonical copies in `session_state.stage_outputs` and note the limitation in the execution trace.

## Handoff Validation

Before every transition:

1. Confirm required fields exist.
2. Confirm the payload is structurally valid YAML or JSON-like data.
3. Confirm the payload matches the expected contract for that stage.
4. Block the transition if the handoff is invalid.

Use:

- [references/contracts.md](references/contracts.md) for schema expectations
- `scripts/validate_handoff.py` for per-stage contract checks
- `scripts/validate_session_state.py` for overall state checks

Do not repair invalid outputs. Mark the transition blocked and reroute according to the state machine.

## State Machine

Advance through these stages only:

1. `INTENT_INTERPRETATION`
2. `INTERVIEW_LOOP`
3. `SPECIFICATION_GENERATION`
4. `EXECUTION_PLANNING`
5. `ARTIFACT_GENERATION`
6. `VALIDATION`

### State 1: Intent Interpretation

Invoke `$intent-interpreter`.

Save the result as:

- `session_state.stage_outputs.intent_interpreter.latest`
- `intent_state`

Default threshold rule:

- Treat intent interpretation as a routing snapshot, not a readiness signal for specification generation.
- Use `session_state.thresholds.confidence_min` if present. If it is missing, default it to `0.95`.
- If `intent_state.confidence < session_state.thresholds.confidence_min`, route to `INTERVIEW_LOOP`.
- Only continue directly to `SPECIFICATION_GENERATION` if all of the following are true:
  - `intent_state.confidence >= session_state.thresholds.confidence_min`
  - `intent_state.ambiguity_notes` is empty or absent
  - the raw prompt does not reference an external framework, reference document, screenshot, template, style guide, or best-practices page whose requirements still need to be captured explicitly

For prompt, document, and agent-spec requests, assume clarification is required unless the handoff proves otherwise.

### State 2: Interview Loop

Invoke `$interview-engine`.

Loop with no retry cap until confidence meets threshold or the user cannot provide more input.

Rules:

- Confidence is expected to increase here.
- After each loop, persist the interview output.
- If updated confidence is still below `session_state.thresholds.confidence_min`, remain in `INTERVIEW_LOOP`.
- If updated confidence is at least `session_state.thresholds.confidence_min`, advance to `SPECIFICATION_GENERATION`.
- If the user declines, disappears, or critical ambiguity remains, set `status: NEEDS_INTERVENTION`.
- If the task depends on matching an external template or prompting framework, do not advance while any material structure choice is still represented as an assumption.

Interview transport rule:

- If `$interview-engine` returns a question payload for the user, present that payload exactly as produced.
- Do not paraphrase, summarize, flatten, restyle, or convert interview YAML into plain text.
- Treat delivery of interview questions as a transport operation, not a transformation step.
- Preserve field names, ordering where feasible, and YAML structure when surfacing the questions to the user.
- If the returned interview payload is not valid YAML or does not match the expected question schema, block the transition and keep the session in `INTERVIEW_LOOP`.

### State 3: Specification Generation

Invoke `$specification-builder`.

If the specification output indicates missing required fields or `needs_interviewing`, reroute backward one stage to `$interview-engine`.

Otherwise advance to `EXECUTION_PLANNING`.

### State 4: Execution Planning

Invoke `$execution-planner`.

If the plan is invalid or incomplete, reroute backward one stage to `$specification-builder`.

Otherwise advance to `ARTIFACT_GENERATION`.

### State 5: Artifact Generation

Invoke `$artifact-generator`.

If the artifact output signals missing inputs or structural failure, reroute backward one stage to `$execution-planner`.

Otherwise advance to `VALIDATION`.

### State 6: Validation

Invoke `$validator-file-writer`.

If validation returns `PASS`, mark the session `COMPLETE`.

If validation returns `FAIL`, reroute backward exactly one stage based on issue type:

- `spec_issue` or spec mismatch: `$specification-builder`
- `plan_issue` or plan mismatch: `$execution-planner`
- `artifact_issue` or artifact structural issue: `$artifact-generator`
- `structural_issue`: retry the same stage once, then continue normal routing rules if it still fails

After rerouting, continue the pipeline from that stage. Do not skip forward.

## Invocation Order

Invoke only these skills and only in these roles:

1. `$intent-interpreter`
2. `$interview-engine`
3. `$specification-builder`
4. `$execution-planner`
5. `$artifact-generator`
6. `$validator-file-writer`

Do not substitute other skills for these roles unless the user explicitly changes the pipeline design.

## Backward Routing Rule

On failure, route backward exactly one stage only.

Examples:

- Validation finds a plan issue: route to `$execution-planner`, not `$specification-builder`.
- Planning is incomplete: route to `$specification-builder`, not `$interview-engine`.
- Specification needs more information: route to `$interview-engine`, not `$intent-interpreter`.

The only same-stage retry allowed by default is `structural_issue`.

## Transition Checklist

Before advancing from any stage, do all of the following:

1. Persist the current stage output.
2. Validate the current `session_state`.
3. Validate the stage handoff contract.
4. Record the attempt in `execution_trace`.
5. Update `current_stage` to the next routed state.

If any validation fails, block the transition and record why.

## User-Facing Pass-Through Rules

When a downstream skill returns user-facing structured content, preserve it unless a contract explicitly allows transformation.

For `$interview-engine` specifically:

- Forward interview question payloads to the user verbatim.
- Do not rewrite YAML into prose bullets, numbered lists, or conversational questions.
- Do not extract only the question text and drop required wrapper keys.
- Do not merge interview content into the final `session_result` format while the session is still waiting for user answers.

During `INTERVIEW_LOOP`, the interview payload is the user-facing output unless the payload is invalid.

## Final Output Contract

Return final orchestration output in this form:

```yaml
session_result:
  status: COMPLETE | IN_PROGRESS | NEEDS_INTERVENTION
  final_artifact:
    present: true | false
    content:
  validation:
    present: true | false
    pass_fail:
  execution_trace:
    - step:
      skill:
      status: SUCCESS | FAILED | BLOCKED
      notes:
  rework_required: true | false
  current_stage:
```

Set:

- `COMPLETE` when validation passes.
- `IN_PROGRESS` when the pipeline is still actively moving.
- `NEEDS_INTERVENTION` when user input or unrecoverable ambiguity blocks the next valid step.

## Working Pattern

Use this operational pattern:

1. Load or initialize `session_state`.
2. Validate `session_state` with `scripts/validate_session_state.py`.
3. Determine `current_stage`.
4. Invoke the correct named skill for that stage.
5. Persist the raw output exactly as produced.
6. Validate the handoff with `scripts/validate_handoff.py`.
7. Advance or reroute strictly by the state rules.
8. Repeat until completion or intervention is required.
9. Emit the final YAML result.

## Reference Loading

Read [references/contracts.md](references/contracts.md) whenever you need:

- the strict `session_state` shape
- required stage output keys
- persistence expectations
- issue type to reroute mapping

## Failure Handling

Treat failure as routing, not fixing.

Never:

- clean up a bad specification yourself
- improve a weak plan yourself
- patch an artifact yourself
- reinterpret a validator result to make it pass

Instead:

- record the failure
- persist the failing output
- reroute one stage backward
- continue from that stage
