# Project and Issue Type Reference

This file is the source of truth for project-specific Jira behavior in `jira-updater`.

## Supported V1 Project Scope

- `UKG`: supported by default. Do not assume extra local create requirements beyond what live Jira metadata reports.
- `ERCD`: supported by default with the project-specific rules below.
- Future projects: discover them through Atlassian MCP before mutation. Do not assume the `UKG` or `ERCD` rules apply to another project.

## Shared Issue Type Support

- `Epic`
- `Story`
- `Task`
- `Bug`
- `Sub-task`

## Shared Issue Type Rules

- Create actions must enforce only the fields Jira itself requires when live metadata is available.
- Sub-task creates still require a valid parent issue key because Jira creates cannot proceed without a parent.
- For Story, Task, and Bug creates or updates, if `Parent Epic` is present and is not `Not linked`, attempt Epic linking only if live Jira metadata exposes a supported field or operation.

## UKG Rules

- No extra local defaults are required beyond the shared rules.
- Use live Jira metadata to determine whether Epic linking, custom fields, or other issue-type fields are available.

## ERCD Rules

- `Fix Versions` affects board visibility in ERCD. Surface its presence or absence in every ERCD create or update preview.
- If `Fix Versions` is missing for ERCD, do not invent a value. Ask for one when the user wants board-ready behavior, or stop when live Jira metadata marks it required.
- Default `customfield_10093` / `Work Type` to `Feature` for ERCD Epics and ERCD Tasks when the user does not provide a different value.

## Known Project-Scoped Fields

- `UKG`: no extra project-scoped fields are maintained locally yet; live Jira metadata is the only authority.
- `ERCD`: `customfield_10093` / `Work Type` is the only locally defaulted project-scoped field in v1.
- `ERCD`: `customfield_10011` / `Epic Name`, `customfield_10014` / `Epic Link`, and `customfield_10059` / `Story Type` are known fields that may appear in supported flows. Validate them live before use.

## Project-Specific Issue-Type Notes

| Project | Issue Type | Local Notes |
| --- | --- | --- |
| UKG | Epic, Story, Task, Bug | No extra local defaults beyond live Jira metadata. |
| UKG | Sub-task | Require parent issue key. |
| ERCD | Epic | Default `Work Type` to `Feature` if omitted. Surface `Fix Versions` status in preview. |
| ERCD | Story | Surface `Fix Versions` status in preview. |
| ERCD | Task | Default `Work Type` to `Feature` if omitted. Surface `Fix Versions` status in preview. |
| ERCD | Bug | Surface `Fix Versions` status in preview. |
| ERCD | Sub-task | Require parent issue key. Surface `Fix Versions` status in preview when supplied. |
