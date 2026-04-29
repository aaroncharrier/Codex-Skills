# Orchestrator Contracts

Use this file as the compact reference for `session_state`, stage output checks, and rerouting.

## Session State Schema

```yaml
session_state:
  session_id: string
  status: IN_PROGRESS | COMPLETE | NEEDS_INTERVENTION
  current_stage: INTENT_INTERPRETATION | INTERVIEW_LOOP | SPECIFICATION_GENERATION | EXECUTION_PLANNING | ARTIFACT_GENERATION | VALIDATION
  thresholds:
    confidence_min: number
  raw_user_prompt: string
  rolling_summary:
    stable_facts: []
    active_constraints: []
    current_decisions: []
    active_assumptions: []
    unresolved_questions: []
    last_updated_by_stage: string
  stage_outputs:
    intent_interpreter:
      latest:
        status:
        summary:
        snapshot_path:
      history: []
    interview_engine:
      latest:
        status:
        summary:
        snapshot_path:
      history: []
    specification_builder:
      latest:
        status:
        summary:
        snapshot_path:
      history: []
    execution_planner:
      latest:
        status:
        summary:
        snapshot_path:
      history: []
    artifact_generator:
      latest:
        status:
        summary:
        snapshot_path:
      history: []
    validator_file_writer:
      latest:
        status:
        summary:
        snapshot_path:
      history: []
  latest_valid_artifact:
    present: true | false
    snapshot_path: string
    content:
  latest_validation:
    present: true | false
    snapshot_path: string
    pass_fail:
    routing_hint:
  execution_trace:
    - step: integer
      stage: string
      skill: string
      status: SUCCESS | FAILED | BLOCKED
      notes: string
      persisted_to:
        file_path: string
  routing_history:
    - from_stage: string
      to_stage: string
      reason: string
      trigger: string
  persistence:
    storage_mode: session_state_only | session_state_and_files
    session_folder: string
  retry_counters:
    intent_interpreter: integer
    interview_engine: integer
    specification_builder: integer
    execution_planner: integer
    artifact_generator: integer
    validator_file_writer: integer
```

Keep `session_state` compact. Prefer `summary` plus `snapshot_path` over storing duplicated raw payloads inline. If file persistence is unavailable, inline the raw payload only as a fallback.

## Mandatory Flow

The orchestrator is a strict state machine. Follow this order unless the current `session_state` already proves that a later stage is the first unsatisfied contract:

1. `INTENT_INTERPRETATION`
2. `INTERVIEW_LOOP`
3. `SPECIFICATION_GENERATION`
4. `EXECUTION_PLANNING`
5. `ARTIFACT_GENERATION`
6. `VALIDATION`

Rules:

- Only one stage may be active at a time.
- A stage may advance only after its raw output has been persisted and its handoff has validated.
- Do not skip a stage because the request seems obvious, small, or time-sensitive.
- Do not convert stage payloads into prose when the canonical payload exists.
- Do not skip `VALIDATION`.
- If a stage fails, reroute exactly one stage backward using the mapping below.

## Stage Gates

| Stage | Required input | Success output | Failure route |
| --- | --- | --- | --- |
| `INTENT_INTERPRETATION` | `raw_user_prompt` and compact `session_state` | `intent` plus `confidence` | `INTERVIEW_LOOP` if ambiguity remains |
| `INTERVIEW_LOOP` | normalized intent and unresolved questions | interview YAML with `confidence` | `INTERVIEW_LOOP` until ready, then `SPECIFICATION_GENERATION` |
| `SPECIFICATION_GENERATION` | valid interview handoff | `refined_understanding` and `decision_log` | `INTERVIEW_LOOP` |
| `EXECUTION_PLANNING` | valid specification handoff | `execution_plan` | `SPECIFICATION_GENERATION` |
| `ARTIFACT_GENERATION` | valid plan handoff | `artifact`, `artifact_metadata`, `validation_flags` | `EXECUTION_PLANNING` |
| `VALIDATION` | valid artifact handoff | `validation_report` or terminal handoff | `ARTIFACT_GENERATION` or mapped reroute |

## Stage Output Expectations

Validate these minimum fields before advancing.

### Intent Interpreter

Require:

```yaml
intent:
confidence: number
```

### Interview Engine

Accept either:

```yaml
interview_result:
  confidence: number
```

or a payload whose top-level `confidence` can be read unambiguously, such as the canonical `interview_questions.yaml` file.

If the interview output contains questions, preserve the raw YAML payload exactly when presenting it to the user.

### Specification Builder

Require:

```yaml
refined_understanding:
decision_log:
```

### Execution Planner

Require:

```yaml
execution_plan:
```

### Artifact Generator

Accept either the ready-state artifact payload:

```yaml
artifact:
artifact_metadata:
validation_flags:
```

or the incomplete-state halt payload defined in `artifact-generator/references/contract.md`.

### Validator File Writer

Accept either the ready-state validation payload:

```yaml
validation_report:
  pass_fail: PASS | FAIL
```

or the handoff payload defined in `validator-file-writer/references/contract.md`.

Optional:

- `validation_report.routing_hint: spec_issue | plan_issue | artifact_issue | structural_issue | none`

## Persistence Rules

After every stage attempt:

1. Persist the raw stage output to `.orchestrator-sessions/<session_id>/`.
2. Update `session_state.stage_outputs.<skill_key>.latest` with a compact entry.
3. Append a compact history entry with status, summary, and `snapshot_path`.
4. Add an `execution_trace` entry.
5. Validate the next handoff before advancing.

If a stage output is user-facing and structured, persist the exact raw payload before presenting it to the user.

Use stage file keys:

- `intent-interpreter`
- `interview-engine`
- `specification-builder`
- `execution-planner`
- `artifact-generator`
- `validator-file-writer`

## Routing Rules

Use this mapping when `validation_report.routing_hint` is present:

```yaml
rework_rules:
  validation_failures:
    spec_issue: specification-builder
    plan_issue: execution-planner
    artifact_issue: artifact-generator
    structural_issue: same_skill_retry
```

If `routing_hint` is missing, derive the reroute from the highest-severity classified issue:

- specification mismatch or unresolved requirement conflict -> `specification-builder`
- plan or ordering mismatch -> `execution-planner`
- structural, completeness, or artifact-shape issue -> `artifact-generator`

Backward routing must remain one stage at a time.

If the required persistence, validation, or handoff checks fail, stop and reroute instead of continuing forward.

## Final Session Result Shape

Emit:

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

## Mid-Run Display Contract

Mid-run user-facing outputs are not automatically reformatted into `session_result`.

Rules:

- During `INTERVIEW_LOOP`, display the interview question payload exactly as emitted by `$interview-engine`.
- Do not convert structured interview YAML into prose.
- Only emit `session_result` when returning orchestration status rather than active interview questions.
- When a stage is active, do not answer unrelated user questions outside the current stage payload.
