#!/bin/bash
# Wiki Automation Master Script
# Run all wiki maintenance tasks

VAULT_PATH="/home/mete/.openclaw/workspace/second-brain-vault"
LOG_FILE="/tmp/wiki-auto.log"

echo "=== Wiki Automation $(date) ===" >> "$LOG_FILE"

cd "$VAULT_PATH" || exit 1

# 1. Ingest new sources
echo "[1/4] Ingesting raw sources..." >> "$LOG_FILE"
python3 scripts/wiki-ingest.py --all >> "$LOG_FILE" 2>&1

# 2. Run lint checks
echo "[2/4] Running lint..." >> "$LOG_FILE"
python3 scripts/wiki-lint.py >> "$LOG_FILE" 2>&1

# 3. Commit changes
echo "[3/4] Committing changes..." >> "$LOG_FILE"
git add -A
git commit -m "Wiki auto-update: $(date +%Y-%m-%d-%H:%M)" >> "$LOG_FILE" 2>&1 || true

# 4. Push to GitHub
echo "[4/4] Pushing to GitHub..." >> "$LOG_FILE"
git push origin main >> "$LOG_FILE" 2>&1 || echo "Push failed - may need auth" >> "$LOG_FILE"

echo "=== Done $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"