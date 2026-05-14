# Question Bank - New Data Pipeline

Ask exactly 3 questions at a time.

## Core Discovery
- What source system is being ingested?
- Who owns the source?
- What business problem requires this data?
- What downstream outputs need this data?
- What is the required cadence?
- What delivery window or SLA matters?

## Technical Discovery
- What is the ingestion method: file, API, database, event stream?
- Is the load full, incremental, CDC, or still unknown?
- Is historical backfill required?
- What is the expected grain of the curated output?
- What keys identify uniqueness?
- What schema drift risk exists?
- What deduplication or idempotency behavior is needed?

## Quality and Operations
- What checks must block publish?
- What happens if the source is late?
- What happens if validation fails?
- What retry behavior is expected?
- What alerts are required?
- Who supports failures after release?
