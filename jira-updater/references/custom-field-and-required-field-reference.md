# Custom Field and Required Field Reference

Use this file for generic Jira field behavior. Treat live Atlassian MCP metadata as the authority whenever it is available.

## Required-Field Policy

- For create actions, enforce only Jira-required fields reported by live metadata when that capability exists.
- If live metadata is unavailable, fall back to the safe minimum contract: project, issue type, summary, and parent issue for Sub-tasks.
- Do not treat template placeholders marked `[Required]` as automatic Jira-required fields.
- For update actions, patch only the fields the user explicitly supplies. Leave all other Jira fields unchanged.

## Known Field IDs

| Jira Field | Purpose | Notes |
| --- | --- | --- |
| `customfield_10011` | Epic Name | Use only when live metadata exposes it for the target project and issue type. |
| `customfield_10014` | Epic Link | Prefer live metadata or equivalent Epic-link capability over assumptions. |
| `customfield_10059` | Story Type | Populate only when the user explicitly provides it and Jira accepts it. |
| `customfield_10093` | Work Type | Default to `Feature` only for ERCD Epics and ERCD Tasks. |

## Live Metadata Precedence

- If a maintained field ID exists but live metadata says the field is unavailable, unavailable wins.
- If live metadata reports a required field that is absent from the local references, surface the gap and stop before mutation.
- If project-specific references conflict with live metadata, prefer safe validation and resolve the discrepancy before mutation.

## Create and Update Behaviors

- Preserve the full markdown body as the Jira `description` for markdown-driven create and update actions.
- Do not clear a Jira field during update unless the user explicitly asks to clear it and the preview shows the cleared value.
- Do not infer labels, components, priority, assignee, sprint, story points, Epic Link, Story Type, or Fix Versions from vague context.
