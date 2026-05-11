# Work Log Questionnaire

Use this questionnaire when creating or updating an entry in `docs/WORK_LOG.md`. Answer directly under each question.

## Change Summary

1. [Required] What changed?
   Example: `Added the first ingestion script and source configuration`

2. [Required] Why was the change made?
   Example: `To land the baseline orders dataset for modeling`

## Files and Commands

3. [Required] Which files were touched?
   Example: `repo/src/orders_ingest.py`, `README.md`

4. [Optional] Which commands were run?
   Example: `python -m pytest`, `dbt build --select orders`

## Validation

5. [Optional] What validation was performed, and what happened?
   Example: `Unit tests passed`, `spot-checked 10 rows against source`

## Follow-Up

6. [Optional] What follow-up task comes next?
   Example: `Add refund joins and reconciliation checks`

7. [Optional] Did this work create a new decision or open question?
   Example: `Need to decide whether to snapshot the mapping table daily`

## Attribution

8. [Required] Who made the change, and on what date?
   Example: `Aaron on 2026-05-09`
