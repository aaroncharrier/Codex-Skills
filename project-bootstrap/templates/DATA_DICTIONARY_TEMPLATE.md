# Data Dictionary Template

Use this template to document datasets, tables, views, or files used in analytics delivery. Replace the sample content with project-specific values.

## Document Header

| Field | Value |
| --- | --- |
| Domain / Subject Area | Inventory |
| Dataset / Table Name | `CURATED.INVENTORY_DAILY` |
| Layer | Curated |
| Primary Owner | Data Engineering |
| Business Owner | Inventory Operations |
| Refresh Cadence | Daily by 7:30 AM PT |
| Source System(s) | Supplier feed, WMS |
| Related Documents | BRD, PRD, SRD, Mapping Doc |
| Status | Draft / Approved |

## Dataset Summary

| Attribute | Description |
| --- | --- |
| Business Purpose | Trusted daily inventory snapshot for reporting and replenishment decisions |
| Grain | One row per item, location, business date |
| Key Fields | `item_id`, `location_id`, `business_date` |
| Downstream Consumers | MicroStrategy dashboard, analyst dataset, planning extracts |
| Data Quality Notes | Publish only after required-field and row-count checks pass |

## Field Definitions

| Field Name | Business Name | Description | Data Type | Nullable | Example | Source / Logic | Business Rules | Sensitivity | Used In |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `item_id` | Item ID | Unique enterprise item identifier | `VARCHAR(50)` | No | `SKU-100245` | Source item code mapped to enterprise item master | Must match active item master record | Internal | Inventory metrics, reporting |
| `location_id` | Location ID | Warehouse or store location identifier | `VARCHAR(25)` | No | `DC-ATL-01` | Source warehouse code mapped to enterprise location | Must map to approved reporting location | Internal | Location reporting |
| `business_date` | Business Date | Date the inventory snapshot represents | `DATE` | No | `2026-05-02` | Derived from source file date or load date rule | One business date per published snapshot | Internal | Daily reporting |
| `on_hand_qty` | On Hand Quantity | Physical inventory currently on hand | `NUMBER(18,2)` | No | `1540` | Source quantity field | Must be non-negative | Internal | Available inventory calculations |
| `reserved_qty` | Reserved Quantity | Quantity already committed to orders or holds | `NUMBER(18,2)` | Yes | `210` | Source reservation field | Null treated as `0` only if approved by business rule | Internal | Available inventory calculations |
| `available_qty` | Available Quantity | Quantity available for sale or allocation | `NUMBER(18,2)` | No | `1330` | `on_hand_qty - reserved_qty` | Must align to certified metric logic | Internal | Certified dashboard metric |
| `load_ts` | Load Timestamp | Time the record was published to the curated layer | `TIMESTAMP_NTZ` | No | `2026-05-02 07:14:33` | System-generated | Required for auditability | Internal | Support and audit |

## Notes and Exceptions

- Document derived fields explicitly; do not assume the column name explains the logic.
- Call out any null-handling, defaulting, rounding, or late-arriving-data rules.
- If one field changes meaning between raw and curated layers, document both definitions separately.

## Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
