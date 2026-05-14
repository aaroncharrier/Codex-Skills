# File Selection Rules

## Always Keep

- `docs/PROJECT_PLAN.md`
- `docs/OPEN_QUESTIONS_AND_DECISIONS_LOG.md`
- `docs/WORK_LOG.md`

## Data Document Bias by Project Type

### New Data Pipeline
Usually keep:
- `DATA_QUALITY_AND_RECONCILIATION_PLAN.md`
- `RUNBOOK_SUPPORT_TEMPLATE.md`

Keep when needed:
- `DATA_DICTIONARY_TEMPLATE.md`
- `DATA_MAPPING_DOCUMENT_TEMPLATE.md`

### Existing Pipeline Enhancement / Optimization
Keep DQ or runbook docs only when the change materially affects trust or support.

### Snowflake Semantic Layer / Analytics Modeling
Usually keep:
- `DATA_DICTIONARY_TEMPLATE.md`

Keep metric-definition docs only when governed metrics are materially in scope.

### MicroStrategy Reporting Development
Usually keep one metric-definition artifact if KPI definition clarity matters.

## Duration Rule

If expected duration is greater than 6 weeks:
- keep BRD / PRD / SRD templates and questionnaires

If expected duration is 6 weeks or less:
- delete the six BRD / PRD / SRD files via `scripts/cleanup_unused_docs.py`
