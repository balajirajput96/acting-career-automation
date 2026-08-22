# Daily Continuation Playbook

Each continuation cycle first reads `MASTER_PROGRESS.json` and the catalog row for the next unfinished Reel. It must not re-create a row whose Drive upload and metadata verification are both complete.

The cycle researches only the current slot, creates a source ledger, labels its evidence category, drafts a Hindi-first 60-second script, generates faceless assets and neutral narration, runs render and visual QC, uploads the MP4 plus metadata to the canonical Drive batch folder, verifies the uploaded file IDs, and only then increments completion counts. A source disagreement, unsafe claim, render issue, or failed upload is written to the retry queue rather than silently skipped.

The public-post stage is outside this cycle. It never publishes automatically: an exact platform, destination account, final caption, and action-specific confirmation are required first.
