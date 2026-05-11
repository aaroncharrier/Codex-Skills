# Simple Metric Definition Template

Use this template when a business user needs to define a metric quickly without filling out a detailed technical document. Keep the wording plain, short, and business-focused.

## How to Use

- Copy the template block below.
- Replace the example text with your metric details.
- Use short sentences.
- If something is unknown, write `TBD`.

## Simple Template

Metric:
`<metric name>`

Definition:
`<plain-English meaning of the metric>`

Formula:
`<formula or calculation>`

Rules:
- `<business rule 1>`
- `<business rule 2>`
- `<business rule 3>`

Used For:
`<what decision, report, or dashboard uses this metric>`

Refresh:
`<daily, weekly, monthly, etc.>`

Owner:
`<business owner or team>`

Notes:
- `<optional note>`

## Example

Metric:
Churn Rate

Definition:
% of customers who became inactive in a given period

Formula:
`churned_customers / total_customers`

Rules:
- churn = no activity for 30 days
- exclude test accounts
- calculated monthly

Used For:
Customer retention reporting

Refresh:
Monthly

Owner:
Customer Analytics

Notes:
- Confirm whether paused accounts count as churned
