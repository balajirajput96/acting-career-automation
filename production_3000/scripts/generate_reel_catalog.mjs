import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(new URL('../', import.meta.url).pathname);
const catalogDir = resolve(root, 'catalog');
const progressDir = resolve(root, 'progress');
mkdirSync(catalogDir, { recursive: true });
mkdirSync(progressDir, { recursive: true });

const families = [
  ['Psychology', 'Attention', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Working Memory', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Long-Term Memory', 'RESEARCH_REQUIRED'],
  ['Neuroscience', 'Sleep and Learning', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Emotion Regulation', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Stress and Coping', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Habits', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Decision Making', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Motivation', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Social Cognition', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Relationships', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Development Across the Lifespan', 'RESEARCH_REQUIRED'],
  ['Neuroscience', 'Brain Basics', 'RESEARCH_REQUIRED'],
  ['Neuroscience', 'Neuroplasticity', 'RESEARCH_REQUIRED'],
  ['Psychology', 'Learning Science', 'RESEARCH_REQUIRED'],
  ['Contemplative Practice', 'Meditation and Awareness', 'RESEARCH_OR_TRADITION_CLASSIFICATION_REQUIRED'],
  ['Philosophy', 'Mind and Identity', 'PHILOSOPHICAL_CLASSIFICATION_REQUIRED'],
  ['Philosophy', 'Consciousness Questions', 'PHILOSOPHICAL_CLASSIFICATION_REQUIRED'],
  ['Spirituality', 'Contemplative Traditions', 'TRADITIONAL_BELIEF_CLASSIFICATION_REQUIRED'],
  ['Psychology', 'Everyday Human Behaviour', 'RESEARCH_REQUIRED']
];

const lenses = [
  'Mechanism', 'Common Misconception', 'Observed Pattern', 'Practical Context', 'Individual Variation',
  'Lab-versus-Life Context', 'Measurement Question', 'Everyday Example', 'Ethical Question', 'Open Question',
  'Evidence Comparison', 'Boundary Condition', 'Historical Context', 'Visual Metaphor', 'Limitation'
];

const contexts = [
  'Study', 'Work', 'Home', 'Digital Life', 'Transition',
  'Relationships', 'Routine', 'Rest', 'Problem Solving', 'Self Reflection'
];

const slots = [];
let number = 1;
for (const [family, subtopic, classification] of families) {
  for (const lens of lenses) {
    for (const context of contexts) {
      const reelId = `Reel_${String(number).padStart(4, '0')}`;
      const batchNumber = Math.ceil(number / 30);
      slots.push({
        reel_id: reelId,
        batch_id: `Batch_${String(batchNumber).padStart(3, '0')}`,
        topic_family: family,
        subtopic,
        editorial_lens: lens,
        audience_context: context,
        source_classification_required: classification,
        status: 'PLANNED',
        drive_upload_verified: false,
        public_post_status: 'NOT_REQUESTED'
      });
      number += 1;
    }
  }
}

if (slots.length !== 3000) throw new Error(`Expected 3000 catalog slots, received ${slots.length}`);
if (new Set(slots.map((slot) => `${slot.topic_family}|${slot.subtopic}|${slot.editorial_lens}|${slot.audience_context}`)).size !== 3000) {
  throw new Error('Catalog uniqueness check failed');
}

writeFileSync(resolve(catalogDir, 'REEL_CATALOG.jsonl'), `${slots.map(JSON.stringify).join('\n')}\n`);
for (let batch = 1; batch <= 100; batch += 1) {
  const batchId = `Batch_${String(batch).padStart(3, '0')}`;
  const records = slots.filter((slot) => slot.batch_id === batchId);
  writeFileSync(resolve(catalogDir, `${batchId}.json`), `${JSON.stringify({ batch_id: batchId, reel_count: records.length, status: 'PLANNED', reels: records }, null, 2)}\n`);
}

writeFileSync(resolve(progressDir, 'CATALOG_GENERATION_REPORT.json'), `${JSON.stringify({ generated_at: new Date().toISOString(), reel_count: slots.length, batch_count: 100, status: 'PASS' }, null, 2)}\n`);
console.log(`PASS: generated ${slots.length} unique planned Reel slots across 100 batches.`);
