# AGENTS Questionnaire (Principal Data Engineering Edition)

Use this questionnaire to fill `AGENTS.md`. This questionnaire is for project orientation and agent operating rules. It is not the questionnaire for building `PROJECT_PLAN.md`. Answer directly under each question, be verbose where helpful, and keep commands exact.

---

# Project Orientation

1. [Required] What is the primary project mode?
   Choose one: `discovery`, `source onboarding`, `full pipeline delivery`, `model enhancement`, `reporting/dashboard delivery`, `optimization`, `production support`

2. [Optional] What secondary project modes also apply?
   Example: `discovery`, `reporting/dashboard delivery`

3. [Required] At a high level, what is this project trying to accomplish?
   Example: `Integrate a new HR source into Databricks, publish curated data to Snowflake, and enable a MicroStrategy dashboard refresh`

4. [Required] Which systems and platforms are involved, and what object or asset types are likely to change?
   Example: `Databricks notebooks and jobs`, `Snowflake tables/views`, `MicroStrategy datasets/reports`, `Python`, `SQL`, `PySpark`

5. [Required] What outputs or downstream assets should agents expect this project to produce or affect?
   Example: `ingestion code`, `transformation logic`, `curated tables`, `validation queries`, `dashboard datasets`, `support docs`

---

# Operating Posture

6. [Required] What role should Codex adopt for this project?
   Example: `Principal Data Engineer`, `hands-on Data Engineer`, `technical reviewer`

7. [Required] How much autonomy should Codex assume before acting?
   Example: `Ask before any non-trivial action`, `Ask before acting unless explicitly told to proceed autonomously`

8. [Required] Which kinds of decisions always require your approval before implementation?
   Example: `architecture changes`, `schema or contract changes`, `naming standards with broad impact`, `stakeholder-facing output changes`

9. [Required] When tradeoffs appear, what should Codex optimize for by default?
   Example: `correctness`, `governance`, `maintainability`, `delivery speed`, `cost optimization`

10. [Optional] What principal-engineer behaviors do you want Codex to show?
    Example: `clarify intent before coding`, `think in systems`, `surface tradeoffs and blind spots`, `improve validation and documentation maturity`

---

# Workspace and Structure

11. [Required] What languages, tools, and local environment conventions should agents assume?
    Example: `Python 3.11`, `SQL`, `PySpark`, `Databricks`, `Snowflake`, `MicroStrategy`, `uv`, `pytest`

12. [Required] How should `repo/` and `docs/` be used at project start, and what contents do you expect in each?
    Example: ``repo/` for notebooks, SQL, Python, configs, tests; `docs/` for plans, mappings, validation notes, runbooks, and support docs``

13. [Optional] Are there any established naming, folder, or file-placement conventions agents should follow?
    Example: `keep the project minimal at first`, `add subfolders only when needed`, `store reusable SQL under repo/sql`

14. [Required] What Git workflow should agents assume?
    Example: `feature branches with PRs`, `direct commits only when explicitly requested`

---

# Execution Boundaries and Safety

15. [Required] What environment boundaries matter at a high level?
    Example: `local development`, `dev/test/prod data platforms`, `separate reporting environments`, `approved promotion paths`

16. [Required] What execution or access constraints must agents assume?
    Example: `Codex works locally only`, `no direct Databricks execution`, `no direct Snowflake execution`, `no production access`

17. [Required] What security, governance, or data-handling rules must agents follow?
    Example: `do not export production data locally`, `do not change production schemas directly`, `document code changes clearly in markdown`

---

# Validation, Handoff, and Communication

18. [Required] What validation categories should Codex think about, even when not all checks can be executed directly?
    Example: `unit tests`, `schema validation`, `row-count reconciliation`, `duplicate checks`, `dashboard QA`, `manual validation handoff`

19. [Optional] What local commands should agents run when they can validate locally?
    Example: `python -m pytest`, `ruff check .`, `sqlfluff lint`, `custom validation scripts`

20. [Required] When Codex cannot run the final platform or reporting steps, what handoff details must be provided?
    Example: `execution steps`, `parameters`, `expected results`, `validation checklist`, `follow-up risks`

21. [Required] How should Codex explain code and document changes back to you?
    Example: `what changed`, `why it changed`, `how to validate`, `assumptions`, `follow-up or handoff`, `use Databricks or Snowflake explainer skills for complex changes if available`

22. [Optional] Which documentation assets should this project improve or create if they are missing?
    Example: `runbooks`, `validation notes`, `source-to-target mappings`, `lineage notes`, `metric definitions`, `support documentation`

23. [Required] What is the default definition of done for this project?
    Example: `implementation or analysis complete`, `validation run or documented`, `relevant markdown updated`, `unresolved risks and handoffs made explicit`
