"""Validate internal educational-video review packages without generating or publishing media."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE_DIR = ROOT / "educational_video_queue"
REQUIRED_MARKERS = (
    "**Status:** `READY FOR INTERNAL ASSET REVIEW — NOT PUBLISHED`",
    "## Source Ledger",
    "## Narration Script",
    "## Scene Plan",
    "## Caption Plan",
    "## Asset and Identity Checklist",
    "## Review Queue Metadata",
)
PROHIBITED_READY_STATE = "PUBLISHED"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_video_queue() -> None:
    if not QUEUE_DIR.is_dir():
        fail("Missing educational_video_queue directory")

    packages = sorted(QUEUE_DIR.glob("*.md"))
    if not packages:
        fail("No internal educational-video review package found")

    for package in packages:
        content = package.read_text(encoding="utf-8")
        missing = [marker for marker in REQUIRED_MARKERS if marker not in content]
        if missing:
            fail(f"{package.name} is missing required sections: {', '.join(missing)}")
        if "http" not in content:
            fail(f"{package.name} has no source URL in its research ledger")
        if "NOT PUBLISHED" not in content or PROHIBITED_READY_STATE in content.replace(
            "NOT PUBLISHED", ""
        ):
            fail(f"{package.name} does not preserve the internal-review publishing boundary")


if __name__ == "__main__":
    validate_video_queue()
    print("PASS: Internal educational-video review packages are complete and not published.")
