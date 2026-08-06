# Notebook Build Requirements

- Purpose: Give Codex the minimum clear context needed to build a Databricks notebook.
- Rule: Write `TBD` when something is unknown. Do not leave required fields blank.

## 1. Document Control

| Field | Value |
| --- | --- |
| Project Name | `[Project name]` |
| Notebook Name | `[Notebook name]` |
| Owner | `[Name / team]` |
| Status | `[Draft / Ready for Build / Validating / Approved]` |
| Last Updated | `[YYYY-MM-DD]` |
| Related Project Plan | `[Path or link]` |

## 2. Objective and Scope

### Objective

`[What the notebook must do and what output it must produce.]`

### In Scope

- `[Sources, transformations, outputs, and behaviors included]`

### Out of Scope

- `[What Codex should not build]`

### Assumptions or Constraints

- `[Runtime, access, timing, compliance, or cost constraints]`

## 3. Discovery Evidence

Capture only the evidence that materially affects the build.

| Evidence | Key Takeaway | Location |
| --- | --- | --- |
| `[Interview / query / sample data / existing code / ticket]` | `[What Codex should learn from it]` | `[Path or link]` |
| `[Type]` | `[Takeaway]` | `[Path or link]` |

## 4. Inputs

| Source | Object | Key Columns or Grain | Access / Refresh Notes |
| --- | --- | --- | --- |
| `[System name]` | `[catalog.schema.table / file / API]` | `[Primary keys, grain, or critical columns]` | `[Permissions, freshness, or upstream dependency]` |
| `[System]` | `[Object]` | `[Columns or grain]` | `[Notes]` |

## 5. Outputs

| Output | Location | Write Mode | Consumer | Success Condition |
| --- | --- | --- | --- | --- |
| `[Table / view / file]` | `[catalog.schema / path]` | `[Append / Merge / Overwrite]` | `[Team / job / report]` | `[What must be true when successful]` |
| `[Output]` | `[Location]` | `[Mode]` | `[Consumer]` | `[Condition]` |

## 6. Transformation Rules

List only the logic that must be implemented.

| Rule ID | Requirement | Validation |
| --- | --- | --- |
| R1 | `[Exact filter, join, calculation, mapping, dedupe, or reconciliation rule]` | `[How to verify it worked]` |
| R2 | `[Requirement]` | `[Validation]` |

## 7. Runtime and Execution

- Language: `[Python / SQL / Scala / mixed]`
- Databricks runtime: `[Version or TBD]`
- Cluster or warehouse: `[Name / type / TBD]`
- Load pattern: `[Full refresh / Incremental / CDC / Streaming]`
- Rerun behavior: `[Idempotent / merge by key / overwrite partition / TBD]`
- Parameters: `[run_date, env, backfill window, etc.]`
- Schedule or trigger: `[Manual / Job / Workflow / external orchestrator / TBD]`

## 8. Data Quality and Acceptance

| Check | Rule | Expected Result |
| --- | --- | --- |
| `[Freshness / completeness / duplicate / reconciliation / schema]` | `[Exact rule]` | `[Threshold or pass condition]` |
| `[Check]` | `[Rule]` | `[Expected result]` |

### Definition of Done

- `[Notebook reads all required inputs]`
- `[Required transformation rules are implemented]`
- `[Outputs are written to the correct location]`
- `[Required parameters are supported]`
- `[Quality checks pass]`
- `[Validation steps pass]`

## 9. Open Items

- Open questions: `[Anything that could change the build]`
- Risks or dependencies: `[Access, approvals, upstream changes, unresolved logic]`
