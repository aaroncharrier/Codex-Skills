# Metric Definition Template

Use this template to document one metric in detail. It is intended for certified business metrics that need clear ownership, calculation logic, validation rules, and approval before they are published in a semantic layer or BI tool.

## Document Header

| Field | Value |
| --- | --- |
| Metric Name | Available to Sell Inventory |
| Metric Code / ID | `available_to_sell_qty` |
| Domain | Inventory |
| Business Owner | Inventory Operations |
| Technical Owner | BI / Data Engineering |
| Status | Draft / Under Review / Certified |
| Effective Date | 2026-05-02 |
| Related Documents | BRD, PRD, SRD, Metric Dictionary, Data Dictionary |

## 1. Business Purpose

| Attribute | Description |
| --- | --- |
| Business Objective | Show how much inventory is actually available for sale or allocation |
| Why It Matters | Supports replenishment, allocation, and inventory visibility decisions |
| Primary Consumers | Planners, merchandising, operations reporting |
| Decision Supported | Whether to replenish, reallocate, or hold inventory |

## 2. Business Definition

| Field | Value |
| --- | --- |
| Plain-English Definition | Inventory available after reserved stock has been excluded from on-hand quantity |
| Business Interpretation | A higher value indicates more immediately usable stock |
| Metric Type | Additive quantity metric |
| Reporting Grain | Item, location, business date |

## 3. Calculation Logic

| Field | Value |
| --- | --- |
| Formula | `on_hand_qty - reserved_qty` |
| Required Inputs | `on_hand_qty`, `reserved_qty` |
| Aggregation Rule | Sum across item/location rows unless business approves an alternate rollup |
| Rounding Rule | Whole number at report display level unless downstream reporting requires decimals |
| Null Handling | Null `reserved_qty` treated per approved business rule; document exact behavior |

## 4. Filters, Exclusions, and Scope

| Topic | Definition |
| --- | --- |
| Included Population | Active items in approved reporting locations |
| Excluded Population | Closed locations, discontinued items, test records |
| Time Scope | Daily published inventory snapshot |
| Regional / Business Scope | U.S. distribution centers in phase 1 |

## 5. Source Data and Dependencies

| Input / Dependency | Description |
| --- | --- |
| Source Dataset(s) | Curated inventory daily fact table |
| Upstream Dependencies | Item master, location mapping, supplier inventory feed, WMS feed |
| Semantic Layer Dependency | Certified metric object in MicroStrategy or governed BI layer |
| Refresh Cadence | Daily by 7:30 AM PT |

## 6. Edge Cases and Business Rules

| Scenario | Expected Handling |
| --- | --- |
| `reserved_qty` is null | Apply approved default rule and document whether null becomes `0` or blocks publication |
| Negative result | Flag for review or block publish if business rule does not allow negative available inventory |
| Late source feed | Apply freshness warning and handle per SLA / UAT agreement |
| Unmapped location or item | Reject from published metric until mapping is resolved |

## 7. Validation and Reconciliation

| Validation Check | Expected Result | Owner |
| --- | --- | --- |
| Manual sample calculation compared to published output | Published value matches approved sample calculation | BI Lead |
| Total available inventory compared to prior-day reasonableness threshold | Variance falls within approved threshold or is explained | Data Engineering |
| Item/location spot check with business users | Reported value matches business expectation for selected records | Inventory Operations |

## 8. Reporting and Consumption Notes

| Topic | Guidance |
| --- | --- |
| Display Name | Available to Sell Inventory |
| Display Format | Whole number |
| Report Usage | Operations dashboards, exception reporting, planning extracts |
| Labeling Requirement | Use the same business name in semantic layer, dashboard label, and glossary |
| Freshness Messaging | Show warning if source data misses SLA |

## 9. Approval and Certification

| Role | Name | Date | Status |
| --- | --- | --- | --- |
| Business Owner |  |  | Pending |
| BI / Semantic Layer Owner |  |  | Pending |
| Data Engineering Lead |  |  | Pending |

## 10. Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
