# Metric Dictionary Template

Use this template to document certified KPIs, calculations, and reporting measures. Replace the sample content with project-specific values.

## Document Header

| Field | Value |
| --- | --- |
| Metric Domain | Inventory |
| Metric Name | Available to Sell Inventory |
| Metric Owner | Inventory Operations |
| Technical Owner | BI / Data Engineering |
| Status | Draft / Certified |
| Effective Date | 2026-05-02 |
| Reporting Tools | MicroStrategy, curated semantic layer |
| Related Documents | BRD, PRD, SRD, Data Dictionary |

## Metric Summary

| Attribute | Description |
| --- | --- |
| Business Purpose | Measures inventory that can be allocated or sold after reserved stock is excluded |
| Metric Type | Additive quantity metric |
| Reporting Grain | Item, location, business date |
| Refresh Cadence | Daily |
| Primary Consumers | Planners, merchandising, operations reporting |

## Metric Definitions

| Metric Name | Business Definition | Formula / Logic | Inputs | Grain | Filters / Exclusions | Aggregation | Display Format | Owner | Certification Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `available_to_sell_qty` | Inventory available for sale or allocation | `on_hand_qty - reserved_qty` | `on_hand_qty`, `reserved_qty` | Item, location, business date | Exclude closed locations; treat null reserved quantity per approved rule | Sum | Whole number | Inventory Ops | Must match approved enterprise definition |
| `inventory_in_stock_pct` | Percent of active items with positive available quantity | `count(items with available_qty > 0) / count(active items)` | `available_qty`, active item flag | Location, business date | Exclude discontinued items | Average or ratio at reporting grain | Percent | Merchandising | Confirm denominator with business |
| `late_feed_flag` | Indicates daily inventory missed freshness SLA | `1 if publish_time > SLA else 0` | `publish_time`, SLA window | Dataset, business date | None | Max | Boolean / Yes-No | Data Engineering | Used for operational reporting |

## Validation Rules

| Metric Name | Validation Check | Expected Result | Owner |
| --- | --- | --- | --- |
| `available_to_sell_qty` | Compare sampled output to approved manual calculation | Matches within agreed tolerance | BI Lead |
| `inventory_in_stock_pct` | Reconcile numerator and denominator with source counts | Counts tie to approved filtered population | Product / Business Owner |

## Usage Notes

- Document the certified business meaning separately from the SQL implementation.
- Note whether a metric is additive, non-additive, or ratio-based.
- If filters materially change the result, make them explicit here rather than burying them in report logic.

## Change Log

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 0.1 | 2026-05-02 | Example | Initial template |
