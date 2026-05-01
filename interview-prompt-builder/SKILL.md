---
name: interview-prompt-builder
description: Build downstream prompt file from interview output at `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_output.json`. Use when turning interview results into prompts. Never build a prompt from an unresolved interview or the raw user request alone.
---

# Interview Prompt Builder

Use this skill after `interview-engine` has produced `interview_output.json`. The snapshot is the source of truth for prompt generation.

## Input Contract

- source: `.interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/interview_output.json`

## Workflow

1. You are an expert at writing Codex prompts.
1. Use `Read-OutputJson.ps1` to read the session's `interview_output.json`.
2. Generate the `prompt-<yyyy-MM-dd_HH-mm-ss>.md`

## Guardrails

- Do not synthesize missing requirements from the original request when the snapshot is incomplete.
- Do not read anything excpt the `interview_output.json` file.

## Output Contract

- `interview-engine/session-<yyyy-MM-dd_HH-mm-ss>/prompt-<yyyy-MM-dd_HH-mm-ss>.md`

## Prompt composition

Include:

1. Objective Context
  - Why this exists
  - What problem we are solving
  - Why it matters downstream

2. Artifact Contract
  - File type
  - Naming
  - Schema or structure
  - Storage location

3. Input Contract
  - Allowed inputs
  - Disallowed assumptions
  - Data boundaries

4. Constraints and Invariants
  - Hard rules
  - Formatting rules
  - Naming rules
  - Idempotency requirements

5. Execution Model
  - Step ordering
  - Required checks
  - Deterministic vs exploratory behavior

6. State and Memory Model
  - What persists
  - What is written to disk
  - What is ephemeral

7. Decomposition Strategy
  - Subtasks
  - Boundaries between steps
  - No cross-responsibility rules

8. Validation Criteria
  - Structural validation
  - Logical validation
  - Edge cases

9. Test Cases and Examples
  - Use sparingly
  - Known good inputs and outputs
  - Anti-patterns

10. Failure Modes and Recovery Rules
  - What to do if input is incomplete
  - What to do if constraints conflict
  - When to stop vs proceed

11. Scope Boundaries
  - No extra features
  - No assumption expansion
  - No format drift

12. Output Formatting Contract
  - Exact structure
  - Ordering rules
  - Required and optional fields

13. Tooling and Execution Interface
  - Scripts to call
  - File operations allowed
  - No direct inline generation when a file-based workflow is required

14. Token Efficiency Strategy
  - Avoid duplication
  - Reference instead of restating
  - Prefer schemas over prose

15. Determinism Strategy
  - No randomness
  - Stable ordering
  - Explicit defaults

16. Integration Context
  - Upstream dependencies
  - Downstream consumers
  - Interface expectations

17. Termination Criteria
  - All files written
  - Validations passed
  - No pending ambiguity

Do not:

- invent missing answers
- drop answered context
- hide contradictions
- broaden the task beyond the interview result

## Style

- Keep the main prompt concise and actionable.
- Preserve the session's terminology.
- Make the prompt ready to paste into the next Codex stage or agent.
