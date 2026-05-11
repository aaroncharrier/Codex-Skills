# Business Requirements Document (BRD) Template for Data Analytics Projects

Use this template for larger projects when the business case, scope, and approvals need to stand on their own before product and technical design.

Shared terms used in this template:

- `source onboarding`: Bringing a new file, API, database, or partner feed into the analytics platform.
- `certified metric`: A business-approved definition for a KPI, measure, or calculation used across reporting.
- `semantic layer`: The reporting-friendly layer that presents business names, definitions, and governed logic.
- `consumer-facing dataset`: A curated table, view, or model intended for reporting or analyst consumption.
- `freshness SLA`: The expected time by which data must be available for business use.

Suggested document header:

- Project Name:
- Business Owner:
- Document Owner:
- Version:
- Status:
- Date:
- Related Documents:

## 1. Executive Summary
**Definition**  
A concise summary of the business need, the expected value, and the high-level change the organization is approving.

**What belongs here**
- The business problem in plain language.
- The business value of solving it.
- A short statement of what the project will deliver from a business perspective.

**What does not belong here**
- Detailed field mappings, source-to-target logic, or SQL.
- Step-by-step product behavior.
- Architecture decisions such as Snowflake warehouse sizing or Databricks job design.

**Examples**
- "The business needs a trusted daily inventory view that combines a new supplier feed with existing warehouse data so planners can make replenishment decisions before 8:00 AM Pacific."
- "This initiative will reduce manual reconciliation and improve confidence in certified product availability metrics used in MicroStrategy reporting."

**Helpful context**  
For analytics work, this section should sound like a funding or approval summary. If a reader only sees this section, they should still understand why the source onboarding or metric work matters to the business.

## 2. Business Problem / Opportunity
**Definition**  
A clear statement of the gap, pain point, or opportunity that justifies the project.

**What belongs here**
- Current business pain such as missing visibility, slow decisions, inconsistent metric definitions, or unreliable reporting.
- Quantified or observable impact where possible.
- Why the problem matters now.

**What does not belong here**
- Proposed technical solution details.
- User interface design notes.
- Low-level implementation constraints unless they directly create business risk.

**Examples**
- "Inventory planners cannot trust on-hand quantity in the dashboard because the current report excludes a key supplier-managed warehouse feed."
- "Revenue leadership wants a certified gross margin metric because multiple teams currently calculate it differently in ad hoc reports."

**Helpful context**  
In a data analytics environment, business problems often show up as low trust, delayed data, duplicate definitions, or manual spreadsheet work. Describe the operational consequence, not the engineering fix.

## 3. Business Goals and Objectives
**Definition**  
The business outcomes the initiative is expected to achieve.

**What belongs here**
- Target outcomes such as improved visibility, reduced cycle time, increased trust, or faster issue detection.
- Specific objectives that can later inform PRD and SRD requirements.
- Priority or ranking if goals are not equally important.

**What does not belong here**
- Feature lists framed as goals.
- Technical tasks such as "build Delta table" or "create Snowflake task."
- Vague statements with no observable outcome.

**Examples**
- "Make new supplier inventory available by 7:30 AM local warehouse time on business days."
- "Establish one certified definition of available-to-sell inventory across operational and executive dashboards."

**Helpful context**  
Strong BRD goals translate naturally into product and technical requirements. If the goal cannot be measured or observed by the business, it is probably too vague.

## 4. Stakeholders and Roles
**Definition**  
The people, teams, and decision-makers affected by the project or responsible for approvals and inputs.

**What belongs here**
- Business sponsors, data owners, operational teams, analysts, BI teams, and engineering partners.
- The role each stakeholder plays: approver, subject matter expert, consumer, or support owner.
- Decision rights where relevant.

**What does not belong here**
- Full technical system ownership matrices.
- Detailed team capacity plans.
- User interface personas beyond a high-level business role.

**Examples**
- "Inventory Operations Manager: defines required freshness and exception handling expectations."
- "Finance Reporting Lead: approves the certified metric definition used in enterprise dashboards."

**Helpful context**  
Analytics projects often fail because a source owner, metric owner, or reporting owner was not identified early. Call out who defines the business truth, not just who builds the pipeline.

## 5. Current State
**Definition**  
A description of how the business operates today and where the pain is occurring.

**What belongs here**
- Existing reports, manual workflows, current source limitations, and known trust issues.
- Current turnaround times, reconciliation steps, or missing coverage.
- Business workarounds in place today.

**What does not belong here**
- Desired future workflow.
- Detailed system diagrams.
- Technical design proposals.

**Examples**
- "Analysts manually join supplier CSV files with warehouse extracts before publishing the daily inventory workbook."
- "MicroStrategy dashboards currently show only internal warehouse stock, leaving partner-managed inventory invisible to planners."

**Helpful context**  
This section helps separate current pain from the future solution. In data work, current state is often fragmented reporting, spreadsheet-based metric logic, or delayed ingestion.

## 6. Future State
**Definition**  
The target business condition after the initiative is delivered.

**What belongs here**
- How the business will operate differently once the new data, metric, or reporting capability is in place.
- Expected decisions, behaviors, or process improvements.
- Business-facing outcomes, not internal engineering mechanics.

**What does not belong here**
- Detailed transformation logic.
- Technology product comparisons.
- Sprint-level delivery details.

**Examples**
- "Planners review one trusted inventory dashboard each morning without needing manual spreadsheet reconciliation."
- "All operational reports use the same certified definition of available quantity across warehouse, supplier, and executive reporting."

**Helpful context**  
Future state should read like a business outcome narrative. If you catch yourself describing notebook steps, schema design, or scheduling mechanics, that content belongs later in the SRD.

