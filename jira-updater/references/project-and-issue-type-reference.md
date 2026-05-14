# Project and Issue Type Reference

This file is the source of truth for supported Jira Cloud issue types in the loader.

## Supported Issue Types

- `Epic`
- `Story`
- `Task`
- `Bug`
- `Sub-task`

## Project Scope

- Any Jira Cloud project key is allowed in principle.
- The loader must validate actual project and issue-type availability through Jira create or edit metadata when credentials are available.
- The loader must not hardcode project-specific defaults for issue fields in v1.

## Parent Rules

- `Sub-task` create requests require `parent_issue`.
- `Story`, `Task`, and `Bug` may include `parent_epic`.
- `Epic` must not include `parent_issue`.
- When Jira does not expose a usable editable field for `parent_epic`, stop before mutation.
