# Product Requirements Document (PRD) Template for Data Analytics Projects

Use this template for larger projects when product behavior, user needs, release scope, and acceptance criteria need their own working document.

Shared terms used in this template:

- `source onboarding`: Bringing a new file, API, database, or partner feed into the analytics platform.
- `certified metric`: A business-approved definition for a KPI, measure, or calculation used across reporting.
- `semantic layer`: The reporting-friendly layer that presents business names, definitions, and governed logic.
- `consumer-facing dataset`: A curated table, view, or model intended for reporting or analyst consumption.
- `freshness SLA`: The expected time by which data must be available for business use.

Suggested document header:

- Product or Capability Name:
- Product Owner:
- Document Owner:
- Version:
- Status:
- Date:
- Related BRD / Links:

## 1. Product Overview
**Definition**  
A concise description of the analytics product, capability, or reporting experience being delivered for users.

**What belongs here**
- What the product is from the user's perspective.
- The main workflow or decision it supports.
- How it relates to the business problem described in the BRD.

**What does not belong here**
- Detailed business sponsorship language that belongs in the BRD.
- System architecture or storage-layer details.
- Team task breakdowns.

**Examples**
- "This capability provides planners with a daily governed inventory dataset and dashboard view that includes partner-managed warehouse stock."
- "This product introduces a certified gross margin metric in the semantic layer so analysts and executives use one calculation across reports."

**Helpful context**  
For analytics, the "product" may be a dataset, dashboard, semantic layer capability, or governed metric experience. Describe the usable thing, not the implementation stack.

## 2. Problem Statement
**Definition**  
A user-centered explanation of the problem the product must solve.

**What belongs here**
- The pain users experience today.
- The consequences for decision-making, trust, or efficiency.
- The gap between current and desired product behavior.

**What does not belong here**
- High-level business funding rationale already captured in the BRD.
- Raw implementation notes.
- Technical constraints without user impact.

**Examples**
- "Planners cannot see supplier-managed stock in the standard dashboard, so they make replenishment decisions with incomplete inventory coverage."
- "Analysts spend time reconciling multiple versions of the same margin metric because no certified definition is exposed in the reporting layer."

**Helpful context**  
The BRD says why the business cares. The PRD says what is broken for the people using the analytics capability day to day.

## 3. Goals and Non-Goals
**Definition**  
The product outcomes the team is targeting and the outcomes it is intentionally not targeting in this release.

**What belongs here**
- Clear product goals tied to user benefit and behavior.
- Explicit non-goals that narrow release expectations.
- Priority if multiple goals exist.

**What does not belong here**
- Technical implementation choices.
- Pure business strategy language with no product implication.
- Open questions presented as goals.

**Examples**
- Goal: "Allow operations users to see validated supplier inventory in the daily dashboard without manual file combination."
- Non-goal: "Replace the existing MicroStrategy dashboard with a new reporting tool during this release."

**Helpful context**  
Analytics teams often over-pack releases. Non-goals help preserve focus when stakeholders assume a new metric or source should also trigger broad report redesign.

## 4. Personas / Users
**Definition**  
The user groups who will consume, interpret, or operationally depend on the analytics capability.

**What belongs here**
- Primary and secondary user groups.
- Their goals, decisions, and context of use.
- Differences in need across roles where relevant.

**What does not belong here**
- Organizational charts.
- Engineering service accounts or system actors best handled in SRD.
- Excessive demographic persona detail irrelevant to analytics consumption.

**Examples**
- "Inventory Planner: needs fresh, location-level stock visibility before placing orders."
- "BI Analyst: needs a certified metric exposed consistently in the semantic layer for self-service reporting."

**Helpful context**  
In analytics work, personas are often role-based rather than consumer-marketing personas. Focus on decisions, trust needs, and how each user interprets the data.

## 5. User Stories or User Needs
**Definition**  
Structured statements of what users need to do, know, or trust when using the product.

**What belongs here**
- User stories, job stories, or direct user-need statements.
- The action, outcome, and why it matters.
- Needs related to consumption, trust, discoverability, and exception visibility.

