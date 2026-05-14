# Project Classification Rules

## Primary Branches

### New Data Pipeline
Use when the main work is ingesting or loading new data into Databricks or another managed layer.

Signals:
- new source system
- new ingestion flow
- raw-to-curated movement
- new downstream dataset enablement

### Existing Pipeline Enhancement / Optimization
Use when the main work is changing an existing pipeline.

Signals:
- performance improvement
- cost reduction
- SLA improvement
- reliability improvement
- bug or defect remediation

### Snowflake Semantic Layer / Analytics Modeling
Use when the main work is building or changing views, curated models, grains, joins, dimensions, or metric-ready outputs for analytics consumption.

### MicroStrategy Reporting Development
Use when the main work is in reports, objects, dashboards, filters, drill paths, or KPI presentation.

### Multi-Domain Initiative
Use when multiple branches materially matter and no single branch clearly dominates.

## Confirmation Rule

After classification, ask:
`I classify this as [TYPE]. Confirm or correct?`

## Adjacent Scope Rule

After choosing a branch, still test for:
- source changes
- modeling changes
- reporting changes
- metric-definition gaps
- support implications
