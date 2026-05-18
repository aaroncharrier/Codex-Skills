# Project Roadmap Template

## Document Control

| Field | Value |
| --- | --- |
| Project Name | `[Project name]` |
| Business Sponsor | `[Name / team]` |
| Product / Analytics Lead | `[Name / team]` |
| Data Engineering Lead | `[Name / team]` |
| Technical Owner | `[Name / team]` |
| Version | `[v0.1]` |
| Last Updated | `[YYYY-MM-DD]` |
| Status | `[Draft / In Review / Approved / Active / Closed]` |

## 1. Project Overview

### Objective

`[Summarize the business problem, target users, expected outcome, and why this project matters.]`

### Business Context

- Problem statement: `[What is broken, slow, manual, or unreliable today?]`
- Primary users / stakeholders: `[Who will use or depend on the output?]`
- Business value: `[Revenue, cost, time saved, risk reduction, trust, compliance, etc.]`

### Deliverables

| Deliverable ID | Deliverable | Description | Owner | Due Date | Acceptance Criteria | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | `[Deliverable name]` | `[Description]` | `[Name]` | `[YYYY-MM-DD]` | `[Definition of done]` | `[Status]` |
| D2 | `[Deliverable name]` | `[Description]` | `[Name]` | `[YYYY-MM-DD]` | `[Definition of done]` | `[Status]` |
| D3 | `[Deliverable name]` | `[Description]` | `[Name]` | `[YYYY-MM-DD]` | `[Definition of done]` | `[Status]` |


## 2. Success Metrics

| Type | Metric | Target | Measurement Method |
| --- | --- | --- | --- |
| `[Delivery / Operational / Business]` | `[Metric]` | `[Target]` | `[How measured]` |
| `Delivery` | `[On-time milestone delivery]` | `[Target]` | `[How measured]` |
| `Operational` | `[Scope completion]` | `[Target]` | `[How measured]` |
| `Operational` | `[Pipeline success rate]` | `[Target]` | `[How measured]` |
| `Operational` | `[Freshness SLA attainment]` | `[Target]` | `[How measured]` |
| `Business` | `[Monthly active dashboard users]` | `[Target]` | `[How measured]` |
| `Business` | `[Reduction in manual effort]` | `[Target]` | `[How measured]` |
| `Business` | `[Improvement in business KPI]` | `[Target]` | `[How measured]` |

## 3. Scope

### In Scope

- `[Subject area, dataset, business process, report family, domain, etc.]`
- `[Source systems included]`
- `[Required pipelines, models, semantic layer, dashboards, or data products]`

### Out of Scope

- `[Explicitly excluded systems, metrics, geographies, teams, use cases, etc.]`
- `[Future phase items not covered in this project]`

### Constraints

- `[Budget / tooling / access / timing / compliance / staffing constraints]`

## 4. Architecture Summary

### Current State (if exists)

`[Brief summary of the current architecture and pain points.]`

### Target State

`[Brief summary of the target architecture and how it solves the problem.]`

### Architecture Overview

| Layer | Current State | Target State | Notes |
| --- | --- | --- | --- |
| Source Systems | `[Description]` | `[Description]` | `[Notes]` |
| Ingestion | `[Description]` | `[Description]` | `[Notes]` |
| Storage | `[Description]` | `[Description]` | `[Notes]` |
| Transformation / Modeling | `[Description]` | `[Description]` | `[Notes]` |
| Orchestration | `[Description]` | `[Description]` | `[Notes]` |
| Semantic / Metrics Layer | `[Description]` | `[Description]` | `[Notes]` |
| BI / Consumption | `[Description]` | `[Description]` | `[Notes]` |
| Monitoring / Alerting | `[Description]` | `[Description]` | `[Notes]` |
| Security / Governance | `[Description]` | `[Description]` | `[Notes]` |

### Diagram / References

- Architecture diagram: `[Link or embed reference]`
- Data model / lineage: `[Link]`
- Standards / design docs: `[Link]`


## 5. Questions / Deceisions

Use this section to track unresolved questions, working assumptions, approved decisions, and delivery dependencies in one place. Review it regularly so assumptions do not quietly become facts.

| Type | Description | Why It Matters | Owner | Due | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `[Question / Decision / Risk / Dependency]` | `[Description]` | `[Impact on scope, architecture, testing, or delivery]` | `[Name]` | `[YYYY-MM-DD]` | `[Open / In Review / Resolved / Closed]` | `[Context, blocker, or next step]` |
| `[Question]` | `[Description]` | `[Impact]` | `[Name]` | `[YYYY-MM-DD]` | `[Status]` | `[Notes]` |

## 6. Phases & Milestones

### Phase Summary

