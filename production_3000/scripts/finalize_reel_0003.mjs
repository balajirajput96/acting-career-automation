import { readFileSync, writeFileSync, appendFileSync } from 'node:fs';
import { resolve } from 'node:path';

const repo = resolve(new URL('../../', import.meta.url).pathname);
const production = resolve(repo, 'production_3000');
const now = new Date().toISOString();
const ids = {
  video: '17iQo5as1qOLYuJry0LX1SexzbwjoK0tA',
  metadata: '1En4WRvg4-2KvEiN5AXBEmkEu5bTgfLw3',
  sourceLedger: '1fBHFZ42qCNwwYtUg4aHw9h7cFVFT67NN',
  qualityControl: '1d8nNpQdzHyLXuxWlxSEwth729rVEOy3P'
};

const metadataPath = resolve(production, 'video_projects/reel-0003-home-attention-reset/metadata.json');
const metadata = JSON.parse(readFileSync(metadataPath, 'utf8'));
metadata.status = 'COMPLETED_DRIVE_VERIFIED';
metadata.drive = {
  ...metadata.drive,
  upload_verified: true,
  video_file_id: ids.video,
  metadata_file_id: ids.metadata,
  source_ledger_file_id: ids.sourceLedger,
  quality_control_file_id: ids.qualityControl,
  video_md5: 'ac662fbd801944b1ef5579c8c1bb699c',
  video_size_bytes: 3606200,
  verified_at: now
};
metadata.completed_at = now;
writeFileSync(metadataPath, `${JSON.stringify(metadata, null, 2)}\n`);

const masterPath = resolve(production, 'progress/MASTER_PROGRESS.json');
const master = JSON.parse(readFileSync(masterPath, 'utf8'));
for (const key of ['source_verified', 'scripted', 'rendered', 'qc_passed', 'drive_uploaded_verified', 'completed']) master.counts[key] = 3;
master.counts.planned = 2997;
master.current_reel = 'Reel_0004';
master.last_updated = now;
master.latest_completion = {
  reel_id: 'Reel_0003',
  status: 'COMPLETED_DRIVE_VERIFIED',
  batch_id: 'Batch_001',
  canonical_drive_root_id: master.canonical_drive.folder_id,
  drive_video_file_id: ids.video,
  verified_at: now,
  recovery_note: 'full-length render recovered with two validated low-memory segments; no public post requested'
};
writeFileSync(masterPath, `${JSON.stringify(master, null, 2)}\n`);

const catalogPath = resolve(production, 'catalog/REEL_CATALOG.jsonl');
const catalog = readFileSync(catalogPath, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
const reel = catalog.find((item) => item.reel_id === 'Reel_0003');
if (!reel) throw new Error('Reel_0003 missing from catalog');
Object.assign(reel, {
  status: 'COMPLETED_DRIVE_VERIFIED',
  drive_upload_verified: true,
  drive_video_file_id: ids.video,
  drive_metadata_file_id: ids.metadata,
  drive_source_ledger_file_id: ids.sourceLedger,
  drive_quality_control_file_id: ids.qualityControl,
  completed_at: now,
  public_post_status: 'NOT_REQUESTED'
});
writeFileSync(catalogPath, `${catalog.map((item) => JSON.stringify(item)).join('\n')}\n`);

const batchPath = resolve(production, 'catalog/Batch_001.json');
const batch = JSON.parse(readFileSync(batchPath, 'utf8'));
const batchReel = batch.reels.find((item) => item.reel_id === 'Reel_0003');
if (!batchReel) throw new Error('Reel_0003 missing from Batch_001');
Object.assign(batchReel, {
  status: 'COMPLETED_DRIVE_VERIFIED',
  drive_upload_verified: true,
  drive_video_file_id: ids.video,
  drive_metadata_file_id: ids.metadata,
  drive_source_ledger_file_id: ids.sourceLedger,
  drive_quality_control_file_id: ids.qualityControl,
  completed_at: now,
  public_post_status: 'NOT_REQUESTED'
});
batch.last_updated = now;
writeFileSync(batchPath, `${JSON.stringify(batch, null, 2)}\n`);

const retryPath = resolve(production, 'progress/ERROR_RETRY_LOG.md');
appendFileSync(retryPath, `\n## ${now} — Reel_0003 recovery resolved\n\nThe initial full low-memory render was interrupted by a sandbox reset under memory pressure. Source assets were restored without overwriting completed records. The recovery strategy used two validated 24-fps low-memory segments, then deterministic final re-encode. Final canonical Drive verification succeeded; no retry remains queued.\n`);

const auditPath = resolve(repo, 'data/automation_run_records.jsonl');
appendFileSync(auditPath, `${JSON.stringify({
  timestamp: now,
  task: 'production_3000_reel_0003_recovery_and_completion',
  tools: ['research_sources', 'native_tts', 'native_image', 'hyperframes_segmented_low_memory_render', 'google_drive'],
  result: 'completed_drive_verified',
  reel_id: 'Reel_0003',
  drive_root: master.canonical_drive.folder_id,
  drive_video_file_id: ids.video,
  public_post_status: 'NOT_REQUESTED',
  validation_status: 'passed',
  failure_category: 'recovered_memory_reset',
  credential_material: 'none'
})}\n`);

console.log(JSON.stringify({ now, next_reel: master.current_reel, completed: master.counts.completed, ids }, null, 2));
