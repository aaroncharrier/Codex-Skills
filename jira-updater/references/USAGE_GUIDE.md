# Jira Updater Usage Guide

This guide explains how to use the `jira-updater` Python script and how to use the Codex skill efficiently without reading the code.

## What This Skill Does

The skill turns a markdown file into one Jira action.

Supported actions:

- create a new Jira issue
- update an existing Jira issue
- add a comment to an existing Jira issue

The script reads a markdown file, validates it, converts the markdown body into Jira Cloud rich text, shows you a preview, and can then send it to Jira.

The main script is:

- `scripts/jira_loader.py`

The create templates are:

- `templates/epic.md`
- `templates/story.md`
- `templates/task.md`
- `templates/bug.md`
- `templates/sub-task.md`

## The Core Idea

Every run uses exactly one markdown file.

That file has two parts:

1. YAML front matter at the top
2. A markdown body underneath

The YAML front matter contains the machine-readable Jira fields.

The markdown body contains the human-readable content that becomes:

- the Jira issue description for create and update files
- the Jira comment body for comment files

## The Three Commands

Run the script with one of these commands:

```powershell
python scripts/jira_loader.py validate <file>
python scripts/jira_loader.py preview <file>
python scripts/jira_loader.py apply <file>
```

### `validate`

Use this first.

It checks:

- the file has valid YAML front matter
- the schema is supported
- required fields are present
- issue keys look like Jira keys
- unsupported top-level fields are rejected

It does not send anything to Jira.

### `preview`

Use this second.

It shows:

- what action the file represents
- which Jira fields will be sent
- the converted description or comment body structure
- local validation warnings
- live Jira validation warnings and errors when credentials are available

If Jira credentials are not set, `preview` still works, but it skips live Jira metadata checks.

### `apply`

Use this last.

It performs the actual Jira mutation.

Use `apply` only after you have already reviewed the `preview` output.

## How The Codex Skill Conversation Flow Works

If you invoke the skill in chat like this:

```text
Use jira-updater to preview C:\path\to\epic.md
```

the intended skill flow is:

1. run `validate`
2. run `preview`
3. summarize the results in chat
4. stop and wait for your approval
5. run `apply` only after you confirm

The skill should not jump from preview straight to apply in the same turn.

### What The Skill Should Show After Preview

The skill should summarize the most important output instead of pasting raw JSON by default.

That summary should include:

- action
- schema
- file path
- project when applicable
- issue type when applicable
- summary
- issue key when applicable
- warnings
- errors
- the key Jira fields that will be sent

### Approval Replies The Skill Accepts

After a clean or warning-only preview, the skill should accept only:

- `proceed`
- `yes`

Approval rules:

- matching should be case-insensitive
- surrounding whitespace should be ignored
- longer phrases such as `yes, create it`
- other phrases such as `approved` or `ok`

should all be rejected

### What The Skill Should Return After Success

After a successful create:

- return the new Jira issue key
- return the Jira browse URL when `JIRA_BASE_URL` is available

The browse URL format is:

```text
<JIRA_BASE_URL>/browse/<ISSUE_KEY>
```

After a successful update or comment:

- return the target issue key
- return the browse URL when available

## Jira Environment Variables

To let the script talk to Jira Cloud, set these environment variables:

- `JIRA_BASE_URL`
  The base URL for your Jira Cloud site, for example `https://your-company.atlassian.net`
- `JIRA_EMAIL`
  The email address for the Jira Cloud account making the API call
- `JIRA_API_TOKEN`
  The Jira Cloud API token for that account

### Temporary Setup For The Current PowerShell Session

Use this when you want a quick one-time setup in the terminal you are already using:

```powershell
$env:JIRA_BASE_URL = "https://your-company.atlassian.net"
$env:JIRA_EMAIL = "your.name@company.com"
$env:JIRA_API_TOKEN = "your_api_token"
```

These values are available only in the current PowerShell window. If you close that window, you will need to set them again.

### Persistent Setup For Your Windows User Profile

Use this when you want new PowerShell windows and a restarted Codex app to pick the values up automatically:

```powershell
[Environment]::SetEnvironmentVariable("JIRA_BASE_URL", "https://your-company.atlassian.net", "User")
[Environment]::SetEnvironmentVariable("JIRA_EMAIL", "your.name@company.com", "User")
[Environment]::SetEnvironmentVariable("JIRA_API_TOKEN", "your_api_token", "User")
```

This stores the values as user-level environment variables in Windows.

### Restart Steps

After setting persistent user variables:

1. close any PowerShell windows that were already open
2. open a new PowerShell window
3. restart Codex

This matters because existing processes do not automatically inherit newly created environment variables.

