# PRD Completion Questionnaire

Use this questionnaire to gather the inputs needed to draft a Product Requirements Document for a data analytics project. Answer from the user and consumer perspective. If an answer is unknown, write `TBD` and name the owner who will resolve it.

## Document Header
- Product or capability name:
- Product owner:
- Document owner:
- Version / status:
- Target release or review date:
- Related BRD or supporting links:

## 1. Product Overview
1. What is the product, capability, dataset, dashboard, or governed metric being delivered?
2. Who will use it?
3. What business workflow or decision does it support?
4. What will users receive that they do not have today?

## 2. Problem Statement
1. What user problem does this product solve?
2. What is frustrating, slow, confusing, or untrusted in the current experience?
3. What happens when users do not have this capability?
4. Which user group feels the problem most directly?

## 3. Goals and Non-Goals
1. What are the primary product goals for this release?
2. What user outcomes should improve if the product works well?
3. What is explicitly not part of this release?
4. If time is limited, what is the minimum acceptable product outcome?

## 4. Personas / Users
1. Who are the primary users?
2. Who are the secondary users or downstream consumers?
3. What decision does each user type make with this product?
4. What level of detail does each user need: summary, operational detail, exception review, self-service analysis?

## 5. User Stories or User Needs
1. What does each user need to see, do, or trust?
2. What timing matters to the user: daily, hourly, monthly close, near real-time?
3. What exceptions or warning states must be visible?
4. What actions should users take after consuming the output?

## 6. Functional Requirements
1. What must the product do for users?
2. What data or metrics must be visible?
3. What filters, drill paths, or segmentation are required?
4. What business rules must the product apply or reflect?
5. What user-visible behavior should occur when source data is late, incomplete, or invalid?

## 7. Non-Functional Requirements
1. What freshness SLA must users experience?
2. What availability expectation exists for the product?
3. What level of trust, auditability, or certification is required?
4. Are there usability or discoverability expectations for metric definitions, labels, or glossary content?

## 8. SLA / Data Contract
1. What freshness SLA is expected for the dataset, metric, or report?
2. What exact delivery time is required, for example `CRM data delivered daily by 6:00 AM Pacific`?
3. Which team owns upstream delivery, and which team owns downstream product support?
4. What schema stability is required for this release?
5. How should teams communicate breaking schema changes, delays, or missing data?
6. What should users expect when the data contract is missed: warning, delayed publish, stale data banner, blocked release, escalation?

## 9. Reporting / Metrics Requirements
1. Which dashboards, semantic layer objects, or reports are in scope?
2. Which certified metrics must be created or updated?
3. What exact business definition is expected for each key metric?
4. Which dimensions, grains, or cuts must users analyze by?
5. Are there required naming standards, formatting rules, or metric descriptions?

## 10. UX / Consumption Considerations
1. How should users discover and understand the output?
2. What labels, glossary text, or freshness warnings are needed?
3. Should stale or partial data be shown, hidden, or flagged?
4. What confusion or misuse is most likely if the product is poorly labeled?

## 11. Scope and Release Phases
1. What is included in phase 1?
2. What is deferred to later phases?
3. Are any user groups, regions, or data domains excluded from the initial release?
4. What dependency controls whether a later phase can start?

## 12. Success Metrics
1. How will product success be measured after launch?
2. What adoption target exists: usage, reduction in manual work, reduction in disputes, faster decisions?
3. What freshness or reliability target should be monitored?
4. What qualitative feedback would indicate the product is working well?

## 13. Open Questions
1. What user or product decisions are still unresolved?
2. What could change scope, acceptance criteria, or release timing?
3. Which questions require business governance or stakeholder alignment?
4. Who owns resolving each open question?

## 14. Acceptance Criteria
1. What must a user be able to do successfully before the product is accepted?
2. What must users be able to see or validate in the dashboard, dataset, or semantic layer?
3. How should the product behave in failure or exception scenarios?
4. What conditions must be true for the product owner to approve release?

## Final Check
1. Are any critical user needs still unclear?
2. Which open items block PRD completion?
3. Who owns each unresolved item, and by what date?
