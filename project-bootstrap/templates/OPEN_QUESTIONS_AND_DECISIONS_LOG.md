# Open Questions and Decisions Log Template

Use this template to track unresolved questions, working assumptions, and approved decisions for a data analytics project. Keep it lightweight and current. This log is most useful when it is reviewed regularly and linked to BRD, PRD, SRD, and delivery planning.

## Document Header

| Field | Value |
| --- | --- |
| Project Name | Inventory Visibility Modernization |
| Document Owner | Program Manager / Product Owner |
| Review Cadence | Twice weekly during design, weekly during delivery |
| Status | Active |
| Effective Date | 2026-05-02 |
| Related Documents | BRD, PRD, SRD, Architecture Diagram, Data Contract Register |

## How to Use This Log

- Record unresolved questions before teams treat assumptions as facts.
- Record approved decisions only after the decision-maker is clear.
- Link each important question to an owner and target resolution date.
- When a question is resolved, either close it with a decision or document why it is no longer relevant.

## 1. Decision-Making Scope

| Topic | Guidance |
| --- | --- |
| Purpose | Maintain one visible record of major open questions, assumptions, and decisions |
| Included Items | Scope decisions, source contract questions, ownership gaps, metric definition disputes, release blockers |
| Excluded Items | Sprint task lists, low-level developer notes, duplicate risk logs with no decision impact |
| Primary Audience | Business owner, product owner, engineering lead, BI lead, project manager |

## 2. Open Questions

- **OQ-001**
  - **Question:** Will the supplier feed include all U.S. partner-managed warehouse locations in phase 1?
  - **Why It Matters:** Scope and completeness affect dashboard trust and onboarding effort
  - **Current Working Assumption:** Current assumption is that all U.S. locations are included unless source owner states otherwise
  - **Owner:** Source Owner
  - **Target Resolution Date:** 2026-05-09
  - **Status:** Open
  - **Notes:**  None

- **OQ-002**
  - **Question:** Should late-arriving source data block dashboard publication or allow stale-data display with warning?
  - **Why It Matters:** Affects SLA handling, user expectations, and incident response
  - **Current Working Assumption:** Working assumption is publish with warning only if business approves
  - **Owner:** Product Owner
  - **Target Resolution Date:** 2026-05-07
  - **Status:** Open
  - **Notes:**  None

- **OQ-003**
  - **Question:** Which team is the final approver for the certified available inventory metric?
  - **Why It Matters:** Release cannot complete without clear metric signoff
  - **Current Working Assumption:** Finance and Inventory Operations both review; final owner still to be named
  - **Owner:** Business Sponsor
  - **Target Resolution Date:** 2026-05-12
  - **Status:** Open
  - **Notes:** None

## 3. Decision Log

- **D-001**
  - **Decision Date:** 2026-05-02
  - **Decision Statement:** Phase 1 will publish one daily curated inventory dataset before dashboard redesign begins
  - **Rationale:** Separates data trust work from report layout changes and reduces release risk
  - **Alternatives Considered:** Combined data plus dashboard redesign in one release
  - **Decision Maker / Approver:** Steering Group
  - **Impacted Artifacts:** BRD, PRD, SRD, release plan

- **D-002**
  - **Decision Date:** 2026-05-02
  - **Decision Statement:** `available_qty` will be treated as a certified metric owned by Inventory Operations
  - **Rationale:** Metric disputes already exist and require one business owner
  - **Alternatives Considered:** Shared ownership across BI and operations
  - **Decision Maker / Approver:** Inventory Operations Director
  - **Impacted Artifacts:** Metric definition, semantic layer, UAT

## 4. Assumptions Requiring Validation

- **A-001**
  - **Assumption:** Supplier sends one complete file per business day by 5:30 AM Pacific
  - **Validation Method:** Review source contract and first two weeks of delivery evidence
  - **Owner:** Data Engineering Lead
  - **Due Date:** 2026-05-16
  - **If False, Then:** SLA, runbook, and publish logic must be revised
  - **Notes:** 

- **A-002**
  - **Assumption:** Existing item and location mappings cover at least 98 percent of incoming rows
  - **Validation Method:** Run mapping coverage analysis on sample files
  - **Owner:** Data Steward
  - **Due Date:** 2026-05-10
  - **If False, Then:** Additional cross-reference work becomes a release dependency
  - **Notes:** 

## 5. Follow-Up Actions

- **FA-001**
  - **Action:** Draft data contract language for late-feed handling
  - **Triggered By:** OQ-002
  - **Owner:** Product Owner
  - **Due Date:** 2026-05-08
  - **Status:** Not Started
  - **Notes:** 

- **FA-002**
  - **Action:** Confirm metric approval path with Finance and Operations
  - **Triggered By:** OQ-003
  - **Owner:** Program Manager
  - **Due Date:** 2026-05-06
  - **Status:** In Progress
  - **Notes:** 

## 6. Review and Closure

| Topic | Guidance |
| --- | --- |
| Review Meeting | Review open items in design review, working sessions, and go-live readiness meetings |
| Closure Rule | Close a question only when the answer is documented in a governed artifact or approved in writing |
| Escalation Rule | Escalate any question that can change scope, release timing, certification, or data contract commitments |
| Archive Rule | Keep resolved decisions for historical context; do not delete prior decisions without replacement |

## 7. Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