### Verify The Variables Are Visible

In a new PowerShell session, run:

```powershell
$env:JIRA_BASE_URL
$env:JIRA_EMAIL
$env:JIRA_API_TOKEN
```

If they are set correctly, PowerShell should print the values.

### Verify The Jira Loader Can See Them

Run a preview command such as:

```powershell
python scripts/jira_loader.py preview templates/task.md
```

If the script can see the environment variables, it will attempt live Jira validation instead of warning that Jira environment variables are missing.

### Important Notes

- `preview` can run without these, but live Jira validation is skipped
- `apply` requires all three
- the current loader reads OS environment variables directly
- the current loader does not auto-load a `.env` file
- do not store the Jira API token inside your markdown issue files

## The Three File Schemas

The `schema` field at the top of the file tells the script what kind of action to perform.

Supported schema values:

- `jira-create-v1`
- `jira-update-v1`
- `jira-comment-v1`

## How Create Files Work

Use a create file when you want to create a new Jira issue.

Start from one of the five templates in `templates/`.

Required front matter fields:

- `schema: jira-create-v1`
- `project`
- `issue_type`
- `summary`

Additional create rule:

- `parent_issue` is required for `Sub-task`

Optional create fields:

- `parent_epic`
- `fix_versions`
- `labels`
- `components`
- `priority`
- `assignee`
- `reporter`
- `work_type`
- `custom_fields`

Example create file:

```md
---
schema: jira-create-v1
project: ERCD
issue_type: Task
summary: Build Jira markdown loader
parent_epic: ERCD-123
fix_versions:
  - 2026.05
labels:
  - codex
  - jira
components:
  - Data Platform
priority: Medium
assignee: 5b10a2844c20165700ede21g
reporter: 5b10a2844c20165700ede21h
work_type: Feature
custom_fields: {}
---

# Objective

Create a Python loader that validates markdown artifacts and sends them to Jira Cloud.

# Technical Details

- Parse YAML front matter and markdown body.
- Convert markdown to ADF.
- Support validate, preview, and apply commands.

# Risks / Impact

- Jira metadata can vary by project.

# Validation Requirements

- Unit tests pass.
- Preview output matches expected Jira fields.

# Dependencies

- Jira Cloud API token
- Project field metadata
```

### Important Create Notes

- `issue_type` must be one of `Epic`, `Story`, `Task`, `Bug`, or `Sub-task`
- `parent_epic` is for `Story`, `Task`, and `Bug`
- `parent_issue` is for `Sub-task`
- `assignee` and `reporter` must be Jira Cloud `accountId` values, not names or emails
- `custom_fields` must use Jira field ids such as `customfield_12345`

## How Update Files Work

Use an update file when you want to change an existing Jira issue.

Required front matter fields:

- `schema: jira-update-v1`
- `issue_key`

Optional update fields:

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

The markdown body is optional.

If the body is present, it replaces the Jira description completely.

If the body is omitted, the description is left unchanged.

Example update file:

```md
---
schema: jira-update-v1
issue_key: ERCD-456
summary: Build Jira markdown loader and preview flow
labels:
  - codex
  - jira
priority: High
clear_fields:
  - work_type
custom_fields:
  customfield_29999: ready-for-review
---

# Updated Description

The loader now supports create, update, and comment actions with markdown-to-ADF conversion.
```

### Important Update Notes

- only fields present in the file are changed
- absent fields remain unchanged
- `clear_fields` is the only supported way to explicitly clear a field
- if you include a markdown body, you are replacing the description, not appending to it

## How Comment Files Work

Use a comment file when you want to add a comment to an existing Jira issue.

Required front matter fields:

- `schema: jira-comment-v1`
- `issue_key`

The markdown body is required.

Example comment file:

```md
---
schema: jira-comment-v1
issue_key: ERCD-456
---

Implemented the initial loader.

- Validation is working
- Preview is working
- Templates are in place
```

## Recommended Step-by-Step Workflow

### For Creating an Issue

1. Copy the correct template from `templates/`
2. Fill in the YAML fields
3. Edit the markdown body
4. Run `validate`
5. Run `preview`
6. Review the preview carefully
7. Run `apply`

### For Updating an Issue

1. Create a new markdown file for the update
2. Set `schema: jira-update-v1`
3. Add `issue_key`
4. Add only the fields you want to change
5. Add a body only if you want to replace the description
6. Run `validate`
7. Run `preview`
8. Run `apply`

### For Adding a Comment

1. Create a markdown file for the comment
2. Set `schema: jira-comment-v1`
3. Add `issue_key`
4. Write the comment in markdown
5. Run `validate`
6. Run `preview`
7. Run `apply`

## What the Script Sends to Jira

