# Scheduled Automation Contract

The `Daily Casting and Educational Video Desk` schedule is active at **05:58 Asia/Kolkata** in `full_auto` mode. Its 3,000-reel continuation cycle is bounded to **one fully completed Reel per run**. A Reel is complete only after the source ledger, Hindi-first script, faceless 60-second 9:16 render, quality checks, canonical Drive upload, remote file-ID/checksum verification, and local progress updates have all completed.

The schedule must read `progress/MASTER_PROGRESS.json` first and write only to canonical Drive root `1s8HhWxw2k1n57lhMyLmIT30Ln6y8rnc4`. The duplicate root `1vYLRarvedtfaYzNcINGKpKAeeFaz0OnD` is preserved and excluded from new writes. An incomplete or failed attempt goes to the retry/error state before the next catalog slot is considered.

The recurring task also retains its bounded casting-research controls: at most 10 sources per run and 20 per day; only public, official, clear-route opportunities may be shortlisted; no automatic submissions or communications are allowed.

> Google Drive upload is a required internal completion step. Public social publication is not part of automatic completion. Facebook or Instagram requires the exact destination account, final caption, and action-specific confirmation at the time of posting.

## Render recovery rule

If a full-length local render fails or is interrupted under memory pressure, the run must not mark the Reel complete and must not start another slot. Preserve the source project and QC artifacts, record the failure in `progress/ERROR_RETRY_LOG.md`, then retry the same Reel using a deterministic low-memory fallback: one worker, 24 fps, short editable segments, final timestamp-safe re-encode, full integrity check, and canonical Drive verification. Only after that complete verification may the catalog advance.
