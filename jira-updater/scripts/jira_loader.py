#!/usr/bin/env python3
"""
Validate and execute Jira Cloud mutations from markdown artifacts.

Supported schemas:
- create
- update
- comment
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

import yaml

SCHEMA_ACTIONS = {
    "create": "create",
    "update": "update",
    "comment": "comment",
}

SUPPORTED_ISSUE_TYPES = {
    "Epic",
    "Story",
    "Task",
    "Bug",
    "Sub-task",
}

FRONT_MATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
ISSUE_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
CUSTOM_FIELD_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
LISTISH_FIELDS = {"fix_versions", "labels", "components", "clear_fields"}
CREATE_ALLOWED_KEYS = {
    "schema",
    "project",
    "issue_type",
    "summary",
    "parent_issue",
    "parent_epic",
    "fix_versions",
    "labels",
    "components",
    "priority",
    "assignee",
    "reporter",
    "work_type",
    "custom_fields",
}
UPDATE_ALLOWED_KEYS = {
    "schema",
    "issue_key",
    "summary",
    "parent_issue",
    "parent_epic",
    "fix_versions",
    "labels",
    "components",
    "priority",
    "assignee",
    "reporter",
    "work_type",
    "custom_fields",
    "clear_fields",
}
COMMENT_ALLOWED_KEYS = {"schema", "issue_key"}
CURATED_MUTATION_FIELDS = {
    "summary",
    "parent_issue",
    "parent_epic",
    "fix_versions",
    "labels",
    "components",
    "priority",
    "assignee",
    "reporter",
    "work_type",
    "description",
}
HTTP_OK_NO_CONTENT = {204}
ENV_VARS = ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN")


class JiraLoaderError(Exception):
    """Base error for loader failures."""


class ValidationError(JiraLoaderError):
    """Raised when a local artifact is invalid."""


class JiraApiError(JiraLoaderError):
    """Raised when Jira responds with an error."""

    def __init__(self, method: str, url: str, status_code: int, body: str) -> None:
        super().__init__(f"Jira API error {status_code} for {method} {url}")
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body


@dataclass
class ParsedArtifact:
    path: Path
    schema: str
    action: str
    front_matter: dict[str, Any]
    body_markdown: str
    project: str | None = None
    issue_type: str | None = None
    summary: str | None = None
    issue_key: str | None = None
    parent_issue: str | None = None
    parent_epic: str | None = None
    fix_versions: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    components: list[str] = field(default_factory=list)
    priority: str | None = None
    assignee: str | None = None
    reporter: str | None = None
    work_type: str | None = None
    custom_fields: dict[str, Any] = field(default_factory=dict)
    clear_fields: list[str] = field(default_factory=list)

    def body_required(self) -> bool:
        return self.action in {"create", "comment"}

    def to_summary(self) -> dict[str, Any]:
        return {
            "file": str(self.path),
            "schema": self.schema,
            "action": self.action,
            "project": self.project,
            "issue_type": self.issue_type,
            "summary": self.summary,
            "issue_key": self.issue_key,
            "parent_issue": self.parent_issue,
            "parent_epic": self.parent_epic,
            "fix_versions": self.fix_versions,
            "labels": self.labels,
            "components": self.components,
            "priority": self.priority,
            "assignee": self.assignee,
            "reporter": self.reporter,
            "work_type": self.work_type,
            "custom_field_ids": sorted(self.custom_fields.keys()),
            "clear_fields": self.clear_fields,
            "body_present": bool(self.body_markdown.strip()),
        }


@dataclass
class MutationPreview:
    artifact: ParsedArtifact
    local_errors: list[str] = field(default_factory=list)
    local_warnings: list[str] = field(default_factory=list)
    live_errors: list[str] = field(default_factory=list)
    live_warnings: list[str] = field(default_factory=list)
    jira_fields: dict[str, Any] = field(default_factory=dict)
    jira_comment_body: dict[str, Any] | None = None
    resolved_issue_type_id: str | None = None
    pending_live_resolution: list[str] = field(default_factory=list)
    metadata_checked: bool = False
    diff: dict[str, Any] = field(default_factory=dict)
    target_issue_summary: str | None = None

    @property
    def ok(self) -> bool:
        return not self.local_errors and not self.live_errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "artifact": self.artifact.to_summary(),
            "local_errors": self.local_errors,
            "local_warnings": self.local_warnings,
            "live_errors": self.live_errors,
            "live_warnings": self.live_warnings,
            "metadata_checked": self.metadata_checked,
            "resolved_issue_type_id": self.resolved_issue_type_id,
            "pending_live_resolution": self.pending_live_resolution,
            "jira_fields": self.jira_fields,
            "jira_comment_body": self.jira_comment_body,
            "target_issue_summary": self.target_issue_summary,
            "diff": self.diff,
        }


def adf_doc(content: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {"version": 1, "type": "doc", "content": content or []}


def merge_adjacent_text_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for node in nodes:
        if (
            merged
            and merged[-1].get("type") == "text"
            and node.get("type") == "text"
            and merged[-1].get("marks") == node.get("marks")
        ):
            merged[-1]["text"] += node.get("text", "")
            continue
        merged.append(node)
    return merged


def apply_mark(nodes: list[dict[str, Any]], mark: dict[str, Any]) -> list[dict[str, Any]]:
    marked: list[dict[str, Any]] = []
    for node in nodes:
        if node.get("type") != "text":
            marked.append(node)
            continue
        clone = dict(node)
        marks = list(clone.get("marks", []))
        marks.append(mark)
        clone["marks"] = marks
        marked.append(clone)
    return merge_adjacent_text_nodes(marked)


def parse_inline(text: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    buffer: list[str] = []
    index = 0

    def flush_buffer() -> None:
        if buffer:
            nodes.append({"type": "text", "text": "".join(buffer)})
            buffer.clear()

    while index < len(text):
        if text.startswith("**", index) or text.startswith("__", index):
            delimiter = text[index : index + 2]
            end_index = text.find(delimiter, index + 2)
            if end_index != -1 and end_index > index + 2:
                flush_buffer()
                nodes.extend(
                    apply_mark(parse_inline(text[index + 2 : end_index]), {"type": "strong"})
                )
                index = end_index + 2
                continue

        if text[index] in "*_":
            delimiter = text[index]
            end_index = text.find(delimiter, index + 1)
            if end_index != -1 and end_index > index + 1:
                flush_buffer()
                nodes.extend(
                    apply_mark(parse_inline(text[index + 1 : end_index]), {"type": "em"})
                )
                index = end_index + 1
                continue

        if text[index] == "`":
            end_index = text.find("`", index + 1)
            if end_index != -1 and end_index > index + 1:
                flush_buffer()
                nodes.append(
                    {
                        "type": "text",
                        "text": text[index + 1 : end_index],
                        "marks": [{"type": "code"}],
                    }
                )
                index = end_index + 1
                continue

        if text[index] == "[":
            label_end = text.find("]", index + 1)
            if label_end != -1 and label_end + 1 < len(text) and text[label_end + 1] == "(":
                url_end = text.find(")", label_end + 2)
                if url_end != -1:
                    flush_buffer()
                    label = text[index + 1 : label_end]
                    url = text[label_end + 2 : url_end].strip()
                    nodes.extend(
                        apply_mark(parse_inline(label), {"type": "link", "attrs": {"href": url}})
                    )
                    index = url_end + 1
                    continue

        buffer.append(text[index])
        index += 1

    flush_buffer()
    return merge_adjacent_text_nodes(nodes)


def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s+\S", line))


def is_code_fence(line: str) -> bool:
    return line.strip().startswith("```")


def is_blockquote(line: str) -> bool:
    return line.lstrip().startswith(">")


def is_bullet_item(line: str) -> bool:
    return bool(re.match(r"^\s*[-*+]\s+\S", line))


def is_ordered_item(line: str) -> bool:
    return bool(re.match(r"^\s*\d+[.)]\s+\S", line))


def parse_markdown_to_adf(markdown: str) -> dict[str, Any]:
    normalized = markdown.replace("\r\n", "\n").strip("\n")
    if not normalized.strip():
        return adf_doc([])
    lines = normalized.split("\n")
    return adf_doc(_parse_blocks(lines))


def _parse_blocks(lines: list[str]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        if is_code_fence(line):
            node, index = _parse_code_block(lines, index)
            blocks.append(node)
            continue

        if is_heading(line):
            node, index = _parse_heading(line, index)
            blocks.append(node)
            continue

        if is_blockquote(line):
            node, index = _parse_blockquote(lines, index)
            blocks.append(node)
            continue

        if is_bullet_item(line):
            node, index = _parse_list(lines, index, ordered=False)
            blocks.append(node)
            continue

        if is_ordered_item(line):
            node, index = _parse_list(lines, index, ordered=True)
            blocks.append(node)
            continue

        node, index = _parse_paragraph(lines, index)
        blocks.append(node)

    return blocks


def _parse_code_block(lines: list[str], index: int) -> tuple[dict[str, Any], int]:
    opening = lines[index].strip()
    language = opening[3:].strip() or None
    index += 1
    code_lines: list[str] = []
    while index < len(lines) and not lines[index].strip().startswith("```"):
        code_lines.append(lines[index])
        index += 1
    if index < len(lines):
        index += 1
    attrs = {"language": language} if language else {}
    return (
        {
            "type": "codeBlock",
            "attrs": attrs,
            "content": [{"type": "text", "text": "\n".join(code_lines)}],
        },
        index,
    )


def _parse_heading(line: str, index: int) -> tuple[dict[str, Any], int]:
    match = re.match(r"^(#{1,6})\s+(.*)$", line)
    assert match
    level = min(len(match.group(1)), 6)
    text = match.group(2).strip()
    return (
        {
            "type": "heading",
            "attrs": {"level": level},
            "content": parse_inline(text),
        },
        index + 1,
    )


def _parse_blockquote(lines: list[str], index: int) -> tuple[dict[str, Any], int]:
    quote_lines: list[str] = []
    while index < len(lines):
        line = lines[index]
        if is_blockquote(line):
            stripped = line.lstrip()
            if stripped.startswith(">"):
                stripped = stripped[1:]
            if stripped.startswith(" "):
                stripped = stripped[1:]
            quote_lines.append(stripped)
            index += 1
            continue
        if not line.strip():
            quote_lines.append("")
            index += 1
            continue
        break

    content = _parse_blocks(quote_lines)
    if not content:
        content = [{"type": "paragraph", "content": []}]
    return {"type": "blockquote", "content": content}, index


def _parse_list(
    lines: list[str],
    index: int,
    *,
    ordered: bool,
) -> tuple[dict[str, Any], int]:
    pattern = r"^\s*(\d+)[.)]\s+(.*)$" if ordered else r"^\s*[-*+]\s+(.*)$"
    item_nodes: list[dict[str, Any]] = []
    order = 1

    while index < len(lines):
        match = re.match(pattern, lines[index])
        if not match:
            break
        if ordered and not item_nodes:
            order = int(match.group(1))
            first_line = match.group(2)
        elif ordered:
            first_line = match.group(2)
        else:
            first_line = match.group(1)

        item_lines = [first_line]
        index += 1
        while index < len(lines):
            next_line = lines[index]
            if not next_line.strip():
                index += 1
                break
            if re.match(pattern, next_line):
                break
            if is_heading(next_line) or is_code_fence(next_line):
                break
            if (ordered and is_bullet_item(next_line)) or (not ordered and is_ordered_item(next_line)):
                break
            item_lines.append(next_line.strip())
            index += 1

        paragraph_text = " ".join(part.strip() for part in item_lines if part.strip())
        paragraph_node = {
            "type": "paragraph",
            "content": parse_inline(paragraph_text),
        }
        item_nodes.append({"type": "listItem", "content": [paragraph_node]})

        while index < len(lines) and not lines[index].strip():
            index += 1

    node: dict[str, Any] = {
        "type": "orderedList" if ordered else "bulletList",
        "content": item_nodes,
    }
    if ordered and order != 1:
        node["attrs"] = {"order": order}
    return node, index


def _parse_paragraph(lines: list[str], index: int) -> tuple[dict[str, Any], int]:
    paragraph_lines: list[str] = []
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        if paragraph_lines and (
            is_heading(line)
            or is_code_fence(line)
            or is_blockquote(line)
            or is_bullet_item(line)
            or is_ordered_item(line)
        ):
            break
        paragraph_lines.append(line.strip())
        index += 1

    text = " ".join(paragraph_lines)
    return {"type": "paragraph", "content": parse_inline(text)}, index


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n")


def load_artifact(path: str | Path) -> ParsedArtifact:
    file_path = Path(path)
    raw_text = file_path.read_text(encoding="utf-8")
    normalized_text = normalize_newlines(raw_text)
    front_matter_match = FRONT_MATTER_PATTERN.match(normalized_text)
    if not front_matter_match:
        raise ValidationError("Missing YAML front matter delimited by --- lines.")

    front_matter_text = front_matter_match.group(1)
    body_markdown = normalized_text[front_matter_match.end() :].lstrip("\n")
    front_matter = yaml.safe_load(front_matter_text) or {}
    if not isinstance(front_matter, dict):
        raise ValidationError("YAML front matter must parse to a mapping.")

    schema = front_matter.get("schema")
    if schema not in SCHEMA_ACTIONS:
        supported = ", ".join(sorted(SCHEMA_ACTIONS))
        raise ValidationError(f"Unsupported schema '{schema}'. Expected one of: {supported}.")

    action = SCHEMA_ACTIONS[schema]
    allowed_keys = {
        "create": CREATE_ALLOWED_KEYS,
        "update": UPDATE_ALLOWED_KEYS,
        "comment": COMMENT_ALLOWED_KEYS,
    }[action]

    unknown_keys = sorted(set(front_matter) - allowed_keys)
    if unknown_keys:
        raise ValidationError(
            "Unsupported YAML keys for this schema: " + ", ".join(unknown_keys)
        )

    artifact = ParsedArtifact(
        path=file_path,
        schema=schema,
        action=action,
        front_matter=front_matter,
        body_markdown=body_markdown,
    )

    artifact.project = _normalize_optional_string(front_matter.get("project"), "project")
    artifact.issue_type = _normalize_issue_type(front_matter.get("issue_type"), required=False)
    artifact.summary = _normalize_optional_string(front_matter.get("summary"), "summary")
    artifact.issue_key = _normalize_optional_string(front_matter.get("issue_key"), "issue_key")
    artifact.parent_issue = _normalize_optional_string(front_matter.get("parent_issue"), "parent_issue")
    artifact.parent_epic = _normalize_optional_string(front_matter.get("parent_epic"), "parent_epic")
    artifact.priority = _normalize_optional_string(front_matter.get("priority"), "priority")
    artifact.assignee = _normalize_optional_string(front_matter.get("assignee"), "assignee")
    artifact.reporter = _normalize_optional_string(front_matter.get("reporter"), "reporter")
    artifact.work_type = _normalize_optional_string(front_matter.get("work_type"), "work_type")
    artifact.fix_versions = _normalize_string_list(front_matter.get("fix_versions"), "fix_versions")
    artifact.labels = _normalize_string_list(front_matter.get("labels"), "labels")
    artifact.components = _normalize_string_list(front_matter.get("components"), "components")
    artifact.clear_fields = _normalize_string_list(front_matter.get("clear_fields"), "clear_fields")
    artifact.custom_fields = _normalize_custom_fields(front_matter.get("custom_fields"))

    _validate_artifact_rules(artifact)
    return artifact


def _normalize_optional_string(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        value = str(value)
    if not isinstance(value, str):
        raise ValidationError(f"'{field_name}' must be a string when provided.")
    normalized = value.strip()
    return normalized or None


def _normalize_issue_type(value: Any, *, required: bool) -> str | None:
    normalized = _normalize_optional_string(value, "issue_type")
    if normalized is None:
        if required:
            raise ValidationError("'issue_type' is required.")
        return None
    canonical = next((item for item in SUPPORTED_ISSUE_TYPES if item.lower() == normalized.lower()), None)
    if canonical is None:
        allowed = ", ".join(sorted(SUPPORTED_ISSUE_TYPES))
        raise ValidationError(f"Unsupported issue_type '{normalized}'. Expected one of: {allowed}.")
    return canonical


def _normalize_string_list(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    if not isinstance(value, list):
        raise ValidationError(f"'{field_name}' must be a list of strings.")
    normalized: list[str] = []
    for item in value:
        if isinstance(item, (int, float)):
            item = str(item)
        if not isinstance(item, str):
            raise ValidationError(f"'{field_name}' must contain only strings.")
        stripped = item.strip()
        if stripped:
            normalized.append(stripped)
    return normalized


def _normalize_custom_fields(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValidationError("'custom_fields' must be a mapping of Jira field id to value.")
    normalized: dict[str, Any] = {}
    for key, field_value in value.items():
        if not isinstance(key, str) or not CUSTOM_FIELD_ID_PATTERN.match(key):
            raise ValidationError(f"Invalid custom field id '{key}'.")
        normalized[key] = field_value
    return normalized


def _validate_artifact_rules(artifact: ParsedArtifact) -> None:
    if artifact.action == "create":
        artifact.issue_type = _normalize_issue_type(artifact.front_matter.get("issue_type"), required=True)
        if artifact.project is None:
            raise ValidationError("'project' is required for create.")
        if artifact.summary is None:
            raise ValidationError("'summary' is required for create.")
        if artifact.issue_type == "Sub-task" and artifact.parent_issue is None:
            raise ValidationError("'parent_issue' is required for Sub-task creates.")
        if artifact.issue_type != "Sub-task" and artifact.parent_issue is not None:
            raise ValidationError("'parent_issue' is only supported for Sub-task creates.")
        if artifact.body_required() and not artifact.body_markdown.strip():
            raise ValidationError("Create artifacts require a markdown body.")

    elif artifact.action == "update":
        if artifact.issue_key is None:
            raise ValidationError("'issue_key' is required for update.")
        if artifact.issue_type is not None:
            raise ValidationError("'issue_type' is not supported for update.")
        if artifact.project is not None:
            raise ValidationError("'project' is not supported for update.")
        if artifact.clear_fields:
            invalid = [item for item in artifact.clear_fields if item not in CURATED_MUTATION_FIELDS and not CUSTOM_FIELD_ID_PATTERN.match(item)]
            if invalid:
                raise ValidationError(
                    "Unsupported clear_fields entries: " + ", ".join(sorted(invalid))
                )
        if not any(
            [
                artifact.summary,
                artifact.parent_issue,
                artifact.parent_epic,
                artifact.fix_versions,
                artifact.labels,
                artifact.components,
                artifact.priority,
                artifact.assignee,
                artifact.reporter,
                artifact.work_type,
                artifact.custom_fields,
                artifact.clear_fields,
                artifact.body_markdown.strip(),
            ]
        ):
            raise ValidationError("Update artifacts must change at least one field or include a body.")

    else:
        if artifact.issue_key is None:
            raise ValidationError("'issue_key' is required for comment.")
        if not artifact.body_markdown.strip():
            raise ValidationError("Comment artifacts require a markdown body.")

    if artifact.issue_key and not ISSUE_KEY_PATTERN.match(artifact.issue_key):
        raise ValidationError(f"'issue_key' must look like a Jira key. Got '{artifact.issue_key}'.")
    if artifact.parent_issue and not ISSUE_KEY_PATTERN.match(artifact.parent_issue):
        raise ValidationError(
            f"'parent_issue' must look like a Jira key. Got '{artifact.parent_issue}'."
        )
    if artifact.parent_epic and not ISSUE_KEY_PATTERN.match(artifact.parent_epic):
        raise ValidationError(
            f"'parent_epic' must look like a Jira key. Got '{artifact.parent_epic}'."
        )


class JiraClient:
    def __init__(self, base_url: str, email: str, api_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.api_token = api_token

    @classmethod
    def from_env(cls) -> "JiraClient":
        missing = [name for name in ENV_VARS if not os.getenv(name)]
        if missing:
            raise ValidationError("Missing Jira environment variables: " + ", ".join(missing))
        return cls(
            base_url=os.environ["JIRA_BASE_URL"],
            email=os.environ["JIRA_EMAIL"],
            api_token=os.environ["JIRA_API_TOKEN"],
        )

    def _request_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        request_data = None
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + base64.b64encode(
                f"{self.email}:{self.api_token}".encode("utf-8")
            ).decode("ascii"),
        }
        if payload is not None:
            request_data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib_request.Request(url, data=request_data, method=method, headers=headers)

        try:
            with urllib_request.urlopen(request) as response:
                body = response.read()
                if response.status in HTTP_OK_NO_CONTENT or not body:
                    return {}
                return json.loads(body.decode("utf-8"))
        except urllib_error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise JiraApiError(method, url, exc.code, error_body) from exc

    def get_issue(self, issue_key: str) -> dict[str, Any]:
        safe_key = urllib_parse.quote(issue_key)
        return self._request_json("GET", f"/rest/api/3/issue/{safe_key}")

    def get_field_catalog(self) -> list[dict[str, Any]]:
        data = self._request_json("GET", "/rest/api/3/field")
        if isinstance(data, list):
            return data
        return data.get("values", [])

    def get_create_issue_types(self, project_key: str) -> list[dict[str, Any]]:
        safe_project = urllib_parse.quote(project_key)
        data = self._request_json(
            "GET", f"/rest/api/3/issue/createmeta/{safe_project}/issuetypes"
        )
        if isinstance(data, list):
            return data
        return data.get("issueTypes", data.get("values", []))

    def get_create_field_metadata(self, project_key: str, issue_type_id: str) -> dict[str, Any]:
        safe_project = urllib_parse.quote(project_key)
        safe_issue_type = urllib_parse.quote(issue_type_id)
        data = self._request_json(
            "GET",
            f"/rest/api/3/issue/createmeta/{safe_project}/issuetypes/{safe_issue_type}",
        )
        if "fields" in data:
            return data["fields"]
        return data

    def get_edit_metadata(self, issue_key: str) -> dict[str, Any]:
        safe_key = urllib_parse.quote(issue_key)
        data = self._request_json("GET", f"/rest/api/3/issue/{safe_key}/editmeta")
        return data.get("fields", {})

    def create_issue(self, fields: dict[str, Any]) -> dict[str, Any]:
        return self._request_json("POST", "/rest/api/3/issue", {"fields": fields})

    def update_issue(self, issue_key: str, fields: dict[str, Any]) -> dict[str, Any]:
        safe_key = urllib_parse.quote(issue_key)
        return self._request_json("PUT", f"/rest/api/3/issue/{safe_key}", {"fields": fields})

    def add_comment(self, issue_key: str, body: dict[str, Any]) -> dict[str, Any]:
        safe_key = urllib_parse.quote(issue_key)
        return self._request_json(
            "POST", f"/rest/api/3/issue/{safe_key}/comment", {"body": body}
        )


def build_preview(artifact: ParsedArtifact, client: JiraClient | None = None) -> MutationPreview:
    preview = MutationPreview(artifact=artifact)
    description_adf = parse_markdown_to_adf(artifact.body_markdown)

    if artifact.action == "comment":
        preview.jira_comment_body = description_adf
    elif artifact.action == "create":
        preview.jira_fields = _build_local_create_fields(artifact, description_adf, preview)
    else:
        preview.jira_fields = _build_local_update_fields(artifact, description_adf, preview)

    if client is None:
        if artifact.action != "comment":
            preview.local_warnings.append(
                "Live Jira validation skipped because Jira environment variables are not set."
            )
        return preview

    preview.metadata_checked = True
    if artifact.action == "create":
        _enrich_create_preview(preview, client, description_adf)
    elif artifact.action == "update":
        _enrich_update_preview(preview, client, description_adf)
    else:
        _enrich_comment_preview(preview, client)

    return preview


def _build_local_create_fields(
    artifact: ParsedArtifact,
    description_adf: dict[str, Any],
    preview: MutationPreview,
) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "project": {"key": artifact.project},
        "issuetype": {"name": artifact.issue_type},
        "summary": artifact.summary,
        "description": description_adf,
    }
    if artifact.fix_versions:
        fields["fixVersions"] = [{"name": item} for item in artifact.fix_versions]
    if artifact.labels:
        fields["labels"] = list(artifact.labels)
    if artifact.components:
        fields["components"] = [{"name": item} for item in artifact.components]
    if artifact.priority:
        fields["priority"] = {"name": artifact.priority}
    if artifact.assignee:
        fields["assignee"] = {"accountId": artifact.assignee}
    if artifact.reporter:
        fields["reporter"] = {"accountId": artifact.reporter}
    if artifact.parent_issue:
        fields["parent"] = {"key": artifact.parent_issue}
    if artifact.parent_epic:
        preview.pending_live_resolution.append("parent_epic")
    if artifact.work_type:
        preview.pending_live_resolution.append("work_type")
    fields.update(artifact.custom_fields)
    return fields


def _build_local_update_fields(
    artifact: ParsedArtifact,
    description_adf: dict[str, Any],
    preview: MutationPreview,
) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    if artifact.summary:
        fields["summary"] = artifact.summary
    if artifact.fix_versions:
        fields["fixVersions"] = [{"name": item} for item in artifact.fix_versions]
    if artifact.labels:
        fields["labels"] = list(artifact.labels)
    if artifact.components:
        fields["components"] = [{"name": item} for item in artifact.components]
    if artifact.priority:
        fields["priority"] = {"name": artifact.priority}
    if artifact.assignee:
        fields["assignee"] = {"accountId": artifact.assignee}
    if artifact.reporter:
        fields["reporter"] = {"accountId": artifact.reporter}
    if artifact.parent_issue:
        fields["parent"] = {"key": artifact.parent_issue}
    if artifact.parent_epic:
        preview.pending_live_resolution.append("parent_epic")
    if artifact.work_type:
        preview.pending_live_resolution.append("work_type")
    if artifact.body_markdown.strip():
        fields["description"] = description_adf
    fields.update(artifact.custom_fields)
    for clear_field in artifact.clear_fields:
        fields[f"__clear__::{clear_field}"] = True
    return fields


def _normalize_metadata_fields(fields: dict[str, Any]) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    for field_id, meta in fields.items():
        clone = dict(meta)
        clone.setdefault("id", field_id)
        normalized[field_id] = clone
    return normalized


def _find_issue_type_by_name(issue_types: list[dict[str, Any]], issue_type_name: str) -> dict[str, Any] | None:
    for issue_type in issue_types:
        if issue_type.get("name", "").lower() == issue_type_name.lower():
            return issue_type
    return None


def _find_field_id_by_name(metadata_fields: dict[str, dict[str, Any]], field_name: str) -> list[str]:
    matches = [
        field_id
        for field_id, meta in metadata_fields.items()
        if meta.get("name", "").lower() == field_name.lower()
    ]
    return matches


def _coerce_value_for_metadata(field_id: str, metadata: dict[str, Any], value: Any) -> Any:
    schema = metadata.get("schema", {})
    schema_type = schema.get("type")
    items_type = schema.get("items")
    system = schema.get("system")

    if field_id == "summary":
        return str(value)
    if field_id == "description":
        return value
    if field_id == "project":
        return {"key": str(value)}
    if field_id == "issuetype":
        return value
    if field_id == "parent":
        return {"key": str(value)}
    if field_id == "labels":
        return list(value)
    if field_id == "fixVersions" or system == "fixVersions" or items_type == "version":
        return [{"name": item} for item in value]
    if field_id == "components" or system == "components" or items_type == "component":
        return [{"name": item} for item in value]
    if field_id == "priority" or schema_type == "priority":
        return {"name": str(value)}
    if schema_type == "user":
        return {"accountId": str(value)}
    if schema_type == "array":
        if items_type == "string":
            return list(value)
        if items_type == "option":
            return [{"value": item} for item in value]
    if schema_type == "option":
        return {"value": str(value)}
    if schema_type in {"string", "number"}:
        return value
    return value


def _resolve_special_field_id(
    *,
    artifact: ParsedArtifact,
    metadata_fields: dict[str, dict[str, Any]],
    field_name: str,
) -> str:
    if field_name == "parent_epic":
        epic_link_matches = _find_field_id_by_name(metadata_fields, "Epic Link")
        if len(epic_link_matches) == 1:
            return epic_link_matches[0]
        if len(epic_link_matches) > 1:
            raise ValidationError("Multiple editable fields matched 'Epic Link'.")
        if "parent" in metadata_fields:
            return "parent"
        raise ValidationError(
            "Unable to resolve a Jira field for 'parent_epic'. Expected editable 'Epic Link' or 'parent'."
        )

    if field_name == "work_type":
        work_type_matches = _find_field_id_by_name(metadata_fields, "Work Type")
        if len(work_type_matches) == 1:
            return work_type_matches[0]
        if not work_type_matches:
            raise ValidationError("Unable to resolve an editable Jira field named 'Work Type'.")
        raise ValidationError("Multiple editable fields matched 'Work Type'.")

    raise ValidationError(f"Unsupported special field resolution for '{field_name}'.")


def _resolve_create_fields(
    artifact: ParsedArtifact,
    metadata_fields: dict[str, dict[str, Any]],
    issue_type_id: str,
    description_adf: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    fields: dict[str, Any] = {
        "project": {"key": artifact.project},
        "issuetype": {"id": issue_type_id},
        "summary": artifact.summary,
        "description": description_adf,
    }

    curated = {
        "fixVersions": artifact.fix_versions,
        "labels": artifact.labels,
        "components": artifact.components,
        "priority": artifact.priority,
        "assignee": artifact.assignee,
        "reporter": artifact.reporter,
        "parent": artifact.parent_issue,
    }
    for field_id, value in curated.items():
        if value in (None, [], {}):
            continue
        meta = metadata_fields.get(field_id, {"id": field_id, "schema": {"type": "string"}})
        fields[field_id] = _coerce_value_for_metadata(field_id, meta, value)

    if artifact.parent_epic:
        field_id = _resolve_special_field_id(
            artifact=artifact,
            metadata_fields=metadata_fields,
            field_name="parent_epic",
        )
        meta = metadata_fields.get(field_id, {"id": field_id, "schema": {"type": "string"}})
        fields[field_id] = _coerce_value_for_metadata(field_id, meta, artifact.parent_epic)

    if artifact.work_type:
        field_id = _resolve_special_field_id(
            artifact=artifact,
            metadata_fields=metadata_fields,
            field_name="work_type",
        )
        meta = metadata_fields[field_id]
        fields[field_id] = _coerce_value_for_metadata(field_id, meta, artifact.work_type)

    for field_id, value in artifact.custom_fields.items():
        if field_id not in metadata_fields:
            raise ValidationError(f"Custom field '{field_id}' is not editable for this create request.")
        fields[field_id] = value

    required_missing = []
    for field_id, meta in metadata_fields.items():
        if not meta.get("required"):
            continue
        if field_id in {"summary", "description"}:
            if fields.get(field_id) in (None, "", []):
                required_missing.append(meta.get("name", field_id))
            continue
        if field_id not in fields:
            required_missing.append(meta.get("name", field_id))
    if required_missing:
        raise ValidationError(
            "Create request is missing Jira-required fields: " + ", ".join(sorted(required_missing))
        )

    if artifact.issue_type == "Epic" and not any(
        meta.get("name", "").lower() == "epic name".lower() for meta in metadata_fields.values()
    ):
        warnings.append("No editable 'Epic Name' field was advertised in create metadata.")

    return fields, warnings


def _resolve_clear_value(field_id: str, metadata: dict[str, Any]) -> Any:
    if field_id == "description":
        return adf_doc([])
    if field_id == "summary":
        raise ValidationError("Clearing 'summary' is not supported.")
    schema = metadata.get("schema", {})
    if schema.get("type") == "array" or field_id in {"labels", "fixVersions", "components"}:
        return []
    return None


def _resolve_update_fields(
    artifact: ParsedArtifact,
    metadata_fields: dict[str, dict[str, Any]],
    description_adf: dict[str, Any],
) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    curated_values = {
        "summary": artifact.summary,
        "fixVersions": artifact.fix_versions,
        "labels": artifact.labels,
        "components": artifact.components,
        "priority": artifact.priority,
        "assignee": artifact.assignee,
        "reporter": artifact.reporter,
        "parent": artifact.parent_issue,
    }
    for field_id, value in curated_values.items():
        if value in (None, [], {}):
            continue
        if field_id not in metadata_fields:
            raise ValidationError(f"Field '{field_id}' is not editable for issue {artifact.issue_key}.")
        fields[field_id] = _coerce_value_for_metadata(field_id, metadata_fields[field_id], value)

    if artifact.parent_epic:
        field_id = _resolve_special_field_id(
            artifact=artifact,
            metadata_fields=metadata_fields,
            field_name="parent_epic",
        )
        fields[field_id] = _coerce_value_for_metadata(
            field_id, metadata_fields[field_id], artifact.parent_epic
        )

    if artifact.work_type:
        field_id = _resolve_special_field_id(
            artifact=artifact,
            metadata_fields=metadata_fields,
            field_name="work_type",
        )
        fields[field_id] = _coerce_value_for_metadata(
            field_id, metadata_fields[field_id], artifact.work_type
        )

    if artifact.body_markdown.strip():
        if "description" not in metadata_fields:
            raise ValidationError(f"Field 'description' is not editable for issue {artifact.issue_key}.")
        fields["description"] = description_adf

    for field_id, value in artifact.custom_fields.items():
        if field_id not in metadata_fields:
            raise ValidationError(f"Custom field '{field_id}' is not editable for issue {artifact.issue_key}.")
        fields[field_id] = value

    for clear_name in artifact.clear_fields:
        if clear_name in {
            "summary",
            "description",
            "fix_versions",
            "labels",
            "components",
            "priority",
            "assignee",
            "reporter",
            "parent_issue",
            "parent_epic",
            "work_type",
        }:
            field_id = {
                "fix_versions": "fixVersions",
                "parent_issue": "parent",
                "labels": "labels",
                "components": "components",
                "priority": "priority",
                "assignee": "assignee",
                "reporter": "reporter",
                "summary": "summary",
                "description": "description",
            }.get(clear_name)
            if field_id is None:
                field_id = _resolve_special_field_id(
                    artifact=artifact,
                    metadata_fields=metadata_fields,
                    field_name=clear_name,
                )
        else:
            field_id = clear_name

        if field_id not in metadata_fields and field_id != "description":
            raise ValidationError(f"Field '{clear_name}' is not editable for issue {artifact.issue_key}.")

        metadata = metadata_fields.get(field_id, {"id": field_id, "schema": {"type": "string"}})
        fields[field_id] = _resolve_clear_value(field_id, metadata)

    return fields


def _compute_diff(current_fields: dict[str, Any], new_fields: dict[str, Any]) -> dict[str, Any]:
    diff: dict[str, Any] = {}
    for field_id, new_value in new_fields.items():
        diff[field_id] = {
            "before": current_fields.get(field_id),
            "after": new_value,
        }
    return diff


def _enrich_create_preview(
    preview: MutationPreview,
    client: JiraClient,
    description_adf: dict[str, Any],
) -> None:
    artifact = preview.artifact
    issue_types = client.get_create_issue_types(artifact.project or "")
    issue_type = _find_issue_type_by_name(issue_types, artifact.issue_type or "")
    if issue_type is None:
        preview.live_errors.append(
            f"Issue type '{artifact.issue_type}' is not available for project '{artifact.project}'."
        )
        return

    issue_type_id = str(issue_type.get("id"))
    preview.resolved_issue_type_id = issue_type_id
    metadata_fields = _normalize_metadata_fields(
        client.get_create_field_metadata(artifact.project or "", issue_type_id)
    )
    try:
        preview.jira_fields, warnings = _resolve_create_fields(
            artifact, metadata_fields, issue_type_id, description_adf
        )
        preview.live_warnings.extend(warnings)
        preview.pending_live_resolution.clear()
    except ValidationError as exc:
        preview.live_errors.append(str(exc))


def _enrich_update_preview(
    preview: MutationPreview,
    client: JiraClient,
    description_adf: dict[str, Any],
) -> None:
    artifact = preview.artifact
    issue = client.get_issue(artifact.issue_key or "")
    preview.target_issue_summary = issue.get("fields", {}).get("summary")
    metadata_fields = _normalize_metadata_fields(client.get_edit_metadata(artifact.issue_key or ""))
    try:
        preview.jira_fields = _resolve_update_fields(artifact, metadata_fields, description_adf)
        preview.pending_live_resolution.clear()
        preview.diff = _compute_diff(issue.get("fields", {}), preview.jira_fields)
    except ValidationError as exc:
        preview.live_errors.append(str(exc))


def _enrich_comment_preview(preview: MutationPreview, client: JiraClient) -> None:
    issue = client.get_issue(preview.artifact.issue_key or "")
    preview.target_issue_summary = issue.get("fields", {}).get("summary")


def validate_artifact(path: str | Path) -> dict[str, Any]:
    artifact = load_artifact(path)
    return {
        "ok": True,
        "artifact": artifact.to_summary(),
        "local_errors": [],
        "local_warnings": [],
    }


def preview_artifact(path: str | Path, client: JiraClient | None = None) -> dict[str, Any]:
    artifact = load_artifact(path)
    preview = build_preview(artifact, client=client)
    return preview.as_dict()


def apply_artifact(path: str | Path, client: JiraClient) -> dict[str, Any]:
    artifact = load_artifact(path)
    preview = build_preview(artifact, client=client)
    if not preview.ok:
        raise ValidationError("Artifact failed validation and cannot be applied.")

    result: dict[str, Any]
    if artifact.action == "create":
        result = client.create_issue(preview.jira_fields)
    elif artifact.action == "update":
        result = client.update_issue(artifact.issue_key or "", preview.jira_fields)
    else:
        result = client.add_comment(artifact.issue_key or "", preview.jira_comment_body or adf_doc([]))

    payload = preview.as_dict()
    payload["result"] = result
    return payload


def _emit_json(payload: dict[str, Any]) -> int:
    sys.stdout.write(json.dumps(payload, indent=2))
    sys.stdout.write("\n")
    return 0


def _handle_command(command: str, path: str) -> int:
    try:
        if command == "validate":
            return _emit_json(validate_artifact(path))

        client = None
        if command in {"preview", "apply"} and all(os.getenv(name) for name in ENV_VARS):
            client = JiraClient.from_env()

        if command == "preview":
            return _emit_json(preview_artifact(path, client=client))

        if client is None:
            raise ValidationError(
                "Jira apply requires JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN."
            )
        return _emit_json(apply_artifact(path, client=client))

    except JiraApiError as exc:
        return _emit_json(
            {
                "ok": False,
                "error": str(exc),
                "status_code": exc.status_code,
                "response_body": exc.body,
            }
        )
    except JiraLoaderError as exc:
        return _emit_json({"ok": False, "error": str(exc)})


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and execute Jira markdown artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("validate", "preview", "apply"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("file", help="Path to the markdown artifact.")

    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    return _handle_command(args.command, args.file)


if __name__ == "__main__":
    raise SystemExit(main())
