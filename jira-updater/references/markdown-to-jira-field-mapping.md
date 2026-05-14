# Markdown to Jira Field Mapping

Use this file to translate the YAML-front-matter artifact contract into Jira Cloud payloads.

## Input Types

- `jira-create-v1` markdown files for new issues
- `jira-update-v1` markdown files for existing issues
- `jira-comment-v1` markdown files for standalone comments

## General Rules

- The markdown body is preserved as authoring input and converted to Atlassian Document Format for Jira Cloud.
- `jira-create-v1` and `jira-update-v1` bodies map to Jira `description`.
- `jira-comment-v1` bodies map to the Jira comment body.
- Unknown top-level YAML keys are rejected unless they are inside `custom_fields`.
- `custom_fields` keys must be explicit Jira field ids.

## Create Contract

Required YAML keys:

- `schema`
- `project`
- `issue_type`
- `summary`

Additional rule:

- `parent_issue` is required for `Sub-task`

Optional curated keys:

- `parent_epic`
- `fix_versions`
- `labels`
- `components`
- `priority`
- `assignee`
- `reporter`
- `work_type`
- `custom_fields`

## Update Contract

Required YAML keys:

- `schema`
- `issue_key`

Optional curated keys:

- `summary`
- `parent_issue`
- `parent_epic`
- `fix_versions`
- `labels`
- `components`
- `priority`
- `assignee`
- `reporter`
- `work_type`
- `custom_fields`
- `clear_fields`

Notes:

- The body is optional.
- When the body is present, it fully replaces Jira `description`.
- Fields absent from the file are left unchanged.
- `clear_fields` is the only supported way to explicitly clear a field.

## Comment Contract

Required YAML keys:

- `schema`
- `issue_key`

The markdown body is required and becomes the Jira comment body.

## Field Map

| Artifact Source | Jira Field | Rule |
| --- | --- | --- |
| `summary` | `summary` | Copy exactly. |
| `project` | `project` | Send as Jira project key. |
| `issue_type` | `issuetype` | Resolve live and send the Jira issue type id for create requests. |
| Body markdown | `description` | Convert markdown to ADF. |
| Comment body markdown | comment `body` | Convert markdown to ADF. |
| `parent_issue` | `parent` | Send Jira issue key. |
| `parent_epic` | editable Epic-link field or `parent` | Resolve live; fail if unsupported or ambiguous. |
| `fix_versions` | `fixVersions` | Convert each value into Jira version-name objects. |
| `labels` | `labels` | Send string array. |
| `components` | `components` | Convert each value into Jira component-name objects. |
| `priority` | `priority` | Send by name. |
| `assignee` | `assignee` | Send by Jira Cloud `accountId`. |
| `reporter` | `reporter` | Send by Jira Cloud `accountId`. |
| `work_type` | editable Work Type field | Resolve live; fail if unsupported or ambiguous. |
| `custom_fields` | matching Jira field ids | Pass through after editability validation. |

## ADF Coverage

The loader converts these markdown constructs directly:

- headings
- paragraphs
- emphasis
- links
- bullet lists
- numbered lists
- block quotes
- fenced code blocks

Unsupported markdown should degrade safely to plain text nodes instead of blocking the request.
