# Runtime Rules

## Allowed Scope

- Accept only the current user request, explicitly referenced local files, and explicitly referenced existing Jira markdown documents.
- Stay limited to local markdown authoring and normalization.
- Refuse Jira API calls, live Jira lookups, Jira updates, and Jira imports.
- Refuse unsupported issue types. Allow only `Epic`, `Story`, `Task`, `Sub-task`, and `Bug`.

## Output Contract

- Write exactly one markdown file per issue.
- Write generated files only to `docs/Jira Documents`.
- Keep markdown only with no YAML frontmatter.
- Keep headings verbatim and in the same order as the canonical template.
- Replace all instructional placeholder text before finalizing a generated issue document.

## Required Shared Fields

Treat these fields as blocking whenever they cannot be derived confidently from the explicit inputs:

- `Title`
- `Fix Versions`
- `Priority`
- `Assignee`
- `Reporter`

Treat `transition` as required, but default it to `Not Started` when the user does not provide a value.

## Required Issue-Type Content

Use the minimum blocking set below when the explicit inputs do not provide enough information to complete the issue responsibly.

- `Epic`: `Business Objective`, `Scope`, `Success Metrics`, `Stakeholders`
- `Story`: `Business Problem`, `Desired Outcome`, `Users / Stakeholders`, `Data Sources`, `Acceptance Criteria`
- `Task`: `Objective`, `Technical Details`, `Validation Requirements`
- `Sub-task`: `Parent Issue`, `Objective`, `Technical Requirements`, `Definition of Done`
- `Bug`: `Problem Description`, `Expected Behavior`, `Actual Behavior`, `Business Impact`, `Severity`, `Affected Systems`, `Reproduction Steps`, `Validation Requirements`

Ask concise grouped clarifying questions and stop before writing if any blocking information is still missing after using only the allowed inputs.

## Generation Rules

1. Decide whether the task is `new` or `refine`.
2. Identify the requested issue type or explicit batch hierarchy.
3. Read only the matching canonical template in `references/templates/`.
4. For `new`, run `scripts/issue_doc_helper.py copy-template` to create the destination file.
5. Replace every placeholder with analytics- or data-engineering-specific content grounded in the user request and explicit artifacts.
6. Keep list sections as bullet lists. Keep `Reproduction Steps` as a numbered list.
7. Keep one issue per file.

## Refinement Rules

- Refine only an explicitly referenced existing Jira markdown document.
- Normalize the full document back to the canonical template for its issue type.
- Preserve valid content, but move it under the canonical headings.
- Remove nonstandard headings instead of carrying them forward.
- Keep `Root Cause (If Known)` as `Unknown` when the cause is not yet known.
- Keep `Parent Epic` as `Not linked` only when the issue is intentionally standalone.

## Batch Rules

- Generate parent-and-child batches only when the user explicitly requests them.
- Create the parent document first.
- In an Epic parent, list child Story, Task, or Bug documents under `Related Stories` in this format:

```md
- Story: [Title] | Document: story__short-title_YYYYMMDD_HHMMSS.md
```

- In a Story, Task, or Bug parent, list child Sub-task documents under `Suggested Sub-tasks` in this format:

```md
- Sub-task: [Title] | Document: sub-task__short-title_YYYYMMDD_HHMMSS.md
```

- In each child document, set `Parent Epic` or `Parent Issue` to the matching parent title and markdown filename.

## Filename Rules

- Use `issue-type__short-title_YYYYMMDD_HHMMSS.md`.
- Use these exact issue-type filename tokens: `epic`, `story`, `task`, `sub-task`, `bug`.
- Normalize `short-title` by lowercasing the title, removing non-alphanumeric characters, converting whitespace and punctuation to single hyphens, trimming edge hyphens, and truncating to 80 characters.
- If the initial filename already exists, advance the timestamp by one second until the path is unique. Change only the `HHMMSS` portion through this collision handling.
- Do not create `docs/Jira Documents`; stop and explain if it is missing.
