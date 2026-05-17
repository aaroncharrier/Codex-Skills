---
name: scratch-notes
description: Capture short scratch notes, reminders, work observations, decisions, and task follow-ups into an append-only Markdown file at the current project root. Use when the user wants a fast, low-friction place in Codex UI to record operational context or career-relevant work evidence without starting a broader task-management workflow.
---

# Scratch Notes

## Overview

Capture one short user note into `scratch-notes.md` at the current project root.

This skill is optimized for fast capture of:

- tasks
- follow-ups
- bugs
- research findings
- decisions
- meeting notes
- achievements
- operational observations

Keep the interaction one-shot, do not read the existing notes file before writing, and return a one-line confirmation only after the append succeeds.

## Workflow

1. Treat the current user note as the full source of truth.
2. Keep the note as one stored item unless multiple tasks are clearly distinct.
3. Normalize each stored item with the fixed field order shown below.
4. Prefer the bundled PowerShell helper script to append the Markdown block.
5. Return a one-line confirmation only after the append succeeds.

## Normalization Rules

- Do not assume facts beyond what the user typed.
- Rewrite lightly for clarity while preserving names, dates, numbers, and direct commitments.
- Keep uncertainty inline when the user expresses it.
- Leave missing fields blank instead of guessing.
- `Type` should normalize only when clearly implied.

Allowed `Type` values:

- Task
- Bug
- Decision
- Research
- Meeting
- Achievement
- Follow-up

If no type is clearly implied, leave blank.

Allowed `Status` values:

- Open
- Done
- Blocked
- Deferred

Normalize status only when clearly implied. Otherwise leave blank.

- `Summary` should contain the clearest concise statement of what happened or what needs to happen.
- `Action Items` should contain concrete follow-up work only.
- `Impact` should capture why the work matters, if explicitly stated or safely inferable from the user's note.
- `Note` should contain extra context that does not fit cleanly elsewhere.
- Do not add priority or other fields beyond the required shape.

## Required Markdown Shape

Always append a fresh heading for today's date. Do not read `scratch-notes.md` to deduplicate, merge, or inspect prior content.

```md
## YYYY-MM-DD

- Date: YYYY-MM-DD
- Project:
- Type:
- Summary:
- Action Items:
- Impact:
- Status:
- Note:
```

- Use Markdown bullets only. Do not use tables.
- Keep the field order fixed.
- Use the current local date in both the heading and the `Date` field.
- Write to `scratch-notes.md` in the current project root.

## Helper Script

Prefer the bundled helper script whenever possible. Run it from the project root and pipe a JSON object or JSON array to stdin.

Expected JSON keys per item:

- `project`
- `type`
- `summary`
- `action_items`
- `impact`
- `status`
- `note`

Example:

```powershell
@'
[
  {
    "project": "Payments",
    "type": "Bug",
    "summary": "Duplicate invoice issue traced to vendor webhook retries.",
    "action_items": "Validate fix in staging.",
    "impact": "Prevent incorrect customer billing.",
    "status": "Open",
    "note": ""
  }
]
'@ | powershell -ExecutionPolicy Bypass -File ".skill-staging\\scratch-notes\\scripts\\append-scratch-notes.ps1"
```

The script sets the date automatically and always appends to `./scratch-notes.md`.

## Fallback

If the helper script cannot run, append the same Markdown block directly to `scratch-notes.md` without reading the file first. Still keep the reply to one line.
