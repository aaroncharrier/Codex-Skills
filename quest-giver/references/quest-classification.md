# Quest Classification

Classify every request into exactly one type before acting.

## New project quest

Use when the request should create a fresh project that is:

- multi-session
- multi-file
- intended to produce a reusable project asset

This type must use the scaffold workflow from `new-project-workflow.md`.

## Continuation quest

Use when the user is continuing an existing project, campaign, or previously started tutorial inside the current workspace.

## Lightweight drill

Use when the user wants a short exercise, practice loop, or one-session learning task that does not need a project scaffold.

## Debugging challenge

Use when the main goal is diagnosis, repair, or troubleshooting of an existing artifact or workflow.

## Workflow or prompt practice quest

Use when the main goal is to improve how the user works with Codex or ChatGPT, such as prompt design, context packaging, review flow, or tool-use habits.

## Boundary rules

- If the work can reasonably finish in one focused session and does not need reusable project structure, keep it out of the scaffold flow.
- If the work should survive across sessions as a named project asset, upgrade it to `new project quest`.
- If classification changes the required workflow depth, ask the user only for that missing decision.
