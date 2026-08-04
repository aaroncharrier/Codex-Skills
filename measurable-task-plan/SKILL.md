---
name: measurable-task-plan
description: Create exactly one MEASURABLE_TASK_PLAN.md from a generic task, project, bug, improvement, data engineering effort, or technical objective. Use when the user explicitly invokes $measurable-task-plan or asks Codex to convert an objective into an executable task plan with measurable outcomes, three-question clarification batches, discovery tasks for unknowns, task-level acceptance criteria, validation actions, and tangible evidence requirements. Do not use for PROJECT_PLAN.md, WORK_LOG.md, Jira issues, implementation, roadmap creation, business cases, progress tracking, or status updates.
---

# Measurable Task Plan

## Mission

Create one planning artifact named `MEASURABLE_TASK_PLAN.md` in the current project. Convert the user's objective into a detailed, executable task plan that answers: what needs to be done, in what order, and how completion will be proven.

Stop after creating `MEASURABLE_TASK_PLAN.md`. Do not continue into implementation, Jira creation, project-plan updates, work-log updates, or status tracking.

## Workflow

1. Read the user's objective and any available local context.
2. If the request lacks enough detail to create executable tasks with minimum assumptions, ask exactly three clarifying questions and wait.
3. Continue asking questions in batches of exactly three until enough detail exists to plan the work.
4. Convert missing details into discovery tasks when the missing information can reasonably be gathered during execution.
5. Split tasks aggressively until each task is nearly checklist-executable.
6. Organize work into phases when phases make the plan easier to execute; use one phase for small work.
7. Write `MEASURABLE_TASK_PLAN.md`.
8. Respond briefly that the file was created, then stop.

## Interview Rules

Ask questions only for details needed to create executable tasks. Focus on:

- Target system, pipeline, dataset, table, report, workflow, file, or code area.
- Current behavior, defect, pain point, or known gap.
- Desired outcome and measurable success threshold.
- Validation expectations and evidence sources.
- Required environments, access, files, notebooks, jobs, tests, or documentation.
- Known dependencies, constraints, data quality expectations, runtime targets, freshness thresholds, reconciliation requirements, or baseline needs.

Do not ask broad project-management questions unless the answer directly changes the task plan. Do not ask for information that can be turned into discovery work.

If required information is missing and cannot be converted into discovery work without making the plan vague, ask three clarifying questions before writing the file.

## Planning Rules

Every task must have a measurable outcome. If a task does not have one clear measurable outcome, split it further. If a measurable outcome cannot be defined yet, create a discovery task to gather the missing context.

Prefer explicit tasks such as `Add null check for customer_id` over broad tasks such as `Improve customer data quality`.

Do not split so far that the plan becomes noisy with trivial actions unless those actions require separate validation evidence.

Use task IDs directly in headings. Use phase-based IDs when phases exist:

```markdown
#### P1-T1: Establish current pipeline runtime baseline
#### P1-T2: Document current job configuration
#### P2-T1: Refactor expensive join logic
```

Do not add a separate `Task ID` field. Do not include status fields.

Represent open questions as discovery tasks, not as a separate open questions section.

## Scope Boundaries

Do create:

- `MEASURABLE_TASK_PLAN.md`
- Planning assumptions needed to split the work into executable tasks.
- Phase and task hierarchy.
- Detailed tasks with objective, technical action, acceptance criteria, validation, evidence, dependencies, and definition of done.

Do not create or update:

- `PROJECT_PLAN.md`
- `WORK_LOG.md`
- Jira issues or Jira import files
- Roadmaps
- Business cases
- Progress notes
- Status trackers
- Implementation files

Do not include Jira-specific fields or project-tracking fields, including owner, assignee, story points, status, sprint, fix version, labels, components, or priority.

## Required File Scaffold

Write the file with this scaffold:

```markdown
# MEASURABLE_TASK_PLAN.md

## 1. Planning Assumptions

Only assumptions needed to split the work into executable tasks.

## 2. Task Hierarchy

Phase and task breakdown.

## 3. Detailed Task Plan

### [Project Phase]

#### P1-T1: [Task Name]

**Objective:**  
[Concrete outcome this task should produce.]

**Technical Action:**  
[Specific action Codex or the engineer should take.]

**Acceptance Criteria:**  
- [Measurable condition 1]
- [Measurable condition 2]
- [Measurable condition 3]

**Validation Type / Action:**  
[How completion will be proven.]

**Evidence Required:**  
[Artifact, query result, test output, log, screenshot, file path, or review note.]

**Dependencies:**  
[Prerequisite tasks, access, decisions, files, systems, or people.]

**Definition of Done:**  
[Final completion rule.]
```

