#!/usr/bin/env python3
"""
Validate minimum handoff contracts for orchestrator stage outputs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


VALID_STAGES = {
    "intent-interpreter",
    "interview-engine",
    "specification-builder",
    "execution-planner",
    "artifact-generator",
    "validator-file-writer",
}
VALID_PASS_FAIL = {"PASS", "FAIL"}
VALID_ROUTING_HINTS = {"spec_issue", "plan_issue", "artifact_issue", "structural_issue", "none"}


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}")
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc


def require(condition, message):
    if not condition:
        raise ValueError(message)


def require_mapping(value, label):
    require(isinstance(value, dict), f"{label} must be a mapping")
    return value


def require_numeric(value, label):
    require(isinstance(value, (int, float)), f"{label} must be numeric")
    require(0 <= value <= 1, f"{label} must be between 0 and 1")


def lookup_confidence(payload):
    if isinstance(payload, dict):
        if isinstance(payload.get("confidence"), (int, float)):
            return payload["confidence"], "confidence"
        nested = payload.get("interview_result")
        if isinstance(nested, dict) and isinstance(nested.get("confidence"), (int, float)):
            return nested["confidence"], "interview_result.confidence"
    return None, None


def validate_intent(payload):
    payload = require_mapping(payload, "payload")
    require_mapping(payload.get("intent"), "intent")
    require_numeric(payload.get("confidence"), "confidence")


def validate_interview(payload):
    payload = require_mapping(payload, "payload")
    confidence, label = lookup_confidence(payload)
    require_numeric(confidence, label or "confidence")

    for key in ("questions",):
        if key in payload:
            require(isinstance(payload[key], list), f"{key} must be a list when present")
    if "interview_result" in payload:
        interview_result = require_mapping(payload["interview_result"], "interview_result")
        if "questions" in interview_result:
            require(isinstance(interview_result["questions"], list), "interview_result.questions must be a list")


def validate_specification(payload):
    payload = require_mapping(payload, "payload")
    require_mapping(payload.get("refined_understanding"), "refined_understanding")
    require_mapping(payload.get("decision_log"), "decision_log")


def validate_plan(payload):
    payload = require_mapping(payload, "payload")
    require_mapping(payload.get("execution_plan"), "execution_plan")


def validate_artifact(payload):
    payload = require_mapping(payload, "payload")
    if payload.get("status") == "incomplete_inputs":
        require(isinstance(payload.get("missing"), list), "missing must be a list")
        handoff = require_mapping(payload.get("handoff_required"), "handoff_required")
        require(isinstance(handoff.get("target_skill"), str), "handoff_required.target_skill must be a string")
        require(isinstance(handoff.get("reason"), str), "handoff_required.reason must be a string")
        return

    require_mapping(payload.get("artifact"), "artifact")
    require_mapping(payload.get("artifact_metadata"), "artifact_metadata")
    require_mapping(payload.get("validation_flags"), "validation_flags")


def validate_validation(payload):
    payload = require_mapping(payload, "payload")
    if payload.get("status") == "validation_handoff_required":
        handoff = require_mapping(payload.get("handoff_required"), "handoff_required")
        require(isinstance(handoff.get("target_skill"), str), "handoff_required.target_skill must be a string")
        require(isinstance(handoff.get("reason"), str), "handoff_required.reason must be a string")
        return

    report = require_mapping(payload.get("validation_report"), "validation_report")
    require(report.get("pass_fail") in VALID_PASS_FAIL, "validation_report.pass_fail must be PASS or FAIL")
    if "routing_hint" in report:
        require(report["routing_hint"] in VALID_ROUTING_HINTS, "validation_report.routing_hint is invalid")


def validate_stage(stage, payload):
    if stage == "intent-interpreter":
        validate_intent(payload)
    elif stage == "interview-engine":
        validate_interview(payload)
    elif stage == "specification-builder":
        validate_specification(payload)
    elif stage == "execution-planner":
        validate_plan(payload)
    elif stage == "artifact-generator":
        validate_artifact(payload)
    elif stage == "validator-file-writer":
        validate_validation(payload)
    else:
        raise ValueError(f"unsupported stage: {stage}")


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
