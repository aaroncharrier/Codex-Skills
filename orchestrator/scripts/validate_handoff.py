#!/usr/bin/env python3
"""
Validate minimum handoff contracts for orchestrator stage outputs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


REQUIRED = {
    "intent-interpreter": [["intent_state", "confidence"], ["confidence"]],
    "interview-engine": [["interview_result", "confidence"], ["confidence"]],
    "specification-builder": [["final_specification"]],
    "execution-planner": [["execution_plan"]],
    "artifact-generator": [["generated_artifact"], ["final_artifact"]],
    "validator-file-writer": [["validation", "pass_fail"]],
}

VALID_STAGES = set(REQUIRED)
VALID_PASS_FAIL = {"PASS", "FAIL"}


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}")
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc


def lookup_path(payload, path_parts):
    current = payload
    for part in path_parts:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def ensure_dict(payload):
    if not isinstance(payload, dict):
        raise ValueError("top-level payload must be a mapping")


def validate_confidence(value, label):
    if not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    if value < 0 or value > 1:
        raise ValueError(f"{label} must be between 0 and 1")


def validate_stage(stage, payload):
    ensure_dict(payload)

    accepted_shapes = REQUIRED[stage]
    found = False
    for shape in accepted_shapes:
        value = lookup_path(payload, shape)
        if value is not None:
            found = True
            if stage in {"intent-interpreter", "interview-engine"}:
                validate_confidence(value, ".".join(shape))
            if stage == "validator-file-writer" and value not in VALID_PASS_FAIL:
                raise ValueError("validation.pass_fail must be PASS or FAIL")
            break

    if not found:
        readable = " or ".join(".".join(shape) for shape in accepted_shapes)
        raise ValueError(f"missing required field: {readable}")


def parse_args():
    parser = argparse.ArgumentParser(description="Validate a stage handoff payload.")
    parser.add_argument("stage", choices=sorted(VALID_STAGES))
    parser.add_argument("input_file", help="YAML file containing the stage output")
    return parser.parse_args()


def main():
    args = parse_args()
    payload = load_yaml(Path(args.input_file))
    validate_stage(args.stage, payload)
    print(f"OK: {args.stage} handoff is valid")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