## 7. Business Scope
**Definition**  
The business capabilities, domains, and outcomes that are included in this initiative.

**What belongs here**
- Which business processes, source domains, dashboards, and metric areas are in scope.
- The populations, geographies, or business units affected.
- The business boundaries for phase 1 if delivery is staged.

**What does not belong here**
- Technical component lists such as exact jobs, tables, or APIs.
- Detailed backlog items.
- Anything better expressed as out-of-scope.

**Examples**
- "Phase 1 includes onboarding the new supplier feed for U.S. distribution centers and exposing daily inventory balances in the existing operations dashboard."
- "The project includes certification of the in-stock percentage metric for operations and merchandising reporting."

**Helpful context**  
For analytics work, scope is usually framed by business data domain, consumer audience, and decision process. Keep the language business-facing even when the work is data-heavy.

## 8. Out of Scope
**Definition**  
An explicit statement of what the business should not expect this initiative to deliver.

**What belongs here**
- Exclusions that prevent assumption creep.
- Deferred regions, advanced analytics, upstream fixes, or unrelated report redesigns.
- Items intentionally left for later phases.

**What does not belong here**
- Hidden requirements that are actually needed for success.
- Technical excuses framed as scope statements.
- Generic filler such as "anything not listed above."

**Examples**
- "Historical restatement of three years of inventory data is not included in the initial rollout."
- "This project will not redesign warehouse operating procedures or replace the current MicroStrategy dashboard with a new BI platform."

**Helpful context**  
This section is especially important for source onboarding work. Business partners often assume a new feed also means historical backfill, process redesign, and new reporting all at once.

## 9. Assumptions and Constraints
**Definition**  
Conditions believed to be true and limits that may shape delivery or business outcomes.

**What belongs here**
- Assumptions about source availability, stakeholder participation, business definitions, and approval timing.
- Constraints such as compliance rules, release windows, or business calendar dependencies.
- Short statements that can be validated later.

**What does not belong here**
- Detailed engineering risk logs.
- Broad technical design explanations.
- Open questions that have no current working assumption.

**Examples**
- "The supplier feed owner will provide daily files by 5:30 AM Pacific on business days."
- "Any changes to certified finance metrics must pass governance review before dashboard publication."

**Helpful context**  
In analytics programs, assumptions often hide in source schedules, ownership, and data definition alignment. Surface them here before they become late delivery surprises.

## 10. Risks and Dependencies
**Definition**  
Business-facing risks and external conditions that can affect success.

**What belongs here**
- Risks tied to data quality, business adoption, upstream source reliability, or approval delays.
- Dependencies on source teams, governance boards, security approvals, or reporting teams.
- The likely business consequence if a risk occurs.

**What does not belong here**
- Detailed retry strategy or technical error handling design.
- Full project plan tasks.
- Minor engineering implementation notes.

**Examples**
- "If the supplier feed arrives late, planners may not have current stock visibility before purchase-order cutoffs."
- "Certification of the gross margin metric depends on signoff from Finance and Merchandising before downstream report changes can go live."

**Helpful context**  
Keep the language focused on operational impact. Technical details may exist, but the BRD should explain why a dependency matters to business delivery and decision-making.

## 11. Business Requirements
**Definition**  
The business capabilities and rules the solution must satisfy to solve the approved problem.

**What belongs here**
- Outcome-focused requirements such as freshness expectations, trust requirements, exception visibility, and business-rule expectations.
- Statements that can later be translated into product and technical requirements.
- Business language tied to how stakeholders use the data.

**What does not belong here**
- Implementation syntax, code, schema definitions, or orchestration logic.
- UI wireframes.
- Engineering-only requirements without business meaning.

**Examples**
- "The business must be able to identify whether a daily inventory dataset contains all required supplier locations before using it for replenishment decisions."
- "Users must be able to view certified product availability metrics consistently across standard operational dashboards."

**Helpful context**  
This is where many teams accidentally insert SQL, mapping tables, or notebook logic. Stay at the level of business need: what must be true for users to trust and act on the data.

## 12. Success Criteria
**Definition**  
The conditions that indicate the business problem has been solved well enough to consider the initiative successful.

**What belongs here**
- Business outcomes, adoption signals, trust indicators, or SLA achievements.
- Measures that business and product stakeholders can validate.
- Criteria appropriate for go-live and post-launch review.

**What does not belong here**
- Purely technical unit-test completion.
- Individual developer tasks.
- Success statements that cannot be observed or measured.

**Examples**
- "Daily inventory data is available before planner cutoff time for 95 percent of business days in the first month after launch."
- "Operations and Finance both confirm that the certified in-stock metric matches the approved business definition in production dashboards."

**Helpful context**  
Success criteria should connect directly back to the business goals. If the criterion only proves that code ran, it belongs in the SRD or testing plan instead.

## 13. Approvals
**Definition**  
The formal signoff record showing who accepts the business problem statement, scope, and intended outcomes.

**What belongs here**
- Names, roles, dates, and approval status for the business owner and key approving stakeholders.
- Notes about conditional approval if needed.
- The minimum signoff required to move into product and technical design.

**What does not belong here**
- Detailed test signoff evidence.
- Engineering deployment approvals.
- Informal meeting notes.

**Examples**
- "Business Operations Director approves the business scope and success criteria on behalf of Inventory Operations."
- "Finance Data Governance Lead signs off on the certified margin metric definition before PRD finalization."

**Helpful context**  
For analytics work, approval should include the owner of the business truth, not just the project sponsor. That is often the difference between a technically complete delivery and an adopted one.
