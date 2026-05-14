# Runbook and Support Template

Use this template to document how a data analytics product is monitored, supported, recovered, and communicated during normal operations and incidents. Complete it before go-live for any pipeline, curated dataset, semantic layer object, or dashboard with production support expectations.

## Document Header

| Field | Value |
| --- | --- |
| Service / Data Product Name | Daily Inventory Curated Publish |
| Service Owner | Data Engineering |
| Business Owner | Inventory Operations |
| Primary Support Team | Data Platform Support |
| Severity Matrix Version | v1 |
| Status | Draft / Approved |
| Effective Date | 2026-05-02 |
| Related Documents | SRD, Data Quality Plan, Release Plan, Architecture Diagram |

## 1. Service Overview

| Attribute | Description |
| --- | --- |
| Business Purpose | Publish trusted daily inventory data for downstream reporting and replenishment decisions |
| Supported Scope | Raw ingestion, validation, curated publish, semantic layer refresh, dashboard availability |
| In-Scope Environments | Test, UAT, Prod |
| Out of Scope | Feature backlog, upstream source redesign, one-time historical analysis support |
| Business Criticality | High during weekday morning publish window |

## 2. Support Model and Ownership

| Role | Team / Owner | Responsibilities | Support Window |
| --- | --- | --- | --- |
| Service Owner | Data Engineering Lead | Technical ownership, remediation approval, backfill decisions | Business hours plus on-call for Sev 1 |
| First Responder | Data Platform Support | Triage alerts, confirm impact, execute first checks | 6:00 AM to 6:00 PM PT |
| Business Contact | Inventory Operations | Confirm business impact and approve fallback use of stale data | Business hours |
| BI / Semantic Layer Owner | BI Platform Team | Validate downstream model and dashboard behavior | Business hours |

## 3. System and Dependency Summary

| Dependency Type | Name | Purpose | Owner | Failure Impact |
| --- | --- | --- | --- | --- |
| Upstream Source | Supplier inventory feed | Daily inventory source | Supplier / Source Owner | No curated publish if file missing or invalid |
| Platform | Snowflake curated schema | Stores published reporting data | Data Engineering | Dataset unavailable or incomplete |
| Orchestration | Scheduled workflow | Runs ingestion, validation, publish sequence | Data Platform | Job failure or late data |
| Downstream Consumer | MicroStrategy inventory dashboard | Consumes curated dataset | BI Team | Users see stale or missing data |

## 4. Normal Operating Expectations

| Topic | Expectation |
| --- | --- |
| Standard Run Window | Daily on business days after source arrival |
| Publish SLA | Curated dataset available by 7:30 AM PT |
| Alerting Threshold | Alert if source missing after 5:45 AM PT or publish incomplete after 7:15 AM PT |
| Data Freshness Messaging | Dashboard shows warning if current business date data is not published |
| Retention of Logs and Evidence | Keep operational logs, validation output, and reconciliation evidence per team standard |

## 5. Monitoring and Alerting

| Monitor | Condition | Severity | Notification Channel | Owner |
| --- | --- | --- | --- | --- |
| Source arrival monitor | Expected file not received by SLA threshold | Sev 2 | Teams / email / pager | Data Platform Support |
| Pipeline job monitor | Workflow run fails or exceeds runtime threshold | Sev 2 | Teams / email / pager | Data Platform Support |
| Data quality monitor | Required validation rule fails | Sev 2 or Sev 1 depending on impact | Teams / email | Data Engineering |
| Dashboard freshness monitor | Dashboard serves stale data beyond agreed tolerance | Sev 3 or Sev 2 depending on audience | Teams / email | BI Platform Team |

## 6. Incident Severity and Response Targets

| Severity | Definition | Example | Response Target | Update Cadence |
| --- | --- | --- | --- | --- |
| Sev 1 | Critical business-impacting outage with no approved workaround | Daily executive dashboard cannot publish before business cutoff | 15 minutes | Every 30 minutes |
| Sev 2 | Major degradation or delay with limited workaround | Curated publish delayed but users can temporarily use prior-day data with approval | 30 minutes | Hourly |
| Sev 3 | Minor defect or non-blocking issue | One alert is noisy but data is correct | Same business day | As needed |

## 7. Standard Operating Procedures

| Scenario | First Checks | Likely Causes | Immediate Actions | Escalate To |
| --- | --- | --- | --- | --- |
| Source file missing | Check source landing location, file manifest, upstream notification | Late source delivery, transport issue, naming mismatch | Confirm absence, notify source owner, decide whether to wait or use fallback | Service Owner + Source Owner |
| Validation failure | Review failed rules, sample rejected rows, recent schema changes | Schema drift, bad source values, mapping gaps | Pause publish if required, capture evidence, notify business owner if SLA risk exists | Service Owner |
| Curated publish failed | Check orchestrator run logs and warehouse errors | Permission issue, compute failure, SQL error | Retry if safe, otherwise hold publish and investigate root cause | Data Engineering Lead |
| Dashboard stale after publish | Check downstream semantic layer refresh and dashboard cache | Refresh failure, dependency lag, filter issue | Trigger downstream refresh and verify business-date view | BI Platform Team |

## 8. Retry, Rerun, and Recovery Guidance

| Topic | Guidance |
| --- | --- |
| Automatic Retry | Allowed only for transient platform or network failures with no duplicate-publish risk |
| Manual Rerun Rule | Confirm idempotency, partition scope, and downstream communication before rerun |
| Backfill Rule | Use approved backfill process if missed data affects certified reporting |
| Duplicate Prevention | Validate business date, partition keys, and control totals before republish |
| Recovery Evidence | Record run ID, timestamps, operator, issue summary, and validation results after recovery |

## 9. Business Communication and Escalation

| Trigger | Audience | Message Content | Channel | Owner |
| --- | --- | --- | --- | --- |
| SLA at risk | Business owner, BI owner, support lead | Expected delay, affected outputs, next update time | Teams / email | First Responder |
| Publish blocked | Broader stakeholder list | Impacted datasets, decision on stale data, target recovery plan | Teams / email | Service Owner |
| Root cause confirmed | Stakeholders and leadership as needed | Cause, fix, recovery status, prevention action | Teams / email / incident summary | Service Owner |

## 10. Access, Tools, and Reference Links

| Item | Purpose | Owner / Access Path |
| --- | --- | --- |
| Orchestrator run history | Review workflow execution | Platform support access |
| Warehouse query history | Investigate failed SQL or load behavior | Data engineering access |
| Validation output location | Review failed checks and reconciliation results | Data quality support path |
| Support channel | Coordinate incident response | Team support chat / ticket queue |

## 11. Post-Incident Review Requirements

| Topic | Requirement |
| --- | --- |
| Sev 1 and Sev 2 Review | Required within agreed timeline after incident closure |
| Evidence to Capture | Timeline, cause, impact, recovery steps, preventive actions |
| Ownership | Service owner coordinates with platform and business teams |
| Closure Condition | Action items logged and owners assigned |

## 12. Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
