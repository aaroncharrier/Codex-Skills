---
name: jira-updater
description: Run jira_loader.py validate, preview, or apply against one Jira markdown artifact and return the loader output in a fixed human-readable format.
---

# Jira Updater

Use this skill only when the user explicitly asks to run `validate`, `preview`, or `apply` for exactly one markdown artifact.

## Entry Pattern

Require:

- one explicit subcommand: `validate`, `preview`, or `apply`
- exactly one markdown file path

If either is missing or ambiguous, ask for the explicit subcommand and file path. Do not infer the command from natural language.

## Workflow

1. Run `python scripts/jira_loader.py <subcommand> <file>`.
2. Read the JSON output from the loader.
3. Return a fixed human-readable summary.

## Response Format

Always format the loader output using these sections when present:

- Command
- Status
- File
- Schema
- Action
- Project
- Issue type
- Issue key
- Summary
- Errors
- Warnings
- Pending live resolution
- Key Jira fields
- Result

Formatting rules:

- Surface loader errors directly. Do not reinterpret or expand them.
- List Jira field names from `jira_fields`. Do not analyze field values unless needed for `Result`.
- For `apply`, highlight the resulting issue key and browse URL when `JIRA_BASE_URL` is available.
- Keep the response deterministic, concise, and shallow.

## Examples

```powershell
python scripts/jira_loader.py validate templates/task.md
python scripts/jira_loader.py preview templates/task.md
python scripts/jira_loader.py apply C:\path\to\issue.update.md
```