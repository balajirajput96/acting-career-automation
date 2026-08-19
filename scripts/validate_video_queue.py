"""Validate internal educational-video review packages without generating or publishing media."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE_DIR = ROOT / "educational_video_queue"
PRIMARY_PATTERN = "20??-??-??_*.md"
BATCH_DIR = QUEUE_DIR / "batch_50"
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
BATCH_MARKERS = (
    "INTERNAL REVIEW ONLY",
    "Source",
    "Script",
    "Scene",
    "Caption",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_video_queue() -> None:
    if not QUEUE_DIR.is_dir():
        fail("Missing educational_video_queue directory")

    packages = sorted(QUEUE_DIR.glob(PRIMARY_PATTERN))
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

    if BATCH_DIR.exists():
        batch_packages = sorted(
            package for package in BATCH_DIR.glob("*.md") if package.name != "INDEX.md"
        )
        if len(batch_packages) != 50:
            fail(f"Expected 50 batch review packages; found {len(batch_packages)}")
        for package in batch_packages:
            content = package.read_text(encoding="utf-8")
            missing = [marker for marker in BATCH_MARKERS if marker not in content]
            if missing:
                fail(f"{package.name} is missing batch markers: {', '.join(missing)}")
            if "http" not in content:
                fail(f"{package.name} has no authoritative source URL")
            if "INTERNAL REVIEW ONLY" not in content or "NOT POSTED" not in content:
                fail(f"{package.name} does not preserve the batch internal-review boundary")


if __name__ == "__main__":
    validate_video_queue()
    print("PASS: Internal educational-video review packages are complete and not published.")
