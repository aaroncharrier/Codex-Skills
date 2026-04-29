#!/usr/bin/env python3
"""
Validate the orchestrator session_state schema.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


VALID_STATUS = {"IN_PROGRESS", "COMPLETE", "NEEDS_INTERVENTION"}
VALID_STAGES = {
    "INTENT_INTERPRETATION",
    "INTERVIEW_LOOP",
    "SPECIFICATION_GENERATION",
    "EXECUTION_PLANNING",
    "ARTIFACT_GENERATION",
    "VALIDATION",
}
STAGE_OUTPUT_KEYS = {
    "intent_interpreter",
    "interview_engine",
    "specification_builder",
    "execution_planner",
    "artifact_generator",
    "validator_file_writer",
}
TRACE_STATUS = {"SUCCESS", "FAILED", "BLOCKED"}
STORAGE_MODES = {"session_state_only", "session_state_and_files"}


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


def require_key(mapping, key):
    require(isinstance(mapping, dict), "expected mapping")
    require(key in mapping, f"missing key: {key}")
    return mapping[key]


def validate_compact_stage_entry(entry, label):
    require(isinstance(entry, dict), f"{label} must be a mapping")
    if "status" in entry:
        require(isinstance(entry["status"], str), f"{label}.status must be a string")
    if "summary" in entry:
        require(isinstance(entry["summary"], str), f"{label}.summary must be a string")
    if "snapshot_path" in entry:
        require(isinstance(entry["snapshot_path"], str), f"{label}.snapshot_path must be a string")


def validate_stage_outputs(stage_outputs):
    require(isinstance(stage_outputs, dict), "stage_outputs must be a mapping")
    missing = STAGE_OUTPUT_KEYS - set(stage_outputs.keys())
    require(not missing, f"stage_outputs missing keys: {', '.join(sorted(missing))}")
    for key in STAGE_OUTPUT_KEYS:
        entry = stage_outputs[key]
        require(isinstance(entry, dict), f"{key} must be a mapping")
        require("latest" in entry, f"{key}.latest is required")
        history = require_key(entry, "history")
        require(isinstance(history, list), f"{key}.history must be a list")
        latest = entry["latest"]
        if isinstance(latest, dict):
            validate_compact_stage_entry(latest, f"{key}.latest")
        for index, item in enumerate(history, start=1):
            require(isinstance(item, (dict, list, str, int, float, bool)) or item is None, f"{key}.history[{index}] has invalid type")
            if isinstance(item, dict):
                validate_compact_stage_entry(item, f"{key}.history[{index}]")


def validate_trace(execution_trace):
    require(isinstance(execution_trace, list), "execution_trace must be a list")
    for index, entry in enumerate(execution_trace, start=1):
        require(isinstance(entry, dict), f"execution_trace[{index}] must be a mapping")
        require(isinstance(require_key(entry, "step"), int), f"execution_trace[{index}].step must be an integer")
        require(require_key(entry, "status") in TRACE_STATUS, f"execution_trace[{index}].status is invalid")
        require(isinstance(require_key(entry, "stage"), str), f"execution_trace[{index}].stage must be a string")
        require(isinstance(require_key(entry, "skill"), str), f"execution_trace[{index}].skill must be a string")
        require(isinstance(require_key(entry, "notes"), str), f"execution_trace[{index}].notes must be a string")
        persisted_to = require_key(entry, "persisted_to")
        require(isinstance(persisted_to, dict), f"execution_trace[{index}].persisted_to must be a mapping")
        require(isinstance(require_key(persisted_to, "file_path"), str), f"execution_trace[{index}].persisted_to.file_path must be a string")
        if "memory_key" in persisted_to:
            require(isinstance(persisted_to["memory_key"], str), f"execution_trace[{index}].persisted_to.memory_key must be a string")


def validate_retry_counters(retry_counters):
    require(isinstance(retry_counters, dict), "retry_counters must be a mapping")
    missing = STAGE_OUTPUT_KEYS - set(retry_counters.keys())
    require(not missing, f"retry_counters missing keys: {', '.join(sorted(missing))}")
    for key in STAGE_OUTPUT_KEYS:
        require(isinstance(retry_counters[key], int), f"retry_counters.{key} must be an integer")


def validate_rolling_summary(rolling_summary):
    require(isinstance(rolling_summary, dict), "rolling_summary must be a mapping")
    for key in ("stable_facts", "active_constraints", "current_decisions", "active_assumptions", "unresolved_questions"):
        require(isinstance(require_key(rolling_summary, key), list), f"rolling_summary.{key} must be a list")
    require(isinstance(require_key(rolling_summary, "last_updated_by_stage"), str), "rolling_summary.last_updated_by_stage must be a string")


def validate_artifact_pointer(payload, label):
    require(isinstance(payload, dict), f"{label} must be a mapping")
    require(isinstance(require_key(payload, "present"), bool), f"{label}.present must be boolean")
    require("content" in payload or "snapshot_path" in payload, f"{label} requires content or snapshot_path")
    if "snapshot_path" in payload:
        require(isinstance(payload["snapshot_path"], str), f"{label}.snapshot_path must be a string")


def validate_validation_pointer(payload):
    require(isinstance(payload, dict), "latest_validation must be a mapping")
    require(isinstance(require_key(payload, "present"), bool), "latest_validation.present must be boolean")
    require("pass_fail" in payload, "latest_validation.pass_fail is required")
    if "snapshot_path" in payload:
        require(isinstance(payload["snapshot_path"], str), "latest_validation.snapshot_path must be a string")
    if "routing_hint" in payload:
        require(isinstance(payload["routing_hint"], str), "latest_validation.routing_hint must be a string")


def validate_routing_history(routing_history):
    require(isinstance(routing_history, list), "routing_history must be a list")
    for index, entry in enumerate(routing_history, start=1):
        require(isinstance(entry, dict), f"routing_history[{index}] must be a mapping")
        for key in ("from_stage", "to_stage", "reason", "trigger"):
            require(isinstance(require_key(entry, key), str), f"routing_history[{index}].{key} must be a string")


def validate(payload):
    require(isinstance(payload, dict), "top-level payload must be a mapping")
    session_state = require_key(payload, "session_state")
    require(isinstance(session_state, dict), "session_state must be a mapping")

    require(isinstance(require_key(session_state, "session_id"), str), "session_id must be a string")
    require(require_key(session_state, "status") in VALID_STATUS, "status is invalid")
    require(require_key(session_state, "current_stage") in VALID_STAGES, "current_stage is invalid")

    thresholds = require_key(session_state, "thresholds")
    require(isinstance(thresholds, dict), "thresholds must be a mapping")
    confidence_min = require_key(thresholds, "confidence_min")
    require(isinstance(confidence_min, (int, float)), "thresholds.confidence_min must be numeric")
    require(0 <= confidence_min <= 1, "thresholds.confidence_min must be between 0 and 1")
    if "assumption_budget_max" in thresholds:
        require(isinstance(thresholds["assumption_budget_max"], int), "thresholds.assumption_budget_max must be an integer")

    require(isinstance(require_key(session_state, "raw_user_prompt"), str), "raw_user_prompt must be a string")

    if "rolling_summary" in session_state:
        validate_rolling_summary(session_state["rolling_summary"])

    validate_stage_outputs(require_key(session_state, "stage_outputs"))
    validate_artifact_pointer(require_key(session_state, "latest_valid_artifact"), "latest_valid_artifact")
    validate_validation_pointer(require_key(session_state, "latest_validation"))
    validate_trace(require_key(session_state, "execution_trace"))
    validate_routing_history(require_key(session_state, "routing_history"))

    persistence = require_key(session_state, "persistence")
    require(isinstance(persistence, dict), "persistence must be a mapping")
    require(require_key(persistence, "storage_mode") in STORAGE_MODES, "persistence.storage_mode is invalid")
    require(isinstance(require_key(persistence, "session_folder"), str), "persistence.session_folder must be a string")

    validate_retry_counters(require_key(session_state, "retry_counters"))


def parse_args():
    parser = argparse.ArgumentParser(description="Validate orchestrator session_state YAML.")
    parser.add_argument("input_file", help="YAML file containing session_state")
    return parser.parse_args()


def main():
    args = parse_args()
    payload = load_yaml(Path(args.input_file))
    validate(payload)
    print("OK: session_state is valid")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
