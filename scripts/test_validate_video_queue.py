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

def test_validate_video_queue_no_http():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("builtins.sorted", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()

def test_validate_video_queue_published():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "PUBLISHED"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("builtins.sorted", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()

def test_validate_video_queue_batch_count_mismatch():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            # sorted will be called multiple times.
            # 1. First time for packages in QUEUE_DIR. glob(PRIMARY_PATTERN)
            # 2. Second time for packages in BATCH_DIR. glob("*.md")
            def fake_sorted(iterable):
                items = list(iterable)
                # If we're sorting glob("*.md") yielding [mock_pkg]
                return items if items else [mock_pkg]
            with patch("builtins.sorted", side_effect=fake_sorted):
                # We need to simulate that glob on BATCH_DIR returns fewer than 50
                with patch("pathlib.Path.glob", side_effect=[[mock_pkg], [mock_pkg]]):
                    with pytest.raises(SystemExit):
                        validate_video_queue()

def test_validate_video_queue_batch_success():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )

    batch_pkg = MagicMock()
    batch_pkg.name = "test_batch.md"
    batch_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\n"
        "Source http://example.com\n"
        "Script Scene Caption\n"
        "NOT POSTED\n"
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            def fake_sorted(iterable):
                items = list(iterable)
                return items
            with patch("builtins.sorted", side_effect=fake_sorted):
                with patch("pathlib.Path.glob", side_effect=[[mock_pkg], [batch_pkg] * 50]):
                    validate_video_queue()

def test_validate_video_queue_batch_missing_marker():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )

    batch_pkg = MagicMock()
    batch_pkg.name = "test_batch.md"
    batch_pkg.read_text.return_value = "Missing batch markers"

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            def fake_sorted(iterable):
                items = list(iterable)
                return items
            with patch("builtins.sorted", side_effect=fake_sorted):
                with patch("pathlib.Path.glob", side_effect=[[mock_pkg], [batch_pkg] * 50]):
                    with pytest.raises(SystemExit):
                        validate_video_queue()

def test_validate_video_queue_batch_no_http():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )

    batch_pkg = MagicMock()
    batch_pkg.name = "test_batch.md"
    batch_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\n"
        "Source Script Scene Caption\n"
        "NOT POSTED\n"
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            def fake_sorted(iterable):
                items = list(iterable)
                return items
            with patch("builtins.sorted", side_effect=fake_sorted):
                with patch("pathlib.Path.glob", side_effect=[[mock_pkg], [batch_pkg] * 50]):
                    with pytest.raises(SystemExit):
                        validate_video_queue()

def test_validate_video_queue_batch_published():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n"
    )

    batch_pkg = MagicMock()
    batch_pkg.name = "test_batch.md"
    batch_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\n"
        "Source http://example.com\n"
        "Script Scene Caption\n"
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            def fake_sorted(iterable):
                items = list(iterable)
                return items
            with patch("builtins.sorted", side_effect=fake_sorted):
                with patch("pathlib.Path.glob", side_effect=[[mock_pkg], [batch_pkg] * 50]):
                    with pytest.raises(SystemExit):
                        validate_video_queue()
