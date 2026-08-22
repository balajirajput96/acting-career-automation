import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(new URL('../', import.meta.url).pathname);
const master = JSON.parse(readFileSync(resolve(root, 'progress/MASTER_PROGRESS.json'), 'utf8'));
const catalog = readFileSync(resolve(root, 'catalog/REEL_CATALOG.jsonl'), 'utf8')
  .trim()
  .split('\n')
  .filter(Boolean)
  .map(JSON.parse);

const errors = [];
if (catalog.length !== master.total_reels) errors.push(`Catalog count ${catalog.length} does not equal total ${master.total_reels}`);
if (new Set(catalog.map((record) => record.reel_id)).size !== master.total_reels) errors.push('Catalog reel IDs are not unique');
if (!master.canonical_drive?.folder_id) errors.push('Canonical Drive root is missing');
if (master.verified_drive_artifacts?.upload_verified !== true) errors.push('Master catalog/progress upload is not verified');

const completed = catalog.filter((record) => record.status === 'COMPLETED_DRIVE_VERIFIED');
if (completed.length !== master.counts.completed) errors.push(`Completed count ${completed.length} does not match master ${master.counts.completed}`);
for (const record of completed) {
  if (!record.drive_upload_verified || !record.drive_video_file_id) errors.push(`${record.reel_id} is marked complete without a verified Drive video ID`);
}

const requiredPilot = [
  'video_projects/reel-0001-attention-switching/metadata.json',
  'source_ledgers/Reel_0001_attention_task_switching.md',
  'quality_control/Reel_0001_preview_review.md'
];
for (const file of requiredPilot) if (!existsSync(resolve(root, file))) errors.push(`Missing pilot record: ${file}`);

if (errors.length) {
  for (const error of errors) console.error(`FAIL: ${error}`);
  process.exit(1);
}
console.log(`PASS: ${master.total_reels} catalog records, ${completed.length} Drive-verified completion(s), canonical Drive mapping valid.`);