Do not add extra top-level sections unless they are necessary to make the plan usable.

## Required Sections

### 1. Planning Assumptions

Include only assumptions needed to split the work into executable tasks.

Good assumptions:

- The target pipeline name is unknown, so a discovery task is included to identify it.
- Runtime baseline is unknown, so a baseline measurement task is included before optimization work.
- Invalid record handling is unknown, so a discovery task is included to confirm whether records should be rejected, quarantined, or logged.

Avoid broad assumptions:

- Stakeholders will support the project.
- The project will be delivered on time.
- The architecture will follow best practices.

### 2. Task Hierarchy

Show a compact phase and task breakdown:

```markdown
- Phase 1: Discovery and Baseline
  - P1-T1: Identify target pipeline and owning workflow
  - P1-T2: Establish current runtime baseline
  - P1-T3: Document current job configuration
- Phase 2: Optimization Implementation
  - P2-T1: Identify slowest transformation step
  - P2-T2: Refactor expensive join logic
  - P2-T3: Validate optimized runtime against baseline
```

Use a single phase for small requests:

```markdown
- Phase 1: Implementation and Validation
  - P1-T1: Add null check for customer_id
  - P1-T2: Run validation query for target table
```

### 3. Detailed Task Plan

Create one section per task. Each task must include exactly these fields:

- Objective
- Technical Action
- Acceptance Criteria
- Validation Type / Action
- Evidence Required
- Dependencies
- Definition of Done

Keep the language direct and executable.

## Discovery Task Pattern

Use discovery tasks when requirements, baseline metrics, target systems, validation thresholds, or handling rules are unknown.

```markdown
#### P1-T1: Establish current pipeline runtime baseline

**Objective:**  
Measure the current runtime of the target pipeline before optimization work begins.

**Technical Action:**  
Review available job run history, logs, or monitoring output for the target pipeline.

**Acceptance Criteria:**  
- The target pipeline/job is identified by name.
- Recent successful run history is reviewed.
- Baseline runtime is documented using available evidence.
- Abnormal or failed runs are noted separately.
- Any missing runtime evidence is documented.

**Validation Type / Action:**  
Runtime baseline review.

**Evidence Required:**  
Runtime summary from job history, logs, monitoring output, or manually documented evidence source.

**Dependencies:**  
Access to the pipeline run history or someone who can provide the runtime evidence.

**Definition of Done:**  
A baseline exists that can be used to define measurable performance improvement work.
```

## Validation And Evidence

Use specific validation actions, such as:

- Runtime baseline review
- Databricks job run history review
- Unit test
- Integration test
- Data quality check
- SQL reconciliation query
- Row count comparison
- Duplicate detection query
- Null check query
- Schema validation
- Backfill reconciliation
- Downstream report validation
- Code review
- Configuration review
- Manual review with documented evidence

Avoid vague validation actions such as `Validate it works`, `Review results`, `Test changes`, or `Confirm completion`.

Evidence must be tangible enough for another person to review. Good evidence examples include:

- Query result showing zero null `customer_id` values in the target table.
- Databricks job run history screenshot or exported run summary.
- Test output showing unit tests passed.
- Row count reconciliation table comparing source and target counts.
- Code review approval note.
- File path to updated documentation.
- Log output showing successful pipeline run.
- Before-and-after runtime comparison.

## Data Engineering Prompts

When relevant, consider tasks for source discovery, source-to-target mapping, schema validation, null checks, duplicate checks, referential integrity checks, row count reconciliation, freshness validation, runtime baseline measurement, performance optimization, backfill planning, incremental load behavior, orchestration, failure handling, quarantine/reject logic, data quality evidence, unit tests, integration tests, regression checks, SQL validation queries, PySpark validation, Databricks job configuration, Delta table writes, Snowflake view validation, BI/report validation, and documentation updates required for completion evidence.

Do not add data engineering tasks automatically when they are irrelevant.

## Final Response

After creating `MEASURABLE_TASK_PLAN.md`, respond briefly, for example:

```text
Created MEASURABLE_TASK_PLAN.md with a phase-based task hierarchy and measurable task-level validation requirements.
```

Do not ask whether to start the first task.
