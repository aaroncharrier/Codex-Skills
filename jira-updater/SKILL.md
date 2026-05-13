---
name: jira-updater
description: Execute Jira create, update, comment, attachment, and assigned-to-me workflows through Atlassian MCP using explicit action verbs plus completed Jira markdown artifacts, structured update markdown, direct chat instructions, issue keys, or explicit attachment paths. Use when Codex must validate Jira mutations against maintained references and live Jira metadata, preview the exact normalized field map, enforce approval gating, and then safely mutate Jira for UKG, ERCD, or future discovered projects.
---

# Jira Updater

Execute Jira actions from finalized inputs. Keep this skill downstream of markdown authoring: do not invent planning content, do not rewrite the user's markdown, and do not mutate Jira without a preview plus explicit approval.

## Workflow

1. Identify the explicit action verb. Accept only `create`, `update`, `add comment`, `add attachment`, or an assigned-to-me query. If the verb is missing, stop and ask for it.
2. Decide the Jira target count for this run. Default to one create, update, comment, or attachment target unless the user explicitly requests multiple.
3. Gather the allowed artifact:
   - New issue: completed canonical markdown or manual markdown that preserves the canonical heading contract.
   - Update: structured markdown update file, or direct chat instructions plus issue key.
   - Comment: direct chat text or markdown plus issue key.
   - Attachment: explicit local file path or explicitly referenced thread attachment plus issue key.
   - Assigned-to-me: no mutation artifact needed.
4. For markdown-driven work, run `scripts/jira_contract_helper.py parse-markdown` to validate the heading contract and extract sections before building any Jira payload.
5. Read [references/Jira Updater.md](references/Jira Updater.md). Then load only the supporting references you need:
   - [project-and-issue-type-reference.md](references/project-and-issue-type-reference.md)
   - [custom-field-and-required-field-reference.md](references/custom-field-and-required-field-reference.md)
   - [markdown-to-jira-field-mapping.md](references/markdown-to-jira-field-mapping.md)
6. Validate locally first:
   - confirm the supported issue type: `Epic`, `Story`, `Task`, `Sub-task`, or `Bug`
   - confirm `UKG` or `ERCD` when the request uses the v1 default scope; for another project, stop until live Jira discovery confirms the requirements
   - for create actions, enforce only Jira-required fields plus contract requirements such as an explicit project and a sub-task parent key
   - for update actions, leave fields absent from the markdown unchanged
7. Validate live Jira behavior through Atlassian MCP when the relevant capability exists. Prefer Jira project lookup, field discovery, create or edit metadata lookup, issue fetch, issue search, comment helpers, and attachment helpers exposed under the current Atlassian MCP tool names.
8. Build the normalized Jira field map:
   - copy the full markdown body into Jira `description` exactly as written for markdown-driven create and update actions
   - map only explicit fields plus the allowed defaults from the references
   - if `Parent Epic` is present for a Story, Task, or Bug and is not `Not linked`, attempt Epic linking only when live Jira metadata supports it
9. For updates, fetch current Jira values when possible and compute a before-versus-after diff limited to touched fields.
10. Present a markdown preview that shows action, issue key when applicable, project, issue type, summary, required-fields check, validation errors or warnings, normalized Jira fields, comments or attachments to send, diffs when available, and the confirmation requirement.
11. Wait for approval text in the allowlist before any mutation. Treat `Approved`, `Yes, create it`, `Yes, update it`, and `Proceed` as valid examples.
12. Execute the Jira action only after approval. If any live metadata conflict remains unresolved, stop instead of mutating Jira.

## Atlassian MCP

Use Atlassian MCP only. Do not fall back to direct REST calls, ad hoc HTTP requests, or another Jira connector.

Prefer these capability groups when available in the current environment:

- project listing or project lookup
- field discovery or custom-field search
- create or edit metadata lookup
- issue fetch or issue search
- issue create
- issue update
- add comment
- add attachment
- Epic-link helpers or equivalent issue-link or issue-update operations

If the exposed tool names differ from `mcp__atlassian__jira_*`, map to the equivalent Atlassian MCP capability and keep the same validation and approval flow.

## Local Helpers

Use the bundled helper for deterministic contract checks before Jira mutations.

```powershell
python scripts/jira_contract_helper.py detect-action --text "Update UKG-123 from this markdown"
python scripts/jira_contract_helper.py check-approval --text "Approved"
python scripts/jira_contract_helper.py parse-markdown --issue-type Story --mode create --input "C:\path\story.md"
```

## Guardrails

- Reject attachment sources that are not explicit local file paths or explicitly referenced thread attachments.
- Reject markdown that does not follow the canonical heading contract closely enough.
- Do not infer unsupported Jira fields from vague context.
- Do not overwrite existing Jira fields during updates unless the preview includes the change.
- Keep `Jira Updater.md` high level. Treat the project-and-issue-type reference as the source of truth for project-specific requirements.
