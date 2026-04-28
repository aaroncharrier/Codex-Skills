# Snowflake Defaults

Use these defaults when the user says the project is Snowflake-based and provides no conflicting guidance.

## Typical stack hints

- Warehouse: Snowflake
- Transformations: dbt or SQL
- Orchestration: Airflow, Dagster, or native task scheduling
- IaC: Terraform
- CI/CD: GitHub Actions

## Good topics to capture

- Warehouses and roles
- Environments and account structure
- dbt project location and model layers
- Incremental model strategy
- Streams, tasks, or dynamic table usage
- Cost and warehouse-size sensitivity

## Working-agreement defaults

- Favor explicit model grain and incremental strategy.
- Call out warehouse-cost impact for wide scans or large backfills.
- Preserve downstream contract stability for marts and shared semantic layers.
