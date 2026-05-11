# Data Quality and Reconciliation Plan Completion Questionnaire

Use this questionnaire to gather the inputs needed to draft a data quality and reconciliation plan for a data analytics project. Answer concretely from a trust, control, and publication-readiness perspective. If an answer is unknown, write `TBD` and name the owner who will resolve it.

## Document Header
- Plan name:
- Domain:
- Primary owner:
- Business owner:
- Version / status:
- Effective date:
- Related SRD / dictionary / mapping / metric / runbook links:

## 1. Objective and Scope
1. What dataset, metric, report, or data product does this plan cover?
2. Why is a formal quality and reconciliation plan needed for this work?
3. Which lifecycle stages are in scope: source receipt, raw landing, transformation, publish, downstream reporting?
4. What is explicitly out of scope?
5. How often should this plan be reviewed?

## 2. Quality Goals
1. What quality dimensions matter most: completeness, accuracy, timeliness, consistency, uniqueness?
2. What business trust expectation must the published output meet?
3. Which freshness SLA or publication cutoff matters?
4. Which quality failures are tolerable as warnings, and which must block publish?

## 3. Data Products and Critical Elements
1. Which datasets, tables, views, metrics, or dashboards are in scope?
2. What is the grain of each published output?
3. Which fields or metrics are critical to business use?
4. Which business decisions depend on those elements?
5. Who owns each critical data product?

## 4. Control Framework
1. What checks should occur at source receipt?
2. What checks should occur after raw landing?
3. What checks should occur during transformation?
4. What checks should occur before publish?
5. What checks should occur in downstream BI or semantic layer outputs?

## 5. Validation Rules
1. Which fields must never be null?
2. What uniqueness, duplication, or grain rules must hold?
3. What type, format, or domain-value checks are required?
4. What range, threshold, or reasonableness checks are required?
5. What mapping coverage or reference-data rules must pass?
6. Who owns each validation rule?

## 6. Reconciliation Approach
1. What source-to-raw reconciliation is required?
2. What raw-to-curated reconciliation is required?
3. What curated-to-report or semantic-layer reconciliation is required?
4. What manual or business reasonableness checks are required?
5. How often should each reconciliation occur?
6. Who owns each reconciliation step?

## 7. Thresholds and Tolerances
1. What null, duplicate, or variance thresholds are acceptable?
2. What late-data tolerance exists, if any?
3. What thresholds automatically block publish?
4. Who can approve publication when a known issue exists?
5. What documentation is required for an override?

## 8. Exception Handling and Evidence
1. What should happen to rejected or bad records?
2. Where should validation and reconciliation evidence be stored?
3. What run metadata or audit trail is required?
4. Who must be notified when quality checks fail?
5. What information must support teams have to diagnose a data quality issue quickly?

## 9. Roles and Review Cadence
1. Which teams own implementation, review, approval, and exception handling?
2. How often should business and technical owners review quality results?
3. Which issues require business signoff versus technical signoff?
4. Who owns plan maintenance after go-live?

## 10. Test and Sign-Off Evidence
1. What sample validations must be performed before release?
2. What aggregate reconciliations must pass before release?
3. What failure scenarios must be tested?
4. What evidence is required for UAT or certification?
5. What conditions must be true before the plan is approved?

## 11. Open Issues
1. What quality rules, thresholds, or data contracts are still unresolved?
2. Which unresolved items could block release or certification?
3. Who owns each open item?
4. By what date must each open item be resolved?

## Final Check
1. What trust risks remain if the project went live today?
2. Which missing controls would create the biggest business or operational exposure?
3. Who owns closing the remaining gaps, and by what date?
