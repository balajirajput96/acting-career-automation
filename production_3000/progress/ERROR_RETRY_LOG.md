# Retry and Error Log

| Timestamp | Run | Stage | State | Recovery / next step |
|---|---|---|---|---|
| 2026-08-22T20:10:42+00:00 | Reel_0002 bounded cycle | Source → render → canonical Drive verification | No unresolved error | Reel completed after local lint/check/preview, MP4 integrity verification, and remote Drive artifact verification. Continue with Reel_0003 only on a later run. |

## 2026-08-25T04:23:17.936Z — Reel_0003 recovery resolved

The initial full low-memory render was interrupted by a sandbox reset under memory pressure. Source assets were restored without overwriting completed records. The recovery strategy used two validated 24-fps low-memory segments, then deterministic final re-encode. Final canonical Drive verification succeeded; no retry remains queued.

## 2026-08-25T04:45:14.285Z — Reel_0004 proactive low-memory completion

Full-timeline rendering was not attempted after the documented environment reset risk. Two self-contained segments passed structural checks, rendered at 24 fps with one worker, were re-encoded into a 60.041667-second final MP4, and passed canonical Drive checksum/parent verification. No retry remains queued.

## 2026-08-28T01:02:14.362Z — Reel_0005 recovered setup and low-memory completion

The production project initially lacked an assets/js directory and requested an unavailable HyperFrames release; both setup faults were corrected before the final quality gate. A permitted Hindi word-timing transcription attempt yielded no usable output, so scene-level time-locked captions were retained and that limitation is recorded in audio_meta.json. Two self-contained 24-fps one-worker low-memory renders were re-encoded into the final 60.032-second H.264/AAC MP4. Canonical Drive parent, file ID, size, MD5, and non-trashed state were verified. No retry remains queued.
