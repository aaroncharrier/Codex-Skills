# Artifact Generator Calibration

Use this file to calibrate what compliant rendering looks like. Favor strictness over helpfulness when those conflict.

## Good Behavior

- render only from the provided specification and execution plan
- preserve step order exactly
- surface missing data as metadata or handoff payloads
- keep the final response limited to the allowed YAML object

## Bad Behavior

- rewriting execution steps for clarity
- optimizing SQL beyond the plan
- adding analysis cells to notebooks
- expanding a document outline beyond the plan
- changing prompt hierarchy or emphasis
- filling in unspecified fields with guesses

## Granularity Guidance

- treat each execution-plan step as binding structure
- translate steps at the artifact layer, not at the design layer
- keep headings, sections, blocks, or statements aligned to the planned sequence

## Hash Guidance

When possible, compute hashes with `scripts/compute-hashes.ps1`.

Suggested usage with local files:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\compute-hashes.ps1 -SpecPath <path> -PlanPath <path>
```

Suggested usage with raw text:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\compute-hashes.ps1 -SpecText "<spec text>" -PlanText "<plan text>"
```

If hashing cannot be performed because the source text is unavailable in a callable form, preserve the metadata fields and use a stable sentinel that truthfully reflects the missing hash source rather than fabricating a value.
