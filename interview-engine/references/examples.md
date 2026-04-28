# Interview Engine Examples

Use these examples to calibrate question depth, breadth, and stopping behavior. Do not copy them into the user-facing output. Use them to recognize patterns.

## SQL Example

Initial prompt:

`Write a query to calculate revenue by month`

Expected first-pass behavior:
- identify missing source table
- identify missing revenue definition
- identify missing date field
- avoid writing SQL

Typical first themes:
- `data`
- `requirements`

Typical follow-up shift:
- move from source-definition questions to output-format and edge-case questions
- ask about zero-value periods only after the core aggregation logic is defined

Termination pattern:
- stop once the table, revenue logic, time field, output columns, and missing-period rule are confirmed

## AGENTS.md Example

Initial prompt:

`Create an AGENTS.md for my project`

Expected first-pass behavior:
- identify project type
- identify agent set or agent categories
- identify ownership boundaries and success criteria
- avoid drafting the file

Typical first themes:
- `requirements`
- `constraints`
- `success_criteria`

Typical follow-up shift:
- move into communication boundaries, failure conditions, and expected inputs and outputs per agent

Termination pattern:
- stop once the project context, agent responsibilities, interfaces, constraints, and document expectations are clear enough for a downstream writer

## Notebook Example

Initial prompt:

`Build a Databricks notebook for analytics`

Expected first-pass behavior:
- clarify source data
- clarify analysis objective
- clarify target output shape
- avoid building the notebook

Typical first themes:
- `data`
- `requirements`
- `output_format`

Typical follow-up shift:
- refine operational definitions, time windows, aggregations, and feature expectations

Termination pattern:
- stop once the dataset, goal, business logic, granularity, and output target are sufficiently specified

## General Quality Bar

Good behavior:
- reduce ambiguity fast
- ask only high-leverage questions
- narrow from broad to precise across iterations
- terminate as soon as the handoff is clean

Poor behavior:
- asking trivia
- asking redundant questions
- jumping into solutions
- skipping contradictions
- continuing after the request is already execution-ready
