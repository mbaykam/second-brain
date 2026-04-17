---
title: Mobile Sync Setup
category: reference
summary: Free options for syncing vault to mobile devices
---

# Mobile Sync (Free)

## Option 1: GitHub + Obsidian Git ⭐ Recommended

**Cost:** Free (public repo) or Free (private repo)  
**Sync:** Manual or auto (every X minutes)  
**Conflict handling:** Git merge

### Desktop Setup

1. Create GitHub repo (private recommended)
2. Add remote to vault:
   ```bash
   git remote add origin https://github.com/YOURNAME/second-brain.git
   git branch -M main
   git push -u origin main
   ```

3. In Obsidian → Settings → Community Plugins → Browse
4. Install **"Obsidian Git"**
5. Enable it
6. Configure:
   - Auto backup: ON
   - Auto backup interval: 5 minutes
   - Auto pull on startup: ON

### Mobile Setup

1. Install Obsidian app (free)
2. Clone repo to phone:
   ```bash
   # Using Termux or Git app
   git clone https://github.com/YOURNAME/second-brain.git
   ```
3. Open folder as vault in Obsidian mobile
4. Install Obsidian Git plugin (same settings)

### Workflow

- Desktop: Edit → auto-commits every 5 min
- Mobile: Pull → Edit → Commit → Push
- Back on desktop: Auto-pulls changes

---

## Option 2: Syncthing (P2P)

**Cost:** Completely free, no server  
**Sync:** Real-time  
**Best for:** Privacy-conscious, no cloud dependency

### Setup

1. Install Syncthing:
   - Desktop: `sudo apt install syncthing`
   - Android: F-Droid or Play Store
   - iOS: Not available (use Möbius Sync - paid)

2. On desktop:
   ```bash
   syncthing
   # Open http://localhost:8384
   ```

3. Add folder: `/home/mete/.openclaw/workspace/second-brain-vault/`

4. On phone: Add device (scan QR), accept share

5. Done. Changes sync instantly both ways.

---

## Option 3: Self-hosted LiveSync

**Cost:** Free (IBM Cloudant, etc.)  
**Sync:** Real-time  
**Best for:** Live collaboration feel

### Setup

1. Get free CouchDB:
   - IBM Cloudant (free tier: 1GB)
   - Or self-host on VPS

2. In Obsidian → Install "Self-hosted LiveSync"

3. Configure with your CouchDB URL/credentials

4. Same setup on mobile

5. Changes appear instantly across devices

---

## Comparison

| Feature | GitHub+Git | Syncthing | LiveSync |
|---------|-----------|-----------|----------|
| Cost | Free | Free | Free* |
| Real-time | No | Yes | Yes |
| iOS support | Yes | No** | Yes |
| Conflict handling | Git merge | Last-write-wins | Built-in |
| Internet required | Yes | No (LAN works) | Yes |
| Privacy | GitHub sees data | Fully private | Cloud sees data |

*Free tier limits  
**iOS requires Möbius Sync ($5)

## Recommendation

- **Desktop + Android:** Syncthing (simplest, free, private)
- **With iPhone:** GitHub + Obsidian Git
- **Need real-time everywhere:** LiveSync with free Cloudant

---

*Last updated: 2026-04-17*
