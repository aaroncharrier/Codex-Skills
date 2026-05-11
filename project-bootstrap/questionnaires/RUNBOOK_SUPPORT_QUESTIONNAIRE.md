# Runbook and Support Completion Questionnaire

Use this questionnaire to gather the inputs needed to draft a runbook and support document for a data analytics product. Answer concretely from an operational support perspective. If an answer is unknown, write `TBD` and name the owner who will resolve it.

## Document Header
- Service or data product name:
- Service owner:
- Business owner:
- Primary support team:
- Version / status:
- Effective date:
- Related SRD / release / architecture links:

## 1. Service Overview
1. What pipeline, dataset, semantic layer object, report, or dashboard does this runbook support?
2. What business outcome depends on it?
3. Which environments require support coverage?
4. What is explicitly out of scope for this runbook?
5. How critical is this service to business operations?

## 2. Support Model and Ownership
1. Who owns the service technically?
2. Who performs first-response triage?
3. Which business contact confirms business impact and fallback decisions?
4. Which downstream or platform teams must be involved during incidents?
5. What support hours or on-call coverage exist?

## 3. Dependencies
1. What upstream sources or systems must be available?
2. Which orchestration, storage, compute, or platform services are required?
3. What downstream reports, dashboards, or data products depend on this output?
4. Who owns each dependency?
5. What happens if each dependency fails?

## 4. Normal Operating Expectations
1. When should the process normally run?
2. What freshness or publish SLA must be met?
3. What runtime, latency, or completion thresholds matter?
4. What stale-data behavior is acceptable, if any?
5. How long should logs, evidence, and operational artifacts be retained?

## 5. Monitoring and Alerting
1. What monitors or alerts must exist?
2. What exact conditions should trigger each alert?
3. Which alerts are informational versus incident-triggering?
4. Who receives each alert?
5. Which channels should be used: Teams, email, pager, ticketing?

## 6. Incident Severity
1. How should severity be defined for this service?
2. What is an example of a Sev 1, Sev 2, and Sev 3 issue?
3. What response target applies to each severity?
4. How often should status updates be sent during an incident?

## 7. Failure Scenarios and First Response
1. What are the most likely failure scenarios?
2. What first checks should responders perform for each scenario?
3. Which issues can be safely retried immediately?
4. Which issues should block publish and trigger investigation?
5. Who should be escalated for each major failure type?

## 8. Retry, Rerun, and Recovery
1. When is automatic retry allowed?
2. What must be checked before a manual rerun?
3. How should duplicate data or duplicate publishes be prevented?
4. When is a backfill required?
5. What recovery evidence must be captured after rerun or repair?

## 9. Business Communication and Escalation
1. When should the business be notified?
2. What information should each incident update include?
3. Who decides whether stale data can remain visible or whether publication must be blocked?
4. What is the escalation path if the issue threatens a critical cutoff or executive report?

## 10. Access and Tools
1. Which consoles, logs, dashboards, folders, or tables are needed to troubleshoot?
2. Who should have access to each tool or location?
3. Which links, queries, or commands are worth recording in the runbook?
4. What credentials or secrets handling rules must support staff follow?

## 11. Post-Incident Review
1. Which incidents require a formal review?
2. What evidence must be collected for the review?
3. Who owns preventive follow-up actions?
4. What closes the incident from an operational perspective?

## Final Check
1. What support information is still missing before go-live?
2. Which gaps would make incident response slow or risky?
3. Who owns closing those gaps, and by what date?
