# Databricks Defaults

Use these defaults when the user says the project is Databricks-based and provides no conflicting guidance.

## Typical stack hints

- Platform: Databricks
- Compute: jobs or interactive clusters
- Storage: Delta Lake
- Governance: Unity Catalog
- Transformations: Spark SQL, PySpark, dbt, or Delta Live Tables
- Orchestration: Databricks Jobs, Airflow, or Dagster

## Good topics to capture

- Workspace and catalog structure
- Job orchestration model
- Notebook versus package-based development
- Delta table expectations
- Medallion layer conventions if used
- Cluster policy and cost constraints

## Working-agreement defaults

- Call out data-skew and shuffle risk for Spark-heavy changes.
- Prefer reproducible job code over ad hoc notebook-only logic when possible.
- Highlight Unity Catalog, access-control, and production promotion assumptions.
