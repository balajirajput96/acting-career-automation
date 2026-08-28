import { readFileSync, writeFileSync, appendFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repo = resolve(new URL('../../', import.meta.url).pathname);
const production = resolve(repo, 'production_3000');
const now = new Date().toISOString();
const ids = {
  video: '1eoY7RgmmFiH-JbGa1bYLYjRxv1IjTkOH',
  metadata: '1ZKJF19hd5wectMPsvkmcyAK3pJByt44E',
  sourceLedger: '1OWrkcMVjDrb3SoYGmHpqlStmR3S-gsuD',
  qualityControl: '1ziwlMf26ly5pi54qjPGB8doBsUKdY9nK',
  visualAsset: '1F4FOjp8b2OSj3n2Csh6pe7PNCBPYmloa'
};

const metadataPath = resolve(production, 'video_projects/reel-0005-attention-transitions/metadata.json');
const metadata = JSON.parse(readFileSync(metadataPath, 'utf8'));
metadata.status = 'COMPLETED_DRIVE_VERIFIED';
metadata.drive = {
  ...metadata.drive,
  upload_verified: true,
  video_file_id: ids.video,
  metadata_file_id: ids.metadata,
  source_ledger_file_id: ids.sourceLedger,
  quality_control_file_id: ids.qualityControl,
  visual_asset_file_id: ids.visualAsset,
  video_md5: 'c5411a18bc522e9440bec3d58e557da3',
  video_size_bytes: 4056499,
  visual_asset_md5: '662821c9dd4545f591c820d84b4fdde7',
  visual_asset_size_bytes: 3975041,
  verified_at: now
};
metadata.completed_at = now;
writeFileSync(metadataPath, `${JSON.stringify(metadata, null, 2)}\n`);

const masterPath = resolve(production, 'progress/MASTER_PROGRESS.json');
const master = JSON.parse(readFileSync(masterPath, 'utf8'));
for (const key of ['source_verified', 'scripted', 'rendered', 'qc_passed', 'drive_uploaded_verified', 'completed']) master.counts[key] = 5;
master.counts.planned = 2995;
master.current_reel = 'Reel_0006';
master.last_updated = now;
master.latest_completion = {
  reel_id: 'Reel_0005',
  status: 'COMPLETED_DRIVE_VERIFIED',
  batch_id: 'Batch_001',
  canonical_drive_root_id: master.canonical_drive.folder_id,
  drive_video_file_id: ids.video,
  verified_at: now,
  recovery_note: 'Recovered project runtime directory/version setup; two-segment 24-fps one-worker low-memory render; no public post requested'
};
writeFileSync(masterPath, `${JSON.stringify(master, null, 2)}\n`);

const catalogPath = resolve(production, 'catalog/REEL_CATALOG.jsonl');
const catalog = readFileSync(catalogPath, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
const reel = catalog.find((item) => item.reel_id === 'Reel_0005');
if (!reel) throw new Error('Reel_0005 missing from catalog');
Object.assign(reel, {
  status: 'COMPLETED_DRIVE_VERIFIED', drive_upload_verified: true,
  drive_video_file_id: ids.video, drive_metadata_file_id: ids.metadata,
  drive_source_ledger_file_id: ids.sourceLedger, drive_quality_control_file_id: ids.qualityControl,
  drive_visual_asset_file_id: ids.visualAsset, completed_at: now, public_post_status: 'NOT_REQUESTED'
});
writeFileSync(catalogPath, `${catalog.map((item) => JSON.stringify(item)).join('\n')}\n`);

const batchPath = resolve(production, 'catalog/Batch_001.json');
const batch = JSON.parse(readFileSync(batchPath, 'utf8'));
const batchReel = batch.reels.find((item) => item.reel_id === 'Reel_0005');
if (!batchReel) throw new Error('Reel_0005 missing from Batch_001');
Object.assign(batchReel, {
  status: 'COMPLETED_DRIVE_VERIFIED', drive_upload_verified: true,
  drive_video_file_id: ids.video, drive_metadata_file_id: ids.metadata,
  drive_source_ledger_file_id: ids.sourceLedger, drive_quality_control_file_id: ids.qualityControl,
  drive_visual_asset_file_id: ids.visualAsset, completed_at: now, public_post_status: 'NOT_REQUESTED'
});
batch.last_updated = now;
writeFileSync(batchPath, `${JSON.stringify(batch, null, 2)}\n`);

const retryPath = resolve(production, 'progress/ERROR_RETRY_LOG.md');
appendFileSync(retryPath, `\n## ${now} — Reel_0005 recovered setup and low-memory completion\n\nThe production project initially lacked an assets/js directory and requested an unavailable HyperFrames release; both setup faults were corrected before the final quality gate. A permitted Hindi word-timing transcription attempt yielded no usable output, so scene-level time-locked captions were retained and that limitation is recorded in audio_meta.json. Two self-contained 24-fps one-worker low-memory renders were re-encoded into the final 60.032-second H.264/AAC MP4. Canonical Drive parent, file ID, size, MD5, and non-trashed state were verified. No retry remains queued.\n`);

const auditPath = resolve(repo, 'data/automation_run_records.jsonl');
appendFileSync(auditPath, `${JSON.stringify({
  timestamp: now, repository: 'balajirajput96/acting-career-automation',
  task: 'bounded_casting_and_production_3000_reel_0005_cycle',
  tools: 'public_casting_source_review,peer_reviewed_research,native_tts,native_image,hyperframes_segmented_low_memory_render,ffprobe,gws_drive',
  action: 'Screened four public casting sources without outreach; created, QC-checked, and canonical-Drive-verified one faceless Hindi research Reel on attention during task transitions, including source ledger, editable project metadata, QC record, and MP4',
  result: 'completed_drive_verified_no_actionable_casting_match', reel_id: 'Reel_0005', drive_root: master.canonical_drive.folder_id,
  drive_video_file_id: ids.video, public_post_status: 'NOT_REQUESTED',
  failure_category: 'recovered_setup_and_caption_timing_limit', recovery_attempt: 'Created missing local asset runtime directory, aligned to the available renderer release, retained time-locked scene captions after no usable Hindi word-timing output, and rendered in two 24-fps one-worker low-memory segments',
  validation_status: 'casting_4_sources_within_10_run_cap_and_20_day_cap; source_ledger_verified; html_lint_zero_errors; hyperframes_check_runtime_layout_motion_contrast_passed_21_of_21; mp4_60.032s_h264_aac_1080x1920_verified; canonical_drive_upload_and_checksum_verified',
  remaining_blocker: 'Casting preparation remains gated by verified factual profile materials and role fit; public social posting remains excluded without a separate exact destination, caption, and action-specific confirmation', credential_material: 'none'
})}\n`);

console.log(JSON.stringify({ now, next_reel: master.current_reel, completed: master.counts.completed, ids }, null, 2));
