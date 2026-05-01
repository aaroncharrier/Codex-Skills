---
name: end-of-day-review
description: Gather approved end-of-day evidence, verify gaps through $interview-engine, and merge a factual daily entry into a project-scoped weekly Markdown work log. Use when Codex needs to document a user's work day from Teams chats, Teams meeting chats, Outlook calendar events, sent emails, Codex session logs, and user input without inventing missing facts or creating extra trackers.
---

# End Of Day Review

## Overview

Document one work day into one weekly Markdown record that the user can revisit later for annual review preparation, year-end recall, and resume updates. Keep the workflow factual, low-friction, and scoped to work documentation rather than general journaling.

## Required Output

- Store exactly one required persistent artifact per week: `[project-folder]/YYYY-MM-DD_to_YYYY-MM-DD/weekly-log.md`
- Store the weekly record inside the user-designated project folder, never inside this skill package
- Add supporting files only when the user explicitly requests them
- Produce Markdown only; do not create JSON, databases, dashboards, or alternate report formats by default

## Approved Evidence Sources

Use only these evidence categories unless the user explicitly expands scope:

- Teams chats
- Teams meeting chats
- Outlook calendar events
- Sent emails
- User chat input
- Codex session logs
- User answers collected through `$interview-engine`

Do not assume other enterprise systems or trackers exist. Do not assume plugin access will always be available. Do not assume missing facts from incomplete evidence.

## Workflow

Follow this order every time:

1. Resolve the target project folder.
2. Resolve the current weekly folder name as `YYYY-MM-DD_to_YYYY-MM-DD`.
3. Locate or create `weekly-log.md` inside that weekly folder.
4. Gather candidate evidence from the approved source list only.
5. Summarize likely work items from plugin evidence without treating them as confirmed facts.
6. Start a follow-up interview with `$interview-engine`.
7. Ask 2-3 broad reflection prompts first.
8. Ask targeted confirmation questions for gaps, contradictions, and ambiguous evidence.
9. Write or merge only confirmed content into the current day section of `weekly-log.md`.
10. Create supporting files only when explicitly needed.

Prefer deterministic behavior over exploratory behavior once writing begins.

## Storage Model

- Weekly folder naming pattern: `YYYY-MM-DD_to_YYYY-MM-DD`
- Required file name: `weekly-log.md`
- Known-good example:

```text
2026-04-27_to_2026-05-03/
  weekly-log.md
```

- Use the project's existing week-boundary convention if one already exists.
- If the project does not already make the week boundary obvious, ask before introducing a new rule.
- Treat one heading per day as the unit of update. Do not split the same day across multiple files or headings.

## Daily Entry Schema

Use the exact daily heading format `# Monday 2026-04-27` and keep the section order fixed. Use the template in `assets/day-entry-template.md` when creating or replacing a day section.

Every day entry must capture the date in the heading plus the following sections:

- `## Summary`
  Include `Project / Workstream`, a concise summary of the day, and `Impact / Outcome`.
- `## Acheivements`
  Use this exact heading. Include `Key accomplishments`, `Measurable results`, and `Skills demonstrated`.
- `## Work Completed`
  Include `Work completed`, `Technologies used`, and `Notable collaboration`.
- `## Decisions`
  Include only confirmed decisions and why they mattered.
- `## Blockers`
  Include active blockers, risks, or unresolved questions that matter for the next work day.
- `## References`
  Render this section as bullets only. Each bullet must contain a file name or stable pseudo-file label in backticks plus the context for including it.
- `## Next Steps`
  Include the next concrete actions.

Keep prose concise under every section. Use bullets only in `## References`.

## Reference Rules

Represent references as bullets in this format:

- `source-label.ext`: What the source was and why it was included.

Use real filenames when they exist. When a source does not correspond to a stored file, use a stable pseudo-file label without creating a new file by default. Examples:

- `teams-chat-2026-04-30.md`
- `teams-meeting-chat-2026-04-30.md`
- `outlook-calendar-2026-04-30.ics`
- `sent-mail-2026-04-30.eml`
- `codex-session-2026-04-30.txt`
- `interview-answers-2026-04-30.json`

Do not paste raw transcripts, long email bodies, secrets, private personal information, or copied supporting material into the weekly folder unless the user explicitly asks for that.

## Evidence Gathering Rules

- Treat Teams, Outlook, calendar, and sent mail plugin results as candidate evidence only.
- If plugin evidence is available, summarize likely work items before questioning the user.
- Do not promote candidate evidence to fact until the user confirms it.
- If evidence is noisy, incomplete, or contradictory, mark it as unconfirmed during questioning and keep it out of the weekly log until verified.
- If a plugin is unavailable, disconnected, or denied, continue with the remaining approved sources and the user interview. Note the unavailable sources in the working context; add them to the log only if that unavailability materially affected what could be confirmed.

## Interview Rules

Use `$interview-engine` after evidence gathering, not before it. Seed the follow-up with concise questions that reduce ambiguity instead of replaying full source content.

If you invoke any PowerShell helper script during this workflow, call it with `-ExecutionPolicy Bypass`.

Start with broad reflection prompts such as:

- What work mattered most today?
- Which outcome, accomplishment, or decision should future-you remember?
- What is still open, blocked, or risky going into the next work day?

Then ask targeted confirmation questions for:

- unclear project or workstream names
- missing outcomes or impact
- missing measurable results
- ambiguous technologies used
- unclear collaborators
- conflicting evidence across sources
- uncertain decisions, blockers, or next steps

If `$interview-engine` is unavailable, fall back to a direct manual interview that follows the same broad-then-targeted pattern. Keep the manual fallback within the same approved evidence scope.

## Merge Rules

If the weekly file already contains the current day:

1. Update only that day section.
2. Preserve prior confirmed content unless the user corrects it or a newer confirmed statement replaces it.
3. Add newly confirmed facts to the matching section without duplicating existing content.
4. Prefer clearer user-confirmed wording over older vague wording.
5. Leave unchanged sections intact when no new confirmed data exists.
6. Never write unconfirmed candidate items into the log.
7. Never create a second heading for the same day.

If the weekly file does not contain the current day, append one new day section using the template asset.

## Privacy And Scope Guardrails

- Exclude secrets, private personal information, and unverified claims.
- Do not infer missing facts from partial evidence.
- Do not broaden this workflow into a resume generator, dashboard, annual review generator, or general knowledge-management system.
- Do not pull from sources outside the approved evidence list unless the user explicitly expands scope.
- Do not store copied supporting materials by default.

## Writing Rules

- Write human-readable Markdown that is predictable for later automation.
- Keep the section order identical across days.
- Write concise prose under each section.
- Write only confirmed content.
- Favor specific outcomes over vague activity summaries.
- When nothing is confirmed for a field, say so plainly instead of guessing.
