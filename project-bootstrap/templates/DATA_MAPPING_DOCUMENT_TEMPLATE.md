# Data Mapping Document Template

Use this template to map source fields to target fields for onboarding a new source, redesigning a pipeline, or publishing a curated dataset. Replace the sample content with project-specific values.

## Document Header

| Field | Value |
| --- | --- |
| Mapping Name | Supplier Inventory Feed to Curated Inventory Daily |
| Source System | Supplier SFTP feed |
| Target System | Snowflake curated table |
| Source Object | `supplier_inventory_YYYYMMDD.csv` |
| Target Object | `CURATED.INVENTORY_DAILY` |
| Owner | Data Engineering |
| Related Documents | BRD, SRD, Data Dictionary |
| Status | Draft / Approved |

## Mapping Scope

| Attribute | Description |
| --- | --- |
| Purpose | Standardize supplier inventory data for enterprise reporting |
| Source Cadence | Daily |
| Target Publish Cadence | Daily after validation |
| Key Matching Logic | Map supplier item code and warehouse code to enterprise dimensions |
| Major Assumptions | Supplier sends one complete file per business day |

## Field Mapping

| Source Field | Source Definition | Target Field | Target Definition | Transformation / Rule | Data Type Conversion | Default / Null Handling | Validation Rule | Example |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `supplier_item_code` | Supplier item identifier | `item_id` | Enterprise item identifier | Join to item cross-reference table | `STRING -> VARCHAR(50)` | Reject if no mapping exists | Must map to active item | `SUP-44501 -> SKU-100245` |
| `warehouse_code` | Supplier warehouse code | `location_id` | Enterprise location identifier | Join to location mapping table | `STRING -> VARCHAR(25)` | Reject if unmapped | Must map to approved reporting location | `ATL01 -> DC-ATL-01` |
| `snapshot_date` | File business date | `business_date` | Inventory business date | Cast to date using `YYYY-MM-DD` format | `STRING -> DATE` | Reject if invalid date | Must equal file control date | `2026-05-02` |
| `qty_on_hand` | Physical stock quantity | `on_hand_qty` | On hand inventory | Direct map after numeric cast | `STRING -> NUMBER(18,2)` | Reject if non-numeric or negative | Must be `>= 0` | `1540` |
| `qty_reserved` | Reserved quantity | `reserved_qty` | Reserved inventory | Direct map after numeric cast | `STRING -> NUMBER(18,2)` | Null handling per approved business rule | Must be `>= 0` when present | `210` |
| N/A | Not provided by source | `available_qty` | Available inventory | Derived as `on_hand_qty - reserved_qty` | Calculated field | If `reserved_qty` null, apply approved default rule | Must align to certified metric definition | `1330` |

## Rejected Record Handling

| Failure Type | Action | Logged To | Owner |
| --- | --- | --- | --- |
| Unmapped item | Reject row | Exception table / run log | Data Engineering |
| Invalid date format | Reject row | Exception table / run log | Data Engineering |
| Negative quantity | Reject row | Exception table / run log | Data Engineering + business review if source issue repeats |

## Sign-Off

| Role | Name | Date | Status |
| --- | --- | --- | --- |
| Business Data Owner |  |  | Pending |
| Data Engineering Lead |  |  | Pending |
| BI / Semantic Layer Owner |  |  | Pending |

## Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
