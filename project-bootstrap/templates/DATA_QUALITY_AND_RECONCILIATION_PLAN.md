# Data Quality and Reconciliation Plan Template

Use this template to define how a data analytics project will validate, reconcile, evidence, and govern data quality before publication and after release. Use it for new source onboarding, curated dataset delivery, metric certification, or major reporting changes where trust and completeness matter.

## Document Header

| Field | Value |
| --- | --- |
| Plan Name | Inventory Daily Publish Data Quality and Reconciliation Plan |
| Domain | Inventory |
| Primary Owner | Data Engineering |
| Business Owner | Inventory Operations |
| Status | Draft / Under Review / Approved |
| Effective Date | 2026-05-02 |
| Related Documents | SRD, Data Dictionary, Mapping Document, Metric Definition, Runbook |

## 1. Objective and Scope

| Attribute | Description |
| --- | --- |
| Objective | Define the controls required to ensure the published dataset is complete, accurate, timely, and fit for business use |
| In-Scope Data Products | Curated inventory daily table, certified availability metric, downstream dashboard extracts |
| In-Scope Lifecycle Points | Source arrival, raw landing, standardization, transformation, publish, downstream consumption |
| Out of Scope | Exploratory analysis datasets, ad hoc analyst spreadsheets, unrelated source systems |
| Review Cadence | Review before go-live and after material source or logic changes |

## 2. Quality Goals and Service Expectations

| Quality Dimension | Target / Expectation | Notes |
| --- | --- | --- |
| Completeness | Required records and fields present for all approved scope | Missing approved locations trigger investigation or block publish |
| Accuracy | Published values match approved transformation and metric logic | Sample and aggregate reconciliations required |
| Timeliness | Dataset published by agreed freshness SLA | Late data behavior must be documented |
| Consistency | Same business definitions used across dataset, metric layer, and reporting | Certified metrics must not diverge across tools |
| Uniqueness | No duplicate business-key rows at published grain | Duplicate threshold normally equals zero unless approved otherwise |

## 3. Data Products and Critical Elements

| Data Product | Grain | Critical Fields / Metrics | Business Use | Owner |
| --- | --- | --- | --- | --- |
| `CURATED.INVENTORY_DAILY` | Item, location, business date | `item_id`, `location_id`, `business_date`, `on_hand_qty`, `available_qty` | Daily inventory reporting | Data Engineering |
| `available_to_sell_qty` | Item, location, business date and rollups | `available_qty` metric output | Planning and replenishment decisions | Inventory Operations |

## 4. Control Framework by Lifecycle Stage

| Stage | Control Objective | Example Checks | Failure Type |
| --- | --- | --- | --- |
| Source receipt | Confirm expected files or data extracts arrived on time and in expected format | File presence, naming convention, control date, record count present | Warning or hard stop depending on SLA |
| Raw landing | Confirm source was landed without truncation or corruption | Row count, checksum if available, schema presence | Hard stop |
| Standardization | Confirm typing, parsing, and base conformance | Data type casting, mandatory fields, reference format checks | Hard stop for critical fields |
| Transformation | Confirm business rules and joins behave as expected | Mapping coverage, duplicates, filtered populations, derived field logic | Warning or hard stop depending on impact |
| Publish | Confirm curated output is safe for downstream use | Final row count, partition completeness, reconciliation totals, freshness date | Hard stop if certified output untrusted |
| Downstream verification | Confirm report and semantic layer reflect approved dataset state | Business-date check, metric spot checks, dashboard freshness | Warning or hard stop depending on audience |

## 5. Validation Rules

