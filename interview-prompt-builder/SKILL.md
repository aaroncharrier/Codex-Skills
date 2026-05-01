---
name: interview-prompt-builder
description: Build downstream prompt files from the lightweight interview snapshot at `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_state.json`, falling back to `interview_questions.yaml` only if the snapshot is missing. Use when turning interview results into reusable prompts, prompt packs, or follow-up prompts.
---

# Interview Prompt Builder

Use this skill after `interview-engine` has produced `session_state.json`. The snapshot is the source of truth for prompt generation. Do not load the full interview YAML unless the snapshot is missing.

## Input Contract

- Preferred source: `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_state.json`
- Fallback source: `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`
- If the snapshot is missing, regenerate it with `scripts/sync_session_state.ps1` before building the prompt. If the shell blocks `.ps1` execution, invoke it with `powershell -ExecutionPolicy Bypass -File`.
- Read only the compact snapshot data needed for the prompt.

## Workflow

1. Open the session's `session_state.json`.
2. Treat the top-level `confidence`, `assumption_lines`, `output_lines`, and every non-empty `questions[].your_answer` as the source of truth.
3. Carry answered text into the prompt verbatim when it adds precision. Paraphrase only when it makes the prompt clearer.
4. Keep unresolved questions out of the main prompt and place them in a separate follow-up prompt.
5. Write the generated files to `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_prompts/`.
6. Overwrite only the files you generate. Do not rewrite the interview YAML or the snapshot.

## Default outputs

- `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_prompts/prompt.md`
- `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/session_prompts/follow-up.md` only when unanswered questions remain.

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
- If the session is still incomplete, make `follow-up.md` ask only for the missing answers.
