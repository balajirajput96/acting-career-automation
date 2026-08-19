#!/usr/bin/env bash
# Import externally generated internal-review packages without publishing media.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${1:-/home/ubuntu/create_50_video_review_packages.json}"
DEST="$ROOT/educational_video_queue/batch_50"
INDEX="$DEST/INDEX.md"

if [[ ! -f "$MANIFEST" ]]; then
  echo "Missing batch manifest: $MANIFEST" >&2
  exit 1
fi

mkdir -p "$DEST"
printf '%s\n\n' '# 50-Video Internal Review Batch' > "$INDEX"
printf '%s\n\n' '**Status:** `INTERNAL REVIEW ONLY — NOT POSTED`' >> "$INDEX"
printf '%s\n' '| No. | Track | Topic | Package | Source URLs | Status |' >> "$INDEX"
printf '%s\n' '| ---: | --- | --- | --- | --- | --- |' >> "$INDEX"

count=0
while IFS= read -r encoded; do
  record="$(printf '%s' "$encoded" | base64 --decode)"
  input="$(printf '%s' "$record" | jq -r '.[0]')"
  url="$(printf '%s' "$record" | jq -r '.[1]')"
  sources="$(printf '%s' "$record" | jq -r '.[2]')"
  status="$(printf '%s' "$record" | jq -r '.[3]')"

  number="$(printf '%s' "$input" | cut -d' ' -f1)"
  track="$(printf '%s' "$input" | cut -d'|' -f2 | xargs)"
  topic="$(printf '%s' "$input" | cut -d'|' -f3- | xargs)"
  slug="$(printf '%s' "$topic" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//; s/-$//')"
  filename="$(printf '%02d' "$((10#$number))")_${slug}.md"

  curl --fail --location --retry 3 --silent --show-error "$url" --output "$DEST/$filename"
  if ! grep -q 'INTERNAL REVIEW ONLY' "$DEST/$filename"; then
    echo "Imported package does not preserve internal-review boundary: $filename" >&2
    exit 1
  fi

  printf '| %s | %s | %s | [%s](%s) | %s | %s |\n' \
    "$number" "$track" "$topic" "$filename" "$filename" "$sources" "$status" >> "$INDEX"
  count=$((count + 1))
done < <(jq -r '.results[] | [.input, .output.package_file, .output.source_urls, .output.result_status] | @base64' "$MANIFEST")

if [[ "$count" -ne 50 ]]; then
  echo "Expected 50 packages; imported $count" >&2
  exit 1
fi

echo "PASS: Imported $count internal-only review packages to $DEST"