**What does not belong here**
- Database implementation logic.
- Broad business requirements with no user action.
- Vague statements like "users need good data."

**Examples**
- "As an inventory planner, I need supplier stock loaded before the morning planning window so I can make replenishment decisions using complete inventory coverage."
- "As a BI analyst, I need the certified available-to-sell metric defined once in the semantic layer so my dashboard matches enterprise reporting."

**Helpful context**  
This section is where analytics teams clarify whether the real need is raw data access, a governed metric, a dashboard behavior, or an exception workflow.

## 6. Functional Requirements
**Definition**  
The product behaviors and capabilities users or downstream consumers must experience.

**What belongs here**
- What the product must do, show, calculate, or expose.
- User-visible behaviors such as filtering, exception surfacing, metric availability, or reporting publication.
- Product rules stated in business or product language.

**What does not belong here**
- SQL statements, notebook steps, or ETL pseudocode.
- Infrastructure sizing.
- Pure process tasks such as "hold stakeholder meeting."

**Examples**
- "The product must publish a daily governed inventory dataset that includes internal and supplier-managed stock by location and item."
- "The product must flag when a certified metric cannot be calculated because required source fields are missing."

**Helpful context**  
A good analytics functional requirement describes what a user or downstream BI object can rely on. Save exact transformation mechanics for the SRD.

## 7. Non-Functional Requirements
**Definition**  
The quality attributes the product must meet for users to trust and successfully use it.

**What belongs here**
- Freshness, availability, usability, auditability, accessibility of metadata, and reliability expectations.
- Product-level service expectations as users experience them.
- Any consumer-facing governance requirement.

**What does not belong here**
- Detailed platform tuning settings.
- Engineering-only performance notes disconnected from the user experience.
- Security implementation specifics better placed in the SRD.

**Examples**
- "The dashboard-ready inventory dataset must be available by 7:30 AM Pacific on business days."
- "Certified metric definitions must be traceable to approved business logic and visible to reporting consumers."

**Helpful context**  
For analytics products, non-functional requirements are often what makes the output usable: freshness, trust, consistency, and explainability.

## 8. SLA / Data Contract
**Definition**  
The explicit operating expectations between teams for delivering, maintaining, and supporting the analytics product or dataset.

**What belongs here**
- Freshness SLA or required delivery time for data, metrics, or reports.
- Schema stability expectations, including how breaking changes are handled.
- Ownership for source delivery, product support, and issue resolution.
- Failure expectations, such as what happens when data is late, missing, incomplete, or structurally changed.

**What does not belong here**
- Low-level orchestration or deployment mechanics that belong in the SRD.
- General business goals with no operational expectation attached.
- Vague statements such as "data should arrive on time" without timing, owner, or consequence.

**Examples**
- "CRM data must be delivered daily by 6:00 AM Pacific so downstream sales dashboards can publish before the morning business review."
- "Source schema changes that add, remove, or rename required fields must be communicated to the product and engineering owners at least five business days before release."

**Helpful context**  
This section is underrated because it prevents avoidable disputes later. In analytics work, users often assume freshness, stability, and support expectations are understood when they are not. Write the contract explicitly.

## 9. Reporting / Metrics Requirements
**Definition**  
Requirements specific to dashboards, semantic layers, certified KPIs, and analytic outputs.

**What belongs here**
- Metric definitions, report behaviors, dimensional cuts, aggregation expectations, and governance needs.
- Requirements for how metrics are exposed to MicroStrategy or another BI layer.
- Rules for metric naming, certification, and interpretation.

**What does not belong here**
- Full technical schema design.
- Implementation SQL for calculated fields.
- General business goals with no reporting implication.

**Examples**
- "Available-to-sell inventory must be exposed as a certified metric using the approved formula and standard business naming."
- "The daily operations dashboard must support filtering by distribution center, supplier, item category, and reporting date."

**Helpful context**  
This section matters because many analytics projects are really metric-definition projects in disguise. Separate what users need to see from how engineering will compute it.

