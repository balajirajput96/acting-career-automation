import { readFileSync, writeFileSync, appendFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repo = resolve(new URL('../../', import.meta.url).pathname);
const production = resolve(repo, 'production_3000');
const now = new Date().toISOString();
const ids = {
  video: '1S5AtsNVhvCkG0Z4Ni9puHkVqh2hJf5P6',
  metadata: '17_jt55Udau4C8ObolK35dFREEEukvjdp',
  sourceLedger: '1UKOkiU0GjH42e1ogjBIFZSnERuxA7Ork',
  qualityControl: '1XtgYxKuiy4i87FXdge33_ehVf0IE6xMx',
  visualAsset: '1qgLa6e_yZSMJBMgEGKPLdkP7hP3qCNiD'
};

const metadataPath = resolve(production, 'video_projects/reel-0004-digital-notifications-focus/metadata.json');
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
  video_md5: 'd43ca9908f8c3625b86cac42cfe75159',
  video_size_bytes: 3982807,
  visual_asset_md5: 'e67a3266d9c85fc2de663d2aac95140c',
  verified_at: now
};
metadata.completed_at = now;
writeFileSync(metadataPath, `${JSON.stringify(metadata, null, 2)}\n`);

const masterPath = resolve(production, 'progress/MASTER_PROGRESS.json');
const master = JSON.parse(readFileSync(masterPath, 'utf8'));
for (const key of ['source_verified', 'scripted', 'rendered', 'qc_passed', 'drive_uploaded_verified', 'completed']) master.counts[key] = 4;
master.counts.planned = 2996;
master.current_reel = 'Reel_0005';
master.last_updated = now;
master.latest_completion = {
  reel_id: 'Reel_0004',
  status: 'COMPLETED_DRIVE_VERIFIED',
  batch_id: 'Batch_001',
  canonical_drive_root_id: master.canonical_drive.folder_id,
  drive_video_file_id: ids.video,
  verified_at: now,
  recovery_note: 'Proactive two-segment, 24-fps, one-worker low-memory render; no public post requested'
};
writeFileSync(masterPath, `${JSON.stringify(master, null, 2)}\n`);

const catalogPath = resolve(production, 'catalog/REEL_CATALOG.jsonl');
const catalog = readFileSync(catalogPath, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
const reel = catalog.find((item) => item.reel_id === 'Reel_0004');
if (!reel) throw new Error('Reel_0004 missing from catalog');
Object.assign(reel, {
  status: 'COMPLETED_DRIVE_VERIFIED', drive_upload_verified: true,
  drive_video_file_id: ids.video, drive_metadata_file_id: ids.metadata,
  drive_source_ledger_file_id: ids.sourceLedger, drive_quality_control_file_id: ids.qualityControl,
  drive_visual_asset_file_id: ids.visualAsset, completed_at: now, public_post_status: 'NOT_REQUESTED'
});
writeFileSync(catalogPath, `${catalog.map((item) => JSON.stringify(item)).join('\n')}\n`);

const batchPath = resolve(production, 'catalog/Batch_001.json');
const batch = JSON.parse(readFileSync(batchPath, 'utf8'));
const batchReel = batch.reels.find((item) => item.reel_id === 'Reel_0004');
if (!batchReel) throw new Error('Reel_0004 missing from Batch_001');
Object.assign(batchReel, {
  status: 'COMPLETED_DRIVE_VERIFIED', drive_upload_verified: true,
  drive_video_file_id: ids.video, drive_metadata_file_id: ids.metadata,
  drive_source_ledger_file_id: ids.sourceLedger, drive_quality_control_file_id: ids.qualityControl,
  drive_visual_asset_file_id: ids.visualAsset, completed_at: now, public_post_status: 'NOT_REQUESTED'
});
batch.last_updated = now;
writeFileSync(batchPath, `${JSON.stringify(batch, null, 2)}\n`);

const retryPath = resolve(production, 'progress/ERROR_RETRY_LOG.md');
appendFileSync(retryPath, `\n## ${now} — Reel_0004 proactive low-memory completion\n\nFull-timeline rendering was not attempted after the documented environment reset risk. Two self-contained segments passed structural checks, rendered at 24 fps with one worker, were re-encoded into a 60.041667-second final MP4, and passed canonical Drive checksum/parent verification. No retry remains queued.\n`);

const auditPath = resolve(repo, 'data/automation_run_records.jsonl');
appendFileSync(auditPath, `${JSON.stringify({
  timestamp: now, repository: 'balajirajput96/acting-career-automation',
  task: 'production_3000_reel_0004_digital_notifications_focus',
  tools: 'peer_reviewed_sources,university_source,native_tts,native_image,hyperframes_segmented_low_memory_render,gws_drive',
  action: 'Created a source-bounded faceless Hindi Reel about notification sounds and attention, completed low-memory render QC, and uploaded all required artifacts only to canonical Drive Batch_001',
  result: 'completed_drive_verified', reel_id: 'Reel_0004', drive_root: master.canonical_drive.folder_id,
  drive_video_file_id: ids.video, public_post_status: 'NOT_REQUESTED',
  failure_category: 'none', recovery_attempt: 'Used proactive two-segment 24-fps one-worker profile after prior sandbox memory-reset evidence',
  validation_status: 'source_ledger_verified; html_lint_zero_errors_per_segment; qc_contact_sheet_reviewed; mp4_60s_h264_aac_1080x1920_verified; canonical_drive_upload_and_checksum_verified',
  remaining_blocker: 'No production blocker remains for Reel_0004; public social posting remains excluded without separate exact destination, caption, and action-specific confirmation', credential_material: 'none'
})}\n`);

console.log(JSON.stringify({ now, next_reel: master.current_reel, completed: master.counts.completed, ids }, null, 2));
