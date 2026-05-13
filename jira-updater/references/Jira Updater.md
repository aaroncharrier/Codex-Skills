# Jira Updater

Use this reference for the high-level execution contract. Keep project-specific requirements in [project-and-issue-type-reference.md](project-and-issue-type-reference.md); do not duplicate or override them here.

## Supported Operations

- Create a new Epic, Story, Task, Sub-task, or Bug from completed markdown.
- Update an existing issue from structured markdown or direct chat instructions plus an issue key.
- Add a standalone comment from direct chat text or markdown plus an issue key.
- Add an attachment from an explicit local file path or explicitly referenced thread attachment plus an issue key.
- List issues assigned to the current user.

## Execution Order

1. Confirm the user supplied an explicit action verb.
2. Resolve the action as `create`, `update`, `add comment`, `add attachment`, or `assigned-to-me query`.
3. Gather the allowed input artifact for that action.
4. Validate the local request contract with the bundled script and the reference files.
5. Validate live Jira behavior with Atlassian MCP whenever the capability exists.
6. Build a normalized Jira field map.
7. For updates, retrieve current Jira values and compute a before-versus-after diff when possible.
8. Present a markdown preview.
9. Wait for approval before every mutation.
10. Execute only the approved Jira action.

## Preview Contract

Every mutation preview must show:

- action
- issue key when applicable
- project
- issue type
- summary
- required-fields check
- validation errors or warnings
- normalized Jira fields to populate
- comment body or attachment list when applicable
- before-versus-after diff for updates when current values are available
- explicit confirmation requirement

## Approval Gate

Require explicit approval before every Jira mutation. Accept only a small allowlist such as:

- `Approved`
- `Yes, create it`
- `Yes, update it`
- `Proceed`

If the reply is outside the allowlist, do not mutate Jira.

## Query Output

For assigned-to-me queries:

- default to not-Done issues only
- return key, summary, and status
- sort by most recently updated first

## Live Metadata Rule

Prefer Atlassian MCP as the source of live truth for project availability, field availability, create or edit metadata, current issue values, comments, and attachments. If live Jira metadata conflicts with maintained references, prefer safe validation, surface the mismatch, and stop before mutating Jira.
