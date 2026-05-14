from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "jira_loader.py"
SPEC = importlib.util.spec_from_file_location("jira_loader", MODULE_PATH)
jira_loader = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = jira_loader
SPEC.loader.exec_module(jira_loader)


class FakeJiraClient:
    def __init__(self) -> None:
        self.created_fields = None
        self.updated_fields = None
        self.comment_body = None

    def get_create_issue_types(self, project_key: str):
        return [
            {"id": "10001", "name": "Task"},
            {"id": "10002", "name": "Story"},
            {"id": "10003", "name": "Bug"},
            {"id": "10004", "name": "Epic"},
            {"id": "10005", "name": "Sub-task"},
        ]

    def get_create_field_metadata(self, project_key: str, issue_type_id: str):
        return {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}},
            "description": {
                "name": "Description",
                "required": False,
                "schema": {"type": "string"},
            },
            "labels": {"name": "Labels", "required": False, "schema": {"type": "array", "items": "string"}},
            "fixVersions": {
                "name": "Fix Versions",
                "required": False,
                "schema": {"type": "array", "items": "version", "system": "fixVersions"},
            },
            "components": {
                "name": "Components",
                "required": False,
                "schema": {"type": "array", "items": "component", "system": "components"},
            },
            "priority": {"name": "Priority", "required": False, "schema": {"type": "priority"}},
            "assignee": {"name": "Assignee", "required": False, "schema": {"type": "user"}},
            "reporter": {"name": "Reporter", "required": False, "schema": {"type": "user"}},
            "customfield_20001": {
                "name": "Work Type",
                "required": False,
                "schema": {"type": "option"},
            },
            "customfield_20002": {
                "name": "Epic Link",
                "required": False,
                "schema": {"type": "string"},
            },
            "customfield_29999": {
                "name": "Custom Flag",
                "required": False,
                "schema": {"type": "string"},
            },
        }

    def get_issue(self, issue_key: str):
        return {
            "key": issue_key,
            "fields": {
                "summary": "Existing summary",
                "labels": ["old-label"],
                "description": {"type": "doc", "version": 1, "content": []},
            },
        }

    def get_edit_metadata(self, issue_key: str):
        return {
            "summary": {"name": "Summary", "schema": {"type": "string"}},
            "description": {"name": "Description", "schema": {"type": "string"}},
            "labels": {"name": "Labels", "schema": {"type": "array", "items": "string"}},
            "priority": {"name": "Priority", "schema": {"type": "priority"}},
            "customfield_20001": {"name": "Work Type", "schema": {"type": "option"}},
            "customfield_29999": {"name": "Custom Flag", "schema": {"type": "string"}},
        }

    def create_issue(self, fields):
        self.created_fields = fields
        return {"key": "TEST-101"}

    def update_issue(self, issue_key: str, fields):
        self.updated_fields = {"issue_key": issue_key, "fields": fields}
        return {}

    def add_comment(self, issue_key: str, body):
        self.comment_body = {"issue_key": issue_key, "body": body}
        return {"id": "9001"}


class JiraLoaderTests(unittest.TestCase):
    def _write_temp_artifact(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "artifact.md"
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
        return path

    def test_all_canonical_templates_validate(self):
        template_dir = SKILL_ROOT / "templates"
        template_names = ["epic.md", "story.md", "task.md", "bug.md", "sub-task.md"]
        for name in template_names:
            with self.subTest(template=name):
                result = jira_loader.validate_artifact(template_dir / name)
                self.assertTrue(result["ok"])

    def test_markdown_to_adf_supports_expected_blocks_and_marks(self):
        markdown = textwrap.dedent(
            """
            # Heading

            This is **bold**, *italic*, a [link](https://example.com), and `code`.

            - First bullet
            - Second bullet

            1. First ordered
            2. Second ordered

            > Quoted text

            ```python
            print("hello")
            ```
            """
        ).strip()

        adf = jira_loader.parse_markdown_to_adf(markdown)
        node_types = [node["type"] for node in adf["content"]]
        self.assertIn("heading", node_types)
        self.assertIn("paragraph", node_types)
        self.assertIn("bulletList", node_types)
        self.assertIn("orderedList", node_types)
        self.assertIn("blockquote", node_types)
        self.assertIn("codeBlock", node_types)

        paragraph = next(node for node in adf["content"] if node["type"] == "paragraph")
        marks = [mark["type"] for item in paragraph["content"] for mark in item.get("marks", [])]
        self.assertIn("strong", marks)
        self.assertIn("em", marks)
        self.assertIn("link", marks)
        self.assertIn("code", marks)

    def test_create_preview_resolves_live_fields(self):
        path = self._write_temp_artifact(
            """
            ---
            schema: jira-create-v1
            project: TEST
            issue_type: Task
            summary: Build loader
            parent_epic: TEST-10
            labels:
              - loader
            fix_versions:
              - 2026.05
            work_type: Feature
            custom_fields:
              customfield_29999: custom value
            ---

            # Objective

            Create the Jira loader.
            """
        )
        client = FakeJiraClient()
        preview = jira_loader.preview_artifact(path, client=client)
        self.assertTrue(preview["ok"])
        self.assertEqual(preview["jira_fields"]["issuetype"]["id"], "10001")
        self.assertEqual(preview["jira_fields"]["customfield_20001"]["value"], "Feature")
        self.assertEqual(preview["jira_fields"]["customfield_20002"], "TEST-10")

    def test_create_preview_fails_when_live_metadata_requires_missing_field(self):
        path = self._write_temp_artifact(
            """
            ---
            schema: jira-create-v1
            project: TEST
            issue_type: Epic
            summary: Missing epic name
            ---

            # Business Objective

            Add a missing field case.
            """
        )

        class RequiredFieldClient(FakeJiraClient):
            def get_create_field_metadata(self, project_key: str, issue_type_id: str):
                fields = super().get_create_field_metadata(project_key, issue_type_id)
                fields["customfield_10011"] = {
                    "name": "Epic Name",
                    "required": True,
                    "schema": {"type": "string"},
                }
                return fields

        preview = jira_loader.preview_artifact(path, client=RequiredFieldClient())
        self.assertFalse(preview["ok"])
        self.assertTrue(
            any("Epic Name" in message for message in preview["live_errors"]),
            preview["live_errors"],
        )

    def test_update_preview_builds_diff_and_clear_fields(self):
        path = self._write_temp_artifact(
            """
            ---
            schema: jira-update-v1
            issue_key: TEST-12
            summary: Updated summary
            labels:
              - refreshed
            clear_fields:
              - work_type
              - customfield_29999
            ---

            # Updated Description

            Replace the description body.
            """
        )
        client = FakeJiraClient()
        preview = jira_loader.preview_artifact(path, client=client)
        self.assertTrue(preview["ok"])
        self.assertIn("summary", preview["diff"])
        self.assertEqual(preview["jira_fields"]["labels"], ["refreshed"])
        self.assertIsNone(preview["jira_fields"]["customfield_20001"])
        self.assertIsNone(preview["jira_fields"]["customfield_29999"])

    def test_comment_apply_sends_adf_body(self):
        path = self._write_temp_artifact(
            """
            ---
            schema: jira-comment-v1
            issue_key: TEST-42
            ---

            This is a **comment**.
            """
        )
        client = FakeJiraClient()
        result = jira_loader.apply_artifact(path, client=client)
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"]["id"], "9001")
        self.assertEqual(client.comment_body["issue_key"], "TEST-42")
        self.assertEqual(client.comment_body["body"]["type"], "doc")

    def test_invalid_custom_field_id_is_rejected(self):
        path = self._write_temp_artifact(
            """
            ---
            schema: jira-create-v1
            project: TEST
            issue_type: Task
            summary: Invalid custom field
            custom_fields:
              Epic Link: TEST-1
            ---

            Body
            """
        )
        with self.assertRaises(jira_loader.ValidationError):
            jira_loader.load_artifact(path)


if __name__ == "__main__":
    unittest.main()
