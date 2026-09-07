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


def test_validate_video_queue_batch_success():
    mock_pkg = MagicMock()
    mock_pkg.name = "batch_01.md"
    mock_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\n"
        "Source: http://example.com\n"
        "Script details\n"
        "Scene notes\n"
        "Caption text\n"
        "NOT POSTED\n"
    )

    batch_pkgs = [mock_pkg] * 50

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch(
            "builtins.sorted",
            side_effect=[
                [
                    MagicMock(
                        name="2024-01-01_test.md",
                        read_text=MagicMock(
                            return_value="**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n## Source Ledger\nhttp://example.com\n## Narration Script\n## Scene Plan\n## Caption Plan\n## Asset and Identity Checklist\n## Review Queue Metadata\n"
                        ),
                    )
                ],
                batch_pkgs,
            ],
        ):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("pathlib.Path.glob", return_value=batch_pkgs):
                    validate_video_queue()


def test_validate_video_queue_batch_wrong_length():
    batch_pkgs = [MagicMock()] * 49
    with patch("pathlib.Path.is_dir", return_value=True):
        with patch(
            "builtins.sorted",
            side_effect=[
                [
                    MagicMock(
                        name="2024-01-01_test.md",
                        read_text=MagicMock(
                            return_value="**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n## Source Ledger\nhttp://example.com\n## Narration Script\n## Scene Plan\n## Caption Plan\n## Asset and Identity Checklist\n## Review Queue Metadata\n"
                        ),
                    )
                ],
                batch_pkgs,
            ],
        ):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("pathlib.Path.glob", return_value=batch_pkgs):
                    with pytest.raises(SystemExit):
                        validate_video_queue()


def test_validate_video_queue_batch_missing_markers():
    mock_pkg = MagicMock()
    mock_pkg.name = "batch_01.md"
    mock_pkg.read_text.return_value = "Missing markers"
    batch_pkgs = [mock_pkg] * 50

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch(
            "builtins.sorted",
            side_effect=[
                [
                    MagicMock(
                        name="2024-01-01_test.md",
                        read_text=MagicMock(
                            return_value="**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n## Source Ledger\nhttp://example.com\n## Narration Script\n## Scene Plan\n## Caption Plan\n## Asset and Identity Checklist\n## Review Queue Metadata\n"
                        ),
                    )
                ],
                batch_pkgs,
            ],
        ):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("pathlib.Path.glob", return_value=batch_pkgs):
                    with pytest.raises(SystemExit):
                        validate_video_queue()


def test_validate_video_queue_batch_missing_http():
    mock_pkg = MagicMock()
    mock_pkg.name = "batch_01.md"
    mock_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\n"
        "Source: \n"
        "Script details\n"
        "Scene notes\n"
        "Caption text\n"
        "NOT POSTED\n"
    )
    batch_pkgs = [mock_pkg] * 50

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch(
            "builtins.sorted",
            side_effect=[
                [
                    MagicMock(
                        name="2024-01-01_test.md",
                        read_text=MagicMock(
                            return_value="**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n## Source Ledger\nhttp://example.com\n## Narration Script\n## Scene Plan\n## Caption Plan\n## Asset and Identity Checklist\n## Review Queue Metadata\n"
                        ),
                    )
                ],
                batch_pkgs,
            ],
        ):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("pathlib.Path.glob", return_value=batch_pkgs):
                    with pytest.raises(SystemExit):
                        validate_video_queue()


def test_validate_video_queue_batch_published():
    mock_pkg = MagicMock()
    mock_pkg.name = "batch_01.md"
    mock_pkg.read_text.return_value = (
        "INTERNAL REVIEW ONLY\n"
        "Source: http://example.com\n"
        "Script details\n"
        "Scene notes\n"
        "Caption text\n"
    )  # Missing NOT POSTED
    batch_pkgs = [mock_pkg] * 50

    with patch("pathlib.Path.is_dir", return_value=True):
        with patch(
            "builtins.sorted",
            side_effect=[
                [
                    MagicMock(
                        name="2024-01-01_test.md",
                        read_text=MagicMock(
                            return_value="**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`\n## Source Ledger\nhttp://example.com\n## Narration Script\n## Scene Plan\n## Caption Plan\n## Asset and Identity Checklist\n## Review Queue Metadata\n"
                        ),
                    )
                ],
                batch_pkgs,
            ],
        ):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("pathlib.Path.glob", return_value=batch_pkgs):
                    with pytest.raises(SystemExit):
                        validate_video_queue()



def test_validate_video_queue_main():
    with patch("validate_video_queue.validate_video_queue") as mock_validate:
        with patch("builtins.print") as mock_print:
            import runpy
            with patch("sys.argv", ["validate_video_queue.py"]):
                try:
                    runpy.run_path("scripts/validate_video_queue.py", run_name="__main__")
                except SystemExit:
                    pass # may exit 1 because of actual files, we just care that it executes
