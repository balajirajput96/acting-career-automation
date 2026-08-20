"""Validate repository-local acting-career automation inputs without external actions."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from validate_video_queue import validate_video_queue


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEAD_HEADER = [
    "id",
    "date_found",
    "source",
    "project",
    "role",
    "contact_type",
    "contact",
    "status",
    "notes",
]
REQUIRED_FILES = [
    "data/casting_leads.csv",
    "data/casting_leads.sample.csv",
    "templates/email_template.md",
    "templates/dm_template.md",
    "templates/followup_template.md",
    "profile_kit/CHECKLIST.md",
    "GEMINI.md",
    "GEMINI_SPARK_DAILY_READINESS_PROMPT.md",
    "DAILY_OPERATIONS_PROFILE.md",
    "DAILY_EDUCATIONAL_VIDEO_PIPELINE.md",
    "APPLICATION_READINESS_ASSESSMENT.md",
    "JULES_DAILY_MAINTENANCE_PROMPT.md",
    "CLI_AND_JULES_AUTOMATION_MANIFEST.md",
    "AUTOMATION_AUDIT_INVENTORY.md",
    "data/automation_run_records.jsonl",
    ".agents/agents/acting-automation-operator/agent.md",
    ".gemini/commands/acting/status.toml",
    ".gemini/commands/acting/plan.toml",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail(f"Missing required toolkit files: {', '.join(missing)}")


def validate_lead_header() -> None:
    csv_path = ROOT / "data" / "casting_leads.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle), [])
    if header != EXPECTED_LEAD_HEADER:
        fail(f"Unexpected casting_leads.csv header: {header!r}")


def validate_templates() -> None:
    email_template = (ROOT / "templates" / "email_template.md").read_text(encoding="utf-8")
    required_placeholders = ("{{name}}", "{{role}}", "{{source}}", "{{project}}")
    missing = [placeholder for placeholder in required_placeholders if placeholder not in email_template]
    if missing:
        fail(f"Email template is missing placeholders: {', '.join(missing)}")


def validate_execution_records() -> None:
    records_path = ROOT / "data" / "automation_run_records.jsonl"
    required_keys = {
        "timestamp",
        "repository",
        "task",
        "tools",
        "action",
        "result",
        "failure_category",
        "recovery_attempt",
        "validation_status",
        "remaining_blocker",
    }
    lines = [line for line in records_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        fail("automation_run_records.jsonl must contain at least one record")
    for number, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            fail(f"Invalid JSON in automation_run_records.jsonl line {number}: {error.msg}")
        missing = sorted(required_keys - set(record))
        if missing:
            fail(f"Automation run record line {number} is missing keys: {', '.join(missing)}")


def main() -> None:
    validate_required_files()
    validate_lead_header()
    validate_templates()
    validate_execution_records()
    validate_video_queue()
    print("PASS: Toolkit files, lead schema, templates, and internal AI workflow assets are valid.")


if __name__ == "__main__":
    main()
