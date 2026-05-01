---
name: interview-prompt-flow
description: Generate Codex prompt artifacts only, including prompt files, templates, and reusable instruction sets, using an interview-first workflow. Use only when the user explicitly wants a prompt to be written, not when they want a direct answer, tutorial, guide, or general explanation.
---

## Workflow

1. Run `$interview-engine` until it reaches its termination condition.
2. Run `$interview-prompt-builder` using the snapshot as the source of truth.

## Guardrails

- Do not generate any output.
- Do not draft a prompt in chat when the key requirements are still unknown.
- Do not substitute generic defaults for missing answers if those answers would change the prompt structure, audience, constraints, or tone.
- Do not skip the interview step just because the user request sounds simple.
- The interview step is mandatory before any prompt text is produced.