# Workspace Studio Internal Material Flow

## Flow Goal

Create an internal-only flow that reads an agreed Drive folder and a Sheets tracker, identifies required material gaps, and writes a readiness summary to an internal Sheet or Doc.

## Allowed Steps

1. Read the internal actor-material folder metadata.
2. Read the internal lead/shortlist sheet.
3. Compare each verified opportunity’s requirements against the available material metadata.
4. Create or update an internal readiness row with missing items and deadline information.
5. Generate an internal summary for review.

## Prohibited Steps

The flow must not email recipients, send DMs, share Drive files externally, complete forms, publish media, pay fees, or change public account settings.

## Scheduling Guidance

Run once daily after the Gemini Spark readiness task or use a manual trigger until the selected Workspace account and Drive/Sheet locations are confirmed.
