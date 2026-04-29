---
name: interview-prompt-builder
description: Build downstream prompt files from interview-engine sessions by reading `..interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`, using `your_answer` entries and resolved interview output to create prompt files in `session_prompts/`. Use when turning interview results into reusable prompts, prompt packs, or follow-up prompts.
---

# Interview Prompt Builder

Use this skill after `interview-engine` has populated `interview_questions.yaml`.

## Workflow

1. Open the active session's `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/interview_questions.yaml`.
2. Treat the top-level `output` block and every non-empty `questions[].your_answer` as the source of truth.
3. Carry answered text into the prompt verbatim when it adds precision. Paraphrase only when it makes the prompt clearer.
4. Keep unresolved questions out of the main prompt and place them in a separate follow-up prompt.
5. Write the generated files to `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/` inside the same session folder.
6. Overwrite only the files you generate. Do not rewrite the interview YAML.

## Default outputs

- `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/prompt.md`: the main downstream prompt.
- `.interview-prompt-builder/session-<yyyy-MM-dd_HH-mm-ss>/follow-up.md`: only when unanswered questions remain.

## Prompt composition

Include:

1. Objective Context (Why this exists)
  - Anchors the model in intent—not just mechanics.
  - What are we solving?
  - Why does it matter?
  - What does success unlock downstream?
  - Prevents local optimization (“just write SQL”) vs global optimization (“fit for reporting pipeline”).

2. Artifact Contract (What must be produced)
  - Defines the output as a first-class artifact, not text.
  - File type(s)
  - Naming conventions
  - Schema / structure
  - Storage location
  - Forces Codex to think in deliverables, not prose

3. Input Contract (What is allowed)
  - Constrains the model’s working set.
  - Allowed inputs (files, schemas, APIs)
  - Disallowed assumptions
  - Data boundaries
  - Reduces hallucination and token waste

4. Constraints & Invariants (What must always be true)
  - Hard rules that cannot be violated.
  - Formatting rules
  - Performance constraints
  - Naming rules
  - Idempotency requirements
  - This is where most prompts are weak

5. Execution Model (How to think)
  - Controls reasoning approach without verbosity bloat
  - Step ordering
  - Required checks before proceeding
  - Deterministic vs exploratory behavior
  - Replaces vague “think step by step” with structured cognition

6. State & Memory Model (What persists across steps)
  - Critical for multi-step / orchestrated systems
  - What gets written to disk
  - What gets reused
  - What is ephemeral
  - Enables system-level coherence, not one-off outputs

7. Decomposition Strategy (How to break the problem down)
  - Forces modular thinking
  - Subtasks
  - Boundaries between steps
  - No cross-responsibility rules
  - Mirrors your skill-based architecture

8. Validation Criteria (What “correct” means)
  - Defines success before generation
  - Structural validation
  - Logical validation
  - Edge cases
  - Prevents “looks right” outputs

9. Test Cases / Examples (Ground truth anchors)
  - Used sparingly but strategically
  - Known good inputs/outputs
  - Edge cases
  - Anti-patterns
  - High leverage, high token cost—use intentionally

10. Failure Modes & Recovery Rules
  - Principal-level prompts anticipate failure
  - What to do if input is incomplete
  - What to do if constraints conflict
  - When to stop vs proceed
  - This is a major differentiator vs mid-level prompts

11. Scope Boundaries (What NOT to do)
  - Explicitly restricts behavior
  - No extra features
  - No assumption expansion
  - No format drift
  - Prevents scope creep (huge for your system)

12. Output Formatting Contract
  - Removes ambiguity at the final step
  - Exact structure (JSON, YAML, SQL, etc.)
  - Ordering rules
  - Required/optional fields
  - Makes outputs machine-consable

13. Tooling & Execution Interface
  - How Codex interacts with the environment
  - Scripts to call
  - File operations allowed
  - No direct inline generation vs required
  - Critical for file-based workflows (your direction)

14. Token Efficiency Strategy
  - Principal engineers design for cost
  - Avoid duplication across sections
  - Reference vs restate
  - Minimize examples
  - Prefer schemas over prose
  - This is rarely formalized—but should be

15. Determinism Strategy
  - Ensures repeatable outputs
  - No randomness
  - Stable ordering
  - Explicit defaults
  - Essential for production use

16. Integration Context (Where this fits)
  - Connects the prompt to the larger system
  - Upstream dependencies
  - Downstream consumers
  - Interface expectations
  - Prevents “locally correct, globally useless”

17. Termination Criteria (When the task is done)
  - Defines completion explicitly
  - All files written
  - All validations passed
  - No pending ambiguity
  - Eliminates partial outputs

Do not:

- invent missing answers
- drop answered context
- hide contradictions
- broaden the task beyond the interview result

## Style

- Keep the main prompt concise and actionable.
- Preserve the session's terminology.
- Make the prompt ready to paste into the next Codex stage or agent.
- If the session is still incomplete, make the follow-up prompt ask only for the missing answers.