| Rule ID | Rule Description | Level | Threshold / Expected Result | Action on Failure | Owner |
| --- | --- | --- | --- | --- | --- |
| DQ-001 | Required business keys must be non-null | Row | Zero nulls for `item_id`, `location_id`, `business_date` | Block publish | Data Engineering |
| DQ-002 | Published grain must be unique by item, location, and business date | Dataset | Zero duplicate keys | Block publish | Data Engineering |
| DQ-003 | Mapping coverage for source items must meet approved threshold | Dataset | At least 98 percent mapped rows unless approved exception exists | Block publish or escalate | Data Steward |
| DQ-004 | Quantities must be numeric and non-negative where required | Row | No invalid numeric values; no negative values unless business rule allows | Reject row or block publish | Data Engineering |
| DQ-005 | Current business-date row count must fall within reasonableness threshold | Aggregate | Within agreed variance or explicitly explained | Investigate and approve before publish | Data Engineering + Business Owner |
| DQ-006 | Certified metric totals must reconcile to approved source or manual control totals | Aggregate | Matches within approved tolerance | Block publish if unexplained | BI / Data Engineering |

## 6. Reconciliation Approach

| Reconciliation Type | Compared Between | Purpose | Frequency | Owner |
| --- | --- | --- | --- | --- |
| Source to raw | Source control totals versus landed raw totals | Confirm ingestion completeness | Every run | Data Engineering |
| Raw to curated | Raw standardized totals versus curated totals by business date and key dimensions | Confirm transformation did not lose or distort data unexpectedly | Every run | Data Engineering |
| Curated to semantic layer | Curated dataset totals versus semantic layer or BI object totals | Confirm downstream refresh aligns to published data | Every run or every publish cycle | BI Platform Team |
| Curated to business expectation | Published totals versus approved business reasonableness checks | Confirm output is believable and usable | Daily or per release | Business Owner |

## 7. Thresholds, Tolerances, and Approval Rules

| Topic | Rule |
| --- | --- |
| Null Threshold | Critical business keys allow zero nulls |
| Duplicate Threshold | Published grain allows zero duplicates unless explicitly approved |
| Variance Tolerance | Any aggregate variance above agreed threshold requires documented explanation and approval |
| Late Data Rule | If freshness SLA is missed, follow documented stale-data or blocked-publish decision |
| Override Authority | Name the role allowed to approve conditional publication with known issue |

## 8. Exception Handling and Evidence

| Topic | Guidance |
| --- | --- |
| Failed Record Handling | Define whether bad rows are rejected, quarantined, defaulted, or corrected upstream |
| Publish Decision | Document which failures are warnings versus hard stops |
| Evidence Storage | Store validation output, reconciliation totals, timestamps, and approver comments in an agreed location |
| Auditability | Ensure one reviewer can trace a reported issue from source through published output |
| Notification | Notify support and business stakeholders when quality issues threaten SLA or trust |

## 9. Roles and Review Cadence

| Role | Responsibilities | Review Cadence |
| --- | --- | --- |
| Data Engineering | Implement checks, review failures, maintain evidence | Every run and after logic changes |
| Data Steward / Business SME | Confirm mappings, review quality exceptions, validate reasonableness | Weekly during stabilization, then as needed |
| BI / Semantic Layer Owner | Confirm downstream metric and dashboard alignment | Each release and major refresh change |
| Business Owner | Approve tolerance, override policy, and conditional publish decisions | Before go-live and during critical incidents |

## 10. Test and Sign-Off Evidence

| Evidence Type | Description | Owner |
| --- | --- | --- |
| Sample row validation | Business-reviewed sample records match expected results | Data Engineering + Business SME |
| Aggregate reconciliation | Control totals tie across lifecycle checkpoints | Data Engineering |
| Failure scenario validation | Alerts and blocked-publish behavior work as designed | Support / Data Platform |
| UAT confirmation | Business confirms outputs are trustworthy for decision-making | Product or Business Owner |

## 11. Open Issues and Follow-Ups

| Item ID | Issue or Follow-Up | Impact | Owner | Target Date | Status |
| --- | --- | --- | --- | --- | --- |
| QA-001 | Finalize approved row-count variance threshold by business date | Publish decision logic cannot be finalized | Business Owner | 2026-05-08 | Open |
| QA-002 | Confirm where reconciliation evidence will be retained for support and audit use | Support model remains incomplete | Data Engineering Lead | 2026-05-06 | Open |

## 12. Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
