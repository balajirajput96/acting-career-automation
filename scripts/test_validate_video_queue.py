import pytest
from unittest.mock import patch, MagicMock

try:
    from validate_video_queue import validate_video_queue, REQUIRED_MARKERS
except ModuleNotFoundError:
    from scripts.validate_video_queue import (
        validate_video_queue,
        REQUIRED_MARKERS,
    )


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


def test_validate_video_queue_missing_url():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nNo URL here"
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("builtins.sorted", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()


def test_validate_video_queue_published():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nhttp://example.com\nPUBLISHED"
    )
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("builtins.sorted", return_value=[mock_pkg]):
            with pytest.raises(SystemExit):
                validate_video_queue()


def test_validate_video_queue_batch_wrong_length():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nhttp://example.com"
    )

    mock_batch_pkg = MagicMock()
    mock_batch_pkg.name = "batch_test.md"

    # Needs to fail because there are not 50
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            # First sorted is for packages, second is for batch packages inside the generator
            with patch(
                "builtins.sorted", side_effect=[[mock_pkg], [mock_batch_pkg]]
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_missing_markers():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nhttp://example.com"
    )

    mock_batch_pkg = MagicMock()
    mock_batch_pkg.name = "batch_test.md"
    mock_batch_pkg.read_text.return_value = "Missing batch markers"

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "builtins.sorted",
                side_effect=[[mock_pkg], [mock_batch_pkg] * 50],
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_missing_url():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nhttp://example.com"
    )

    mock_batch_pkg = MagicMock()
    mock_batch_pkg.name = "batch_test.md"
    mock_batch_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\nSource\nScript\nScene\nCaption"
    )

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "builtins.sorted",
                side_effect=[[mock_pkg], [mock_batch_pkg] * 50],
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_not_posted():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nhttp://example.com"
    )

    mock_batch_pkg = MagicMock()
    mock_batch_pkg.name = "batch_test.md"
    mock_batch_pkg.read_text.return_value = "INTERNAL REVIEW ONLY\nSource\nScript\nScene\nCaption\nhttp://example.com"

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "builtins.sorted",
                side_effect=[[mock_pkg], [mock_batch_pkg] * 50],
            ):
                with pytest.raises(SystemExit):
                    validate_video_queue()


def test_validate_video_queue_batch_success():
    mock_pkg = MagicMock()
    mock_pkg.name = "2024-01-01_test.md"
    mock_pkg.read_text.return_value = (
        "\n".join(REQUIRED_MARKERS) + "\nhttp://example.com"
    )

    mock_batch_pkg = MagicMock()
    mock_batch_pkg.name = "batch_test.md"
    mock_batch_pkg.read_text.return_value = "INTERNAL REVIEW ONLY\nSource\nScript\nScene\nCaption\nhttp://example.com\nNOT POSTED"

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "builtins.sorted",
                side_effect=[[mock_pkg], [mock_batch_pkg] * 50],
            ):
                validate_video_queue()
