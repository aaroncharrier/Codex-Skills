# Orchestrator Contracts

## Session State Schema

Use this strict schema for `session_state`.

```yaml
session_state:
  session_id: string
  status: IN_PROGRESS | COMPLETE | NEEDS_INTERVENTION
  current_stage: INTENT_INTERPRETATION | INTERVIEW_LOOP | SPECIFICATION_GENERATION | EXECUTION_PLANNING | ARTIFACT_GENERATION | VALIDATION
  thresholds:
    confidence_min: number
    assumption_budget_max: integer
  raw_user_prompt: string
  stage_outputs:
    intent_interpreter:
      latest:
      history: []
    interview_engine:
      latest:
      history: []
    specification_builder:
      latest:
      history: []
    execution_planner:
      latest:
      history: []
    artifact_generator:
      latest:
      history: []
    validator_file_writer:
      latest:
      history: []
  latest_valid_artifact:
    present: true | false
    content:
  latest_validation:
    present: true | false
    pass_fail:
    issue_type:
  execution_trace:
    - step: integer
      stage: string
      skill: string
      status: SUCCESS | FAILED | BLOCKED
      notes: string
      persisted_to:
        memory_key: string
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

## Stage Output Expectations

Validate these minimum fields before advancing.

### Intent Interpreter

```yaml
intent_state:
  confidence: number
```

Recommended fields:

- `resolved_inputs`
- `resolved_outputs`
- `constraints`
- `assumptions`
- `intent.ambiguity_notes`

### Interview Engine

Accept either:

```yaml
interview_result:
  confidence: number
```

or a payload whose top-level `confidence` can be read unambiguously.

If the interview output contains user-facing questions, require this structure to preserve pass-through delivery:

```yaml
interview_result:
  confidence: number
  questions:
    - id: string
      prompt: string
```

Additional question metadata is allowed, but the Orchestrator must preserve the full YAML payload exactly when presenting it to the user.

If the raw prompt references an external framework, style guide, screenshot, example artifact, prompt template, or best-practices document, treat these as required clarification targets before allowing transition to `SPECIFICATION_GENERATION` unless the interview output already resolves them explicitly.

### Specification Builder

Require:

```yaml
final_specification:
```

Optional routing flags:

- `needs_interviewing`
- `missing_fields`

### Execution Planner

Require:

```yaml
execution_plan:
```

Optional planning health flags:

- `incomplete`
- `invalid`

### Artifact Generator

Require either:

```yaml
generated_artifact:
```

or:

```yaml
final_artifact:
```

Optional generation health flags:

- `missing_inputs`
- `structural_failure`
- `validation_flags`

### Validator File Writer

Require:

```yaml
validation:
  pass_fail: PASS | FAIL
```

Optional issue typing:

- `issue_type: spec_issue | plan_issue | artifact_issue | structural_issue`

## Persistence Rules

After every stage attempt:

1. Save the raw stage output under `session_state.stage_outputs.<skill_key>.history`.
2. Replace `session_state.stage_outputs.<skill_key>.latest` with the newest raw output.
3. Add an `execution_trace` entry.
4. If file persistence is enabled, mirror the same output into `.orchestrator-sessions/<session_id>/`.

If a stage output is user-facing and structured, persist the exact raw payload before presenting it to the user.

Use stage file keys:

- `intent-interpreter`
- `interview-engine`
- `specification-builder`
- `execution-planner`
- `artifact-generator`
- `validator-file-writer`

## Routing Rules

Use this exact mapping:

```yaml
rework_rules:
  validation_failures:
    spec_issue: specification-builder
    plan_issue: execution-planner
    artifact_issue: artifact-generator
    structural_issue: same_skill_retry
```

Backward routing must be only one stage at a time.

## Final Session Result Shape

Emit:

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

## Mid-Run Display Contract

Mid-run user-facing outputs are not automatically reformatted into `session_result`.

Rules:

- During `INTERVIEW_LOOP`, display the interview question payload exactly as emitted by `$interview-engine`.
- Do not convert structured interview YAML into prose.
- Only emit `session_result` when returning orchestration status rather than active interview questions.
