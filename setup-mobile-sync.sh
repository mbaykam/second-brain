#!/bin/bash
# One-time setup for mobile sync via GitHub

echo "🔧 Setting up mobile sync..."

# Check if remote exists
if git remote | grep -q origin; then
    echo "✅ Remote already configured"
else
    echo "❌ No remote configured"
    echo ""
    echo "To complete setup:"
    echo "1. Create a free private repo at: https://github.com/new"
    echo "   Name it: second-brain"
    echo "   Keep it private"
    echo ""
    echo "2. Run this command (replace YOURNAME with your GitHub username):"
    echo "   git remote add origin https://github.com/YOURNAME/second-brain.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

# Push current state
git add -A
git commit -m "Update: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
git push origin main

echo "✅ Vault synced to GitHub!"
echo ""
echo "📱 Now on your phone:"
echo "1. Open Obsidian app"
echo "2. Tap 'Open folder as vault'"
echo "3. Choose where to clone (e.g., iCloud/Obsidian/)"
echo "4. Run: git clone https://github.com/YOURNAME/second-brain.git"
echo "5. Open that folder in Obsidian"
echo "6. Settings → Community Plugins → Browse → Install 'Obsidian Git'"
echo "7. Enable it, configure auto-sync every 5 min"
echo ""
echo "Done! Changes sync both ways automatically."
