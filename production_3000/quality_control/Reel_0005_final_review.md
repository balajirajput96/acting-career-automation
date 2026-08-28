# Reel_0005 Quality-Control Record

**Status:** QC passed; canonical Drive upload verification pending.

| Gate | Result | Evidence |
|---|---|---|
| Source scope | Pass | Source ledger classifies the framework, laboratory result, contextual explainer, and limits. No diagnosis, treatment, numeric productivity, or universal-causation claim is used. |
| Format | Pass | Editable root composition specifies 1080×1920 portrait, 24 fps, and 60 seconds. |
| Voice policy | Pass | Native `generate_speech` created a 58.8-second mono 24 kHz WAV with the neutral synthetic Charon voice; no face or user-authorized personal voice asset is used. |
| Visual policy | Pass | Original faceless generated visual is staged as the only external visual plate and is listed in the media manifest. |
| Structural lint | Pass with non-blocking advisory | Zero errors; one `timeline_track_too_dense` warning because eight sequential clips are authored in one self-contained file. Low-memory output is split before rendering. |
| Runtime / layout / motion / contrast | Pass | `hyperframes check --snapshots --samples 12 --at-transitions` returned zero errors. Runtime, layout, motion, and contrast all passed; the contrast check passed 21/21 inspected samples. |
| Full contact-sheet review | Pass | Eight targeted scene midpoints at 4, 11, 18, 25, 34, 44, 53, and 58 seconds show the generated faceless hero, the three-part attention framework, task-transition diagram, laboratory comparison, scope card, and final disclaimer. Hindi-first headline/caption text is readable against the dark ground. |
| Segmented render | Pass | Two self-contained segments rendered at 24 fps with one worker, forced low-memory mode, screenshot capture, and frame cache disabled. |
| Final MP4 integrity | Pass | Timestamp-safe FFmpeg re-encode produced `reel-0005-attention-transitions.mp4`: 1080×1920, 24 fps, H.264 video, AAC audio at 48 kHz/2 channels, 60.032 seconds, 4,056,499 bytes, MD5 `c5411a18bc522e9440bec3d58e557da3`. |

## Recovery note

The project initially lacked an `assets/js` directory and specified an unavailable renderer version. Both setup issues were repaired before final checks: the reusable local GSAP runtime was staged, and the project was aligned to the available `hyperframes@0.8.16` release. Installation then required standard local post-install hooks for already declared renderer dependencies; those completed successfully. A permitted word-level transcription attempt returned no usable Hindi timing output, so the final package retains time-locked scene captions and transparently records that limitation in `audio_meta.json`.

## Render acceptance criteria

The final artifact must remain one 1080×1920 H.264/AAC MP4 of approximately 60 seconds; retain audible Hindi narration; contain no user face or personal voice; pass ffprobe integrity checks; and be verified in the canonical Drive Batch_001 folder with checksum, parent, and non-trashed status before completion is recorded.
