# AGENTS Questionnaire (Analytics Engineering Edition)

Use this questionnaire to fill `AGENTS.md`. Answer directly under each question and keep commands exact.

---

# Data Platform and Stack

1. [Required] What core analytics and data platforms are in use?
   Example: `Databricks`, `Snowflake`, `MicroStrategy`, `Python 3.10`, `SQL`, `PySpark`

2. [Required] What orchestrates pipelines and scheduled workloads?
   Example: `Databricks Workflows`, `Airflow`, `Azure Data Factory`

3. [Required] What development patterns are used?
   Example: `Databricks notebooks`, `Databricks Repos`, `CI/CD pipelines`, `SQL views`

4. [Required] What systems are the primary data sources?
   Example: `ERP/CRM APIs`, `flat files`, `event streams`, `SQL Server`, `Postgres`, `SaaS platforms`

5. [Required] What are the system-of-record and reporting platforms?
   Example: `Databricks Delta Lake is the source of truth`, `Snowflake EDW supports reporting`

---

# Validation and Data Quality

6. [Required] What validation or testing expectations should agents follow?
   Example: `row-count validation`, `duplicate checks`, `schema validation`, `reconciliation queries`

7. [Required] What production issues occur most frequently?
   Example: `late-arriving data`, `duplicate records`, `missing data`, `schema drift`

8. [Optional] What refresh expectations or SLAs exist?
   Example: `daily executive reporting`, `hourly operational refreshes`, `dataset-specific SLAs`

9. [Optional] What validation commands or workflows should agents use?
   Example: `pytest`, `sql validation scripts`, `dbt test`

---

# Performance and Cost Constraints

10. [Required] What performance or cost priorities must agents optimize for?
    Example: `query cost optimization`, `cluster efficiency`, `incremental processing`, `partition pruning`, `materialization strategy`

11. [Optional] What runtime or execution constraints matter?
    Example: `Jobs run only in Databricks`, `avoid full-table rewrites`, `Snowflake warehouse costs are monitored`

---

# Security and Governance

12. [Required] What security or governance rules must agents follow?
    Example: `Never expose internal-only PII`, `Do not export production data locally`

13. [Required] What actions are agents explicitly prohibited from performing?
    Example:
    - `No direct database query access`
    - `No direct GitHub write access`
    - `Do not modify production schemas`
    - `Do not overwrite curated tables`

---

# Git and Delivery Workflow

14. [Required] What Git workflow should agents assume?
    Example: `feature branches with PR reviews for Databricks`, `release branches for Snowflake`

15. [Required] What is the definition of done for analytics work?
    Example:
    - `dashboards validated`
    - `documentation updated`
    - `stakeholder sign-off completed`

16. [Required] How is data consumed by downstream users?
    Example: `MicroStrategy dashboards`, `SQL datasets`, `semantic reporting layers`

---

# Agent Operating Principles

17. [Required] What should agents optimize for when making implementation decisions?
    Example:
    - `reliability`
    - `governance`
    - `maintainability`
    - `cost efficiency`
    - `self-service analytics`
    - `delivery speed`

18. [Required] What project-specific guardrails should agents follow?
    Example:
    - `Prefer incremental processing over full refreshes`
    - `Avoid expensive cross-warehouse joins`
    - `Preserve reporting-facing table contracts`
    - `Document schema changes before implementation`