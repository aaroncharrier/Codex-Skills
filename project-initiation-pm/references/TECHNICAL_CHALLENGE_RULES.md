# Technical Challenge Rules

The skill should not merely document. It should challenge and recommend.

## Common Challenge Areas

### Full Reload vs Incremental
Challenge when full reload is proposed without a clear reason.

Ask:
- Why full reload instead of incremental?
- What are the volume, cost, and runtime implications?
- How will reruns and recoverability work?

Recommend considering:
- incremental loading
- idempotent processing
- watermark or CDC strategy

### Missing Data Quality Controls
Challenge when no DQ plan exists.

Ask:
- How will freshness, completeness, and duplicate issues be detected?
- What stops bad data from reaching consumers?

Recommend considering:
- row-count checks
- freshness checks
- null and duplicate rules
- reconciliation checks
- publish gates

### Weak Operational Design
Challenge when retry, alerting, or support is vague.

Ask:
- What happens if the source is late or unavailable?
- How will failures be detected?
- Who responds first?

Recommend considering:
- retry behavior
- logged run metadata
- alert routing
- runbook ownership

### Unclear Ownership
Challenge when owners are not identified.

Ask:
- Who owns the source?
- Who approves business definitions?
- Who supports the output after release?

Record unknown ownership as `TBD`.

## Tone Rule

Be firm, practical, and educational.
Avoid process bloat.
