import pytest
from unittest.mock import patch
from validate_video_queue import validate_video_queue


class MockPath:
    def __init__(self, name):
        self.name = name

    def read_text(self, encoding="utf-8"):
        return self.content

    def __lt__(self, other):
        return self.name < other.name


def create_mock_path(name, content):
    p = MockPath(name)
    p.content = content
    return p


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
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=False):
            with patch("pathlib.Path.glob", return_value=[mock_pkg]):
                validate_video_queue()


def test_validate_video_queue_missing_marker():
    mock_pkg = create_mock_path("2024-01-01_test.md", "Missing markers")
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.glob", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()


def test_validate_video_queue_missing_http():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.glob", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()


def test_validate_video_queue_published():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.glob", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()


def test_validate_video_queue_batch_wrong_len():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob", side_effect=[[mock_pkg], [mock_pkg]]
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_missing_marker():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )
    mock_batch = create_mock_path("batch.md", "Missing marker")
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob",
                side_effect=[[mock_pkg], [mock_batch] * 50],
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_missing_http():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )
    mock_batch = create_mock_path(
        "batch.md",
        "INTERNAL REVIEW ONLY\n" "Source\n" "Script\n" "Scene\n" "Caption\n",
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob",
                side_effect=[[mock_pkg], [mock_batch] * 50],
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_not_posted():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )
    mock_batch = create_mock_path(
        "batch.md",
        "INTERNAL REVIEW ONLY\n"
        "Source\n"
        "Script\n"
        "Scene\n"
        "Caption\n"
        "http://example.com\n",
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob",
                side_effect=[[mock_pkg], [mock_batch] * 50],
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_success():
    mock_pkg = create_mock_path(
        "2024-01-01_test.md",
        "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n"
        "## Source Ledger\nhttp://example.com\n"
        "## Narration Script\n## Scene Plan\n## Caption Plan\n"
        "## Asset and Identity Checklist\n## Review Queue Metadata\n",
    )
    mock_batch = create_mock_path(
        "batch.md",
        "INTERNAL REVIEW ONLY\n"
        "Source\n"
        "Script\n"
        "Scene\n"
        "Caption\n"
        "http://example.com\n"
        "NOT POSTED\n",
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob",
                side_effect=[[mock_pkg], [mock_batch] * 50],
            ):
                validate_video_queue()
