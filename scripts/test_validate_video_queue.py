import pytest
from unittest.mock import patch, MagicMock
from validate_video_queue import validate_video_queue

def test_validate_video_queue_missing_dir():
    with patch("pathlib.Path.is_dir", return_value=False):
        with pytest.raises(SystemExit):
            validate_video_queue()

def test_validate_video_queue_no_packages():
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.glob", return_value=[]):
            with pytest.raises(SystemExit):
                validate_video_queue()

def test_validate_video_queue_success():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )

    # We need to make them sortable by ensuring they return comparable values or just override sorted
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=False):
            with patch("builtins.sorted", return_value=[mock_pkg]):
                validate_video_queue()

def test_validate_video_queue_missing_marker():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = "Missing markers"
    with patch("pathlib.Path.is_dir", return_value=True):
         with patch("builtins.sorted", return_value=[mock_pkg]):
             with pytest.raises(SystemExit):
                 validate_video_queue()