| Phase | Goal | Planned Start | Planned End | Exit Criteria | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Discovery & Alignment | `[Goal]` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[Criteria]` | `[Name]` | `[Not Started / In Progress / Blocked / Done]` |
| 2. Data Foundation | `[Goal]` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[Criteria]` | `[Name]` | `[Status]` |
| 3. Modeling & Quality | `[Goal]` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[Criteria]` | `[Name]` | `[Status]` |
| 4. Validation & UAT | `[Goal]` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[Criteria]` | `[Name]` | `[Status]` |
| 5. Rollout & Stabilization | `[Goal]` | `[YYYY-MM-DD]` | `[YYYY-MM-DD]` | `[Criteria]` | `[Name]` | `[Status]` |

### Detailed Task Plan

| Phase | Task | Deliverable | Status | Role | Notes | Impact |
| --- | --- | --- | --- | --- | --- | --- |
| [Discovery / Data Foundation / Modeling / UAT / Rollout] | [Task name] | [Concrete output] | [Not Started / In Progress / Blocked / Done] | [Technical Lead / Product / Analytics Lead / Owner] | [Business or technical context] | [Impact] |
| [Phase] | [Task name] | [Concrete output] | [Status] | [Technical Lead / Product / Analytics Lead / Owner] | [Context] | [Impact] |
| [Phase] | [Task name] | [Concrete output] | [Status] | [Technical Lead / Product / Analytics Lead / Owner] | [Context] | [Impact] |


## 7. Data Quality Plan

### Critical Data Elements

| Data Element | Business Definition | Source | Target | Owner | Priority |
| --- | --- | --- | --- | --- | --- |
| `[Metric / field / entity]` | `[Definition]` | `[System]` | `[Model / table / dashboard]` | `[Name]` | `[Critical / High / Medium]` |
| `[Metric / field / entity]` | `[Definition]` | `[System]` | `[Model / table / dashboard]` | `[Name]` | `[Priority]` |

### Quality Checks

| Check Type | Rule / Validation | Threshold | Frequency | Owner | Escalation Path |
| --- | --- | --- | --- | --- | --- |
| `[Freshness / Completeness / Accuracy / Consistency / Uniqueness / Reconciliation]` | `[Rule]` | `[Threshold]` | `[Hourly / Daily / Weekly / Per run]` | `[Name]` | `[Team / channel / ticket queue]` |
| `[Type]` | `[Rule]` | `[Threshold]` | `[Frequency]` | `[Name]` | `[Path]` |

### Defect Management

- Detection method: `[Automated checks, manual review, user feedback, etc.]`
- Triage owner: `[Name / team]`
- Severity levels: `[Define Sev1 / Sev2 / Sev3 if needed]`
- SLA for response and resolution: `[Target]`
- Audit trail location: `[Tool / ticket system / incident log]`


## 8. Rollout Plan

### Rollout Strategy

- Release approach: `[Pilot / phased / big bang]`
- Target audience / teams: `[Who is included in each rollout wave?]`
- Cutover date: `[YYYY-MM-DD]`
- Hypercare period: `[Start / end dates]`

### Rollout Activities

| Activity | Owner | Planned Date | Status | Notes |
| --- | --- | --- | --- | --- |
| `[Backfill historical data]` | `[Name]` | `[YYYY-MM-DD]` | `[Status]` | `[Notes]` |
| `[Complete UAT signoff]` | `[Name]` | `[YYYY-MM-DD]` | `[Status]` | `[Notes]` |
| `[Enable production schedule]` | `[Name]` | `[YYYY-MM-DD]` | `[Status]` | `[Notes]` |
| `[Train users / publish enablement]` | `[Name]` | `[YYYY-MM-DD]` | `[Status]` | `[Notes]` |
| `[Monitor post-launch issues]` | `[Name]` | `[YYYY-MM-DD]` | `[Status]` | `[Notes]` |

### Rollback / Contingency Plan

- Rollback trigger: `[What conditions require rollback?]`
- Rollback owner: `[Name / team]`
- Rollback steps: `[High-level actions]`
- Communication plan: `[Who is notified and how?]`

## 9. Key Achievements

| Achievement | Outcome | Business Impact |
| --- | --- | --- |
| `[Designed reusable semantic model]` | `[standardized KPI definitions]` | `[reduced reporting inconsistency]` |
| `[Automated finance reporting workflow]` | `[replaced manual process]` | `[saved 20 hrs/month]` |

## 10. Status Definitions

| Status | Meaning |
| --- | --- |
| Not Started | Work has not begun. |
| In Progress | Work is actively underway. |
| Blocked | Work cannot proceed due to an issue or dependency. |
| At Risk | Work is moving, but timeline or scope risk exists. |
| Done | Work is complete and acceptance criteria are met. |
