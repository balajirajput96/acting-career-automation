import pytest
from unittest.mock import patch, mock_open
from validate_toolkit import (
    validate_required_files,
    validate_lead_header,
    validate_templates,
    validate_execution_records
)

def test_validate_required_files_success():
    with patch("pathlib.Path.is_file", return_value=True):
        validate_required_files()

def test_validate_required_files_failure():
    with patch("pathlib.Path.is_file", return_value=False):
        with pytest.raises(SystemExit):
            validate_required_files()

def test_validate_lead_header_success():
    valid_header = "id,date_found,source,project,role,contact_type,contact,status,notes\n"
    with patch("pathlib.Path.open", mock_open(read_data=valid_header)):
        validate_lead_header()

def test_validate_lead_header_failure():
    invalid_header = "id,date_found,source\n"
    with patch("pathlib.Path.open", mock_open(read_data=invalid_header)):
        with pytest.raises(SystemExit):
            validate_lead_header()

def test_validate_templates_success():
    template = "Hello {{name}}, role {{role}}, source {{source}}, project {{project}}"
    with patch("pathlib.Path.read_text", return_value=template):
        validate_templates()

def test_validate_templates_failure():
    template = "Hello {{name}}"
    with patch("pathlib.Path.read_text", return_value=template):
        with pytest.raises(SystemExit):
            validate_templates()

def test_validate_execution_records_success():
    valid_record = '{"timestamp": "1", "repository": "1", "task": "1", "tools": "1", "action": "1", "result": "1", "failure_category": "1", "recovery_attempt": "1", "validation_status": "1", "remaining_blocker": "1"}\n'
    with patch("pathlib.Path.read_text", return_value=valid_record):
        validate_execution_records()

def test_validate_execution_records_empty_failure():
    with patch("pathlib.Path.read_text", return_value=""):
        with pytest.raises(SystemExit):
            validate_execution_records()

def test_validate_execution_records_invalid_json_failure():
    with patch("pathlib.Path.read_text", return_value="not json"):
        with pytest.raises(SystemExit):
            validate_execution_records()

def test_validate_execution_records_missing_keys_failure():
    invalid_record = '{"timestamp": "1"}\n'
    with patch("pathlib.Path.read_text", return_value=invalid_record):
        with pytest.raises(SystemExit):
            validate_execution_records()