## 10. UX / Consumption Considerations
**Definition**  
Guidance on how users find, interpret, and consume the analytics output.

**What belongs here**
- Navigation, discoverability, labeling, glossary needs, warning states, and explanatory content for consumers.
- Expectations for consistent naming and interpretation across dashboards or datasets.
- User-facing handling of late or incomplete data.

**What does not belong here**
- Pixel-perfect design specifications unless the project truly requires them.
- Backend error processing logic.
- Deep BI object configuration details with no user-facing implication.

**Examples**
- "If the supplier feed is late, the dashboard should display a clear freshness warning instead of silently showing stale values."
- "Certified metrics should use the same business labels in the semantic layer, report headers, and glossary documentation."

**Helpful context**  
Analytics UX is not just colors and layout. It includes whether users can understand freshness, trust the labels, and recognize exceptions before acting on the data.

## 11. Scope and Release Phases
**Definition**  
The product capabilities included in the current release and how later phases are separated.

**What belongs here**
- Release sequencing, phased rollouts, and what each phase delivers to users.
- Any rollout constraints by user group, region, or data domain.
- Dependencies that affect feature availability by phase.

**What does not belong here**
- Detailed sprint plans.
- Infrastructure deployment scripts.
- General business scope already documented in the BRD without product-specific release detail.

**Examples**
- "Phase 1 exposes the governed dataset and one operations dashboard; Phase 2 adds exception trend reporting and self-service analyst views."
- "Initial release covers U.S. distribution centers only; international supplier inventory is deferred pending source readiness."

**Helpful context**  
Phasing is common in analytics because source readiness, governance, and BI publishing often mature at different speeds. Make those release boundaries explicit.

## 12. Success Metrics
**Definition**  
The measurable indicators that show whether the product is delivering value to its users.

**What belongs here**
- Adoption, usage, accuracy perception, reduction in manual work, SLA performance, or issue-rate metrics.
- Metrics aligned to the product goals.
- Definitions for how success will be observed.

**What does not belong here**
- Internal engineering task completion.
- Undefined aspirations such as "users like it."
- Technical monitoring metrics that users never experience unless they directly support product success.

**Examples**
- "Reduce manual inventory reconciliation time for planners by at least 50 percent within one month of launch."
- "Achieve 95 percent on-time publication of the certified daily inventory dataset during the first 30 production days."

**Helpful context**  
PRD success metrics often bridge business and technical measures. Choose the metrics that best prove improved user outcomes, not just healthy pipelines.

## 13. Open Questions
**Definition**  
Known unresolved product decisions that need closure before build completion or release.

**What belongs here**
- Questions about user behavior, release scope, governance decisions, or reporting expectations.
- Items that could change product design or acceptance criteria.
- Ownership for resolving the question when possible.

**What does not belong here**
- Hidden requirements that should already be defined.
- Technical implementation details better managed as SRD issues.
- General brainstorming with no decision impact.

**Examples**
- "Do planners need same-day intraday refresh for supplier inventory, or is one daily update sufficient for phase 1?"
- "Should the certified metric be released first to analyst users before it appears in executive dashboards?"

**Helpful context**  
Analytics work often has unresolved questions around freshness expectations, dimensional grain, and exception visibility. Capture them before they become late-breaking change requests.

## 14. Acceptance Criteria
**Definition**  
The product-level conditions that must be true for stakeholders to accept the delivered capability.

**What belongs here**
- Observable statements that can be validated through demos, UAT, or controlled checks.
- Criteria tied to the product behaviors and goals.
- User-facing data trust, reporting, and metric expectations.

**What does not belong here**
- Implementation-only checklists.
- Vague approval statements without testable meaning.
- Low-level platform verification steps with no product impact.

**Examples**
- "Users can view supplier and internal inventory together in the standard dashboard using the approved certified metric definitions."
- "If required source data is missing, consumers see a clear exception state rather than silently receiving incomplete totals."

**Helpful context**  
Acceptance criteria should allow a business or product stakeholder to say yes or no. If only an engineer can understand the criterion, it likely belongs in the SRD.