You do not need to write Jira ADF manually.

The script converts common markdown into Jira Cloud rich text for you.

Supported markdown patterns include:

- headings
- paragraphs
- bold and italic text
- inline code
- links
- bullet lists
- numbered lists
- block quotes
- fenced code blocks

If a markdown feature is not fully supported, the script falls back safely instead of asking you to write ADF by hand.

## Common Mistakes to Avoid

Avoid these problems:

- using display names instead of Jira `accountId` for `assignee` or `reporter`
- using a parent title instead of a Jira key like `ERCD-123`
- putting unsupported top-level YAML keys in the front matter
- forgetting that update bodies replace the description
- using `custom_fields` keys like `Epic Link` instead of actual Jira field ids like `customfield_10014`
- skipping `preview` and going straight to `apply`

## How to Use the Skill Effectively in Codex

The best way to use this skill is to let files do most of the work and keep prompts short.

### Best Practice 1: Do Not Paste Large Markdown Bodies Into Chat

Instead of pasting the full issue content into the conversation, store it in a local markdown file and reference the file path.

Good:

```text
Use jira-updater to preview C:\work\jira\loader-task.md
```

Less efficient:

```text
Here is a 200-line issue file. Please inspect it and send it to Jira.
```

Why this saves tokens:

- the file already exists locally
- Codex can work from the file directly
- you avoid repeatedly sending the same content in chat

### Best Practice 2: Keep One File Per Jira Action

Do not bundle multiple create, update, and comment actions into one conversation turn if you can avoid it.

Good:

- one file
- one action
- one preview
- one apply

This keeps the skill predictable and keeps the prompt small.

### Best Practice 3: Use Templates Instead of Describing Structure in Chat

If you want a new issue, start from the closest template and edit the file.

That is more efficient than asking Codex to repeatedly explain or reconstruct the schema.

### Best Practice 4: Use Codex for High-Value Help Only

Ask Codex to help with:

- drafting the issue body
- choosing the right template
- troubleshooting preview errors
- finding the right fields to clear
- converting rough notes into a clean artifact

Do not spend tokens asking Codex to repeat information that the guide or templates already provide.

### Best Practice 5: Use Very Specific Requests

Short, precise prompts are best.

Good examples:

- `Use jira-updater to validate C:\jira\bug.md`
- `Use jira-updater to preview C:\jira\task.update.md`
- `Use jira-updater to preview C:\jira\epic.md and I will reply yes if it looks good`
- `Create a jira-update-v1 file for ERCD-456 that changes only priority and labels`
- `Explain why preview says Work Type could not be resolved`

Less efficient examples:

- `Can you look at Jira and figure out what I probably want to do here?`
- `Please explain everything this skill does again`

### Best Practice 6: Reuse Files Across Iterations

If `preview` reveals a problem, edit the same file and rerun `preview`.

That is cheaper than asking Codex to rebuild the artifact from scratch every time.

### Best Practice 7: Let the Script Validate First

If you are working in a terminal, run `validate` and `preview` yourself before asking Codex for help.

Then, if something fails, ask a focused question with the exact error.

Example:

```text
Preview failed for C:\jira\story.md with "Unable to resolve an editable Jira field named Work Type."
Help me adjust the file.
```

That is much cheaper than a broad request like:

```text
My Jira integration is not working. Please debug everything.
```

## Low-Token Workflow You Can Reuse

This is a practical pattern for minimizing token usage:

1. create or edit the markdown file yourself
2. run `validate`
3. run `preview`
4. if both look good, run `apply`
5. only involve Codex if you need help drafting content or fixing a specific error

That workflow uses Codex where it adds the most value and keeps routine work local.

## Suggested Prompt Patterns

Use prompts like these with the skill:

### Create

```text
Use jira-updater to help me fill out templates\task.md for a new Jira task about adding retry logic to the Snowflake loader.
```

### Preview

```text
Use jira-updater to preview C:\Users\Aaron\Documents\jira\new-task.md
```

Then reply with one of these exact confirmations if the preview looks correct:

```text
yes
```

or

```text
proceed
```

### Direct CLI Apply

```text
Use jira-updater to apply C:\Users\Aaron\Documents\jira\new-task.md
```

### Troubleshoot

```text
Use jira-updater to help me fix the preview error for C:\Users\Aaron\Documents\jira\bug.update.md
```

## Final Recommendation

Treat the skill as a file-based Jira tool, not a chat-first Jira tool.

That one mindset shift will save the most tokens:

- keep the artifact in a markdown file
- keep prompts short
- use `validate` and `preview` before `apply`
- ask Codex only for focused help

That gives you the best balance of safety, speed, and low token usage.
