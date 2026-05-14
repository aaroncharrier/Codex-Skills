# Custom Field and Required Field Reference

Use this file for generic Jira Cloud field behavior in the loader.

## Required-Field Policy

- For create requests, rely on Jira create metadata when credentials are available.
- If live metadata reports a required field that the artifact does not populate, stop before mutation.
- If live metadata is unavailable, local validation should still enforce the artifact contract only.
- For update requests, patch only the fields the file explicitly supplies plus `clear_fields`.

## Curated Fields

Supported curated keys:

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
- `description` through the markdown body

## Custom Field Rules

- `custom_fields` must be a mapping keyed by Jira field id.
- Custom fields are passed through as authored after the loader verifies the field is editable for the target operation.
- The loader must not infer custom field ids from display names.

## Clear-Field Rules

- `clear_fields` is supported only for `jira-update-v1`.
- Clear only fields named explicitly in `clear_fields`.
- Clear array-like fields with empty arrays where Jira expects arrays.
- Clear other editable fields with `null`.
- Reject attempts to clear `summary`.

## Live Metadata Precedence

- If local assumptions conflict with Jira metadata, Jira metadata wins.
- If a curated field cannot be resolved to one editable Jira field at runtime, stop instead of guessing.
- `parent_epic` and `work_type` must be resolved live because their Jira field ids may vary by project configuration.
