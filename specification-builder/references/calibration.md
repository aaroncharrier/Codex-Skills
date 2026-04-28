# Specification Builder Calibration

Use these examples to calibrate strictness, normalization, and scope control. Do not copy the examples into the final answer unless the request actually describes the same content.

## Normalization Example

Input concepts:
- `customer id`
- `customer_id`
- `Customer ID`

Expected behavior:
- normalize to one form such as `customer_id`
- keep a single concept in the final output

## Assumption Trimming Example

Given assumptions:
- source table exists
- user has a computer
- source table contains `price`
- price should probably be positive

Expected behavior:
- keep only assumptions that still matter and are grounded in the handoff
- remove trivial assumptions such as `user has a computer`
- remove speculative assumptions such as `price should probably be positive` unless explicitly supported

## Consistency Example

Given:
- output requires monthly revenue by customer
- constraint says include months with zero revenue
- decision says aggregate by `order_date`

Expected behavior:
- keep these elements because they are compatible
- derive success criteria such as accurate monthly aggregation and inclusion of zero-revenue months
- avoid adding implementation details such as calendar table strategy

## Conflict Example

Given:
- output says CSV export
- decision says dashboard only

Expected behavior:
- do not invent a reconciliation
- do not silently choose one
- treat the handoff as inconsistent and return control to `$interview-engine`

## Summary Quality Bar

Good summary behavior:
- explain what is being built
- explain high-level behavior
- include key shaping constraints
- stay within 2-5 sentences

Poor summary behavior:
- include implementation steps
- introduce tools or technologies not provided
- speculate about architecture
- restate the entire handoff verbatim
