# SRD Completion Questionnaire

Use this questionnaire to gather the inputs needed to draft a Software Requirements Document for a data analytics project. Answer at the system and engineering level. If an answer is unknown, write `TBD` and name the owner who will resolve it.

## Document Header
- System name:
- Engineering owner:
- Document owner:
- Version / status:
- Target design review date:
- Related BRD / PRD / diagrams:

## 1. System Purpose
1. What system or technical capability is being built or changed?
2. What business or product requirement does it support?
3. What is the boundary of this system versus adjacent systems?
4. What technical outcome must exist when implementation is complete?

## 2. System Scope
1. Which pipelines, tables, jobs, notebooks, APIs, semantic layer objects, or BI integrations are in scope?
2. Which environments are in scope: dev, test, prod?
3. What technical items are explicitly out of scope?
4. Is this a new build, an enhancement, or a replacement?

## 3. System Architecture Overview
1. What are the major components in the end-to-end flow?
2. Where will ingestion occur?
3. Where will transformation and curation occur?
4. What platform components are involved: Snowflake, Databricks, orchestration, storage, MicroStrategy?
5. Is there an architecture diagram or existing reference design?

## 4. Data Sources and Destinations
1. What are the upstream data sources?
2. What is the delivery method for each source: file, API, database, event stream?
3. What is the cadence and expected delivery window?
4. What are the downstream destinations?
5. Who owns each source and destination?

## 5. Data Model / Schema Notes
1. What is the target grain of the curated output?
2. What are the primary business keys and technical keys?
3. Which dimensions or conformed entities must be used?
4. Are there history, SCD, or snapshot requirements?
5. What schema decisions are already fixed versus still open?

## 6. Interface Requirements
1. What interface contracts must be supported?
2. What file formats, naming conventions, or API payload structures are required?
3. What authentication or connectivity method is required?
4. What downstream contract must remain stable for BI or consuming systems?
5. Is acknowledgment, checkpointing, or handshake logic required?

## 7. Ingestion / Transformation Logic
1. How should raw data be landed and standardized?
2. What mappings or enrichments are required?
3. What deduplication or idempotency rules apply?
4. What publish conditions must be met before curated output is released?
5. Are there ordered dependencies between jobs or datasets?

## 8. Validation and Data Quality Rules
1. What required fields must be non-null?
2. What schema, type, or format rules must be enforced?
3. What threshold checks must be applied: row count, null rate, duplicate rate, freshness?
4. Which failures are warnings versus hard stops?
5. What validation evidence must be stored?

## 9. Error Handling and Retry Behavior
1. What should happen when the source is unavailable?
2. What should happen when validation fails?
3. How many retries are allowed for transient failures?
4. Where should failed records or failed runs be logged?
5. How should reruns behave to avoid duplicates or corruption?

## 10. Security and Access Control
1. How will credentials and secrets be stored?
2. Which service accounts, roles, or groups need access?
3. What least-privilege restrictions apply?
4. Are any fields sensitive or restricted?
5. What audit or access logging is required?

## 11. Performance and Scalability Requirements
1. How quickly must the pipeline complete after source arrival?
2. What data volume is expected now?
3. What growth should the design support over 6 to 24 months?
4. Are there concurrency, cost, or compute constraints?
5. What performance threshold would be considered unacceptable?

## 12. Logging and Monitoring
1. What run metadata must be logged?
2. What alerts are required for failures, lateness, or abnormal data quality?
3. Who receives alerts?
4. What dashboards or monitoring views are required for support teams?
5. What information is needed to trace one bad number from source to report?

## 13. Creation of Runbook / Operational Playbook
1. What are the most likely failure scenarios for this system?
2. What first-step troubleshooting checks should responders perform for each major failure type?
3. When should the team retry automatically versus pause and investigate?
4. What actions should be taken if ingestion fails, for example check API, retry job, notify team?
5. Who owns first response, escalation, and final resolution for each failure class?
6. What contacts, support channels, or on-call paths must be documented in the playbook?

## 14. Non-Functional Requirements
1. What maintainability expectations exist?
2. Which configuration values should be externalized?
3. What deployment, rollback, or environment-separation rules apply?
4. What resilience or recoverability requirements exist?
5. What documentation or runbook content is required before go-live?

## 15. Release Plan / Deployment Plan
1. Which environments will be used: dev, test, UAT, prod?
2. What must be deployed in each environment: code, jobs, tables, views, semantic layer objects, reports?
3. What are the ordered deployment steps?
4. What approvals are required before production release?
5. What is the rollback plan if the release introduces bad data, failed jobs, or broken BI output?
6. When should the release occur, and are there blackout windows or business-calendar constraints?

## 16. UAT (User Acceptance Testing) Plan
1. Which business users or teams will perform UAT?
2. What real business scenarios must be tested?
3. What are the expected results for each scenario?
4. Which datasets, dashboards, reports, or metrics must be checked during UAT?
5. What defects would block signoff?
6. What sign-off criteria must be met before release approval?

## 17. Acceptance Criteria
1. What end-to-end technical scenario must pass before release?
2. What data quality checks must pass?
3. What security and access checks must pass?
4. What monitoring and alerting checks must pass?
5. What technical evidence is required for signoff?

## 18. Open Technical Issues
1. What source, schema, infrastructure, or tooling decisions are still unresolved?
2. What assumptions are currently being made in the design?
3. Which unresolved items could change implementation scope or timeline?
4. Who owns each technical issue, and what is the target resolution date?

## Final Check
1. Are any architecture or data-contract decisions still missing?
2. Which unresolved items block SRD completion?
3. Who owns each unresolved item, and by what date?
