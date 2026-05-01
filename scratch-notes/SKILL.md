---
name: scratch-notes
description: Capture short scratch reminders and task notes into an append-only Markdown file at the current project root. Use when the user wants a fast, low-friction place in Codex UI to record a reminder, follow-up, or task note without starting a broader task-management workflow.
---

# Scratch Notes

## Overview

Capture one short user note into `scratch-notes.md` at the current project root. Keep the interaction one-shot, keep the reply to one line, and do not read the existing notes file before writing.

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
- Leave any missing component blank instead of guessing.
- Use `High`, `Medium`, or `Low` only.
- Normalize priority only from explicit priority wording. Leave it blank if the note does not clearly state one.
- Fill `Summary` with a short restatement of the action when that can be done safely. If not, reuse the action wording with light cleanup.
- Use `Note` only for extra context that does not fit cleanly in the other fields. Leave it blank when nothing extra is needed.
- Do not add a status field.

## Required Markdown Shape

Always append a fresh heading for today's date. Do not read `scratch-notes.md` to deduplicate, merge, or inspect prior content.

```md
## YYYY-MM-DD

- Date: YYYY-MM-DD
- Project:
- Priority: High|Medium|Low
- Action Items:
- Summary:
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
- `priority`
- `action_items`
- `summary`
- `note`

Example:

```powershell
@'
[
  {
    "project": "Project Atlas",
    "priority": "High",
    "action_items": "Follow up with Dana on API cutoff",
    "summary": "Follow up on API cutoff with Dana.",
    "note": ""
  }
]
'@ | powershell -ExecutionPolicy Bypass -File ".skill-staging\\scratch-notes\\scripts\\append-scratch-notes.ps1"
```

The script sets the date automatically and always appends to `./scratch-notes.md`.

## Fallback

If the helper script cannot run, append the same Markdown block directly to `scratch-notes.md` without reading the file first. Still keep the reply to one line.
