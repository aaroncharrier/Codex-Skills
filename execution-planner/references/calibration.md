# Execution Planner Calibration

Use these examples to calibrate step quality, traceability, and scope control. Do not copy them into the final answer unless the request actually matches them.

## Good Step Granularity

Good:
- `Load and validate source data`
- `Prepare complete monthly periods`
- `Aggregate revenue by customer and month`
- `Format the final output structure`

Why these work:
- each step is actionable
- each step advances the work materially
- each step stays above implementation detail

Poor:
- `Write SQL query`
- `Join orders to customers with LEFT JOIN`
- `Optimize performance`

Why these fail:
- they are too vague, too implementation-specific, or not grounded in the specification

## Ordering Example

Given:
- input data contains transactions
- output requires monthly customer revenue
- constraint requires months with no revenue to appear

Expected ordering:
1. validate required inputs and fields
2. prepare the monthly period structure
3. calculate record-level revenue
4. aggregate by customer and month
5. account for missing periods
6. format and validate output

Why this works:
- it follows dependency order
- it reflects the zero-period constraint
- it ends with output structuring and validation

## Traceability Example

Given:
- output requires CSV export
- constraint requires stable column order
- decision fixes month as the reporting grain

Expected behavior:
- include a step to structure the output for CSV delivery
- include a step that reflects the monthly reporting grain
- include a validation step that checks column order
- do not add unrelated steps such as dashboard publishing

## Scope Control Example

Bad behavior:
- specifying a calendar table strategy
- naming a database engine
- recommending performance tuning
- inventing a fallback export format

Good behavior:
- stay at the planning level
- preserve the specification exactly
- describe what must happen, not how it is implemented in a specific tool
