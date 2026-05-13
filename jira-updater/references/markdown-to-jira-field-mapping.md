# Markdown to Jira Field Mapping

Use this file to translate supported markdown inputs into Jira payloads.

## Input Types

- Completed canonical markdown files for new issues.
- Structured markdown update files for existing issues.
- Direct chat instructions plus issue key for existing-issue updates.
- Markdown file or direct chat text plus issue key for standalone comments.
- Explicit local file paths and explicitly referenced thread attachments for attachments.

## General Rules

- Copy the full markdown body into Jira `description` exactly as written for markdown-driven create and update actions.
- For markdown-driven updates, leave Jira fields absent from the markdown unchanged.
- Determine the issue type from the top-level markdown heading, the referenced canonical template, or the explicit user instruction.
- Determine the project from an explicit user instruction or an optional `## Jira Project` heading. If neither exists, stop and ask.
- Accept `## Issue Type` and `## Jira Project` as compatible extension headings when a manually authored markdown file includes them.

## Canonical Heading Contract

Create-mode markdown must follow the canonical heading order for its issue type. Update-mode markdown may omit untouched sections, but every included heading must still match a canonical heading or an allowed extension heading.

### Epic

1. `# Epic`
2. `## Title`
3. `## Fix Versions`
4. `## Priority`
5. `## Assignee`
6. `## Reporter`
7. `## Jira Status or Phase`
8. `## Business Objective`
9. `## Scope`
10. `### Included`
11. `### Excluded`
12. `## Success Metrics`
13. `## Stakeholders`
14. `## Risks / Dependencies`
15. `## Related Stories`

### Story

1. `# Story`
2. `## Title`
3. `## Fix Versions`
4. `## Priority`
5. `## Assignee`
6. `## Reporter`
7. `## Jira Status or Phase`
8. `## Parent Epic`
9. `## Business Problem`
10. `## Desired Outcome`
11. `## Users / Stakeholders`
12. `## Data Sources`
13. `## Acceptance Criteria`
14. `## Success Metrics`
15. `## Dependencies`
16. `## Suggested Sub-tasks`

### Task

1. `# Task`
2. `## Title`
3. `## Fix Versions`
4. `## Priority`
5. `## Assignee`
6. `## Reporter`
7. `## Jira Status or Phase`
8. `## Parent Epic`
9. `## Objective`
10. `## Technical Details`
11. `## Risks / Impact`
12. `## Validation Requirements`
13. `## Dependencies`

### Bug

1. `# Bug`
2. `## Title`
3. `## Fix Versions`
4. `## Priority`
5. `## Assignee`
6. `## Reporter`
7. `## Jira Status or Phase`
8. `## Parent Epic`
9. `## Problem Description`
10. `## Expected Behavior`
11. `## Actual Behavior`
12. `## Business Impact`
13. `## Severity`
14. `## Affected Systems`
15. `## Affected Data Sources`
16. `## Root Cause (If Known)`
17. `## Reproduction Steps`
18. `## Validation Requirements`
19. `## Dependencies`
20. `## Suggested Sub-tasks`
21. `## Attachments / References`
22. `## Definition of Done`

### Sub-task

1. `# Sub-task`
2. `## Title`
3. `## Fix Versions`
4. `## Priority`
5. `## Assignee`
6. `## Reporter`
7. `## Jira Status or Phase`
8. `## Parent Issue`
9. `## Objective`
10. `## Technical Requirements`
11. `## Definition of Done`
12. `## Dependencies`

## Field Map

| Markdown Source | Jira Field | Rule |
| --- | --- | --- |
| `## Title` | `summary` | Copy exactly. |
| Full markdown body | `description` | Copy exactly with no rewriting. |
| `## Fix Versions` or `## Fix Version` | `fixVersions` | Parse list items or line values. Do not invent values. |
| `## Priority` | `priority` | Populate only when the user or markdown supplies it and Jira accepts it. |
| `## Assignee` | `assignee` | Use the explicitly supplied value only. |
| `## Reporter` | `reporter` | Use the explicitly supplied value only. |
| `## Parent Epic` | Epic-link field or operation | Skip when `Not linked`; otherwise validate live support before linking. |
| `## Parent Issue` | `parent` | Require an actual Jira issue key for Sub-task creates. |
| `## Jira Status or Phase` | project-specific status field or text | Treat as informational unless the Jira workflow accepts it for the target operation. |
| `## Issue Type` | `issuetype` | Use only as a compatible extension heading; the top-level heading still defines the canonical contract. |
| `## Jira Project` | `project` | Use when present; otherwise rely on explicit chat context. |

## Parent Resolution Rules

- If `Parent Epic` or `Parent Issue` contains only a title, document name, or another non-key reference, stop and ask for the actual Jira issue key before mutation.
- If `Parent Epic` is `Not linked`, do not send an Epic-link field.
- If the user supplies both a markdown parent reference and a chat-supplied issue key, prefer the explicit Jira issue key.

## Comments and Attachments

- Standalone comments require an issue key and either direct comment text or an explicitly referenced markdown file whose body becomes the comment.
- Attachments require an issue key plus an explicit local file path or explicitly referenced thread attachment.
- For previews, show the exact comment text or attachment path list that will be sent.
