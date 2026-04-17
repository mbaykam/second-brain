---
title: Daily Morning Briefing
summary: Automated RSS news briefing system with email delivery
category: project
status: active
schedule: "0 7 * * *"
created: 2026-04-17
updated: 2026-04-17
provenance:
  - memory.md^[extracted]
  - daily-notes-2026-04-16^[extracted]
---

# Daily Morning Briefing

**Status:** Active ✅  
**Schedule:** Daily at 7:00 AM (Europe/Istanbul)  
**Output:** Email to msbaykam@gmail.com

## Overview

Automated morning news briefing system that aggregates RSS feeds from multiple sources and delivers a formatted digest via email.

## Data Sources

| Section | Source | URL |
|---------|--------|-----|
| Economy | Exchange rates API + Financial news | Multiple |
| World News | BBC | `http://feeds.bbci.co.uk/news/world/rss.xml` |
| World News | Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` |
| Turkey News | Daily Sabah | `https://www.dailysabah.com/rss` |
| Technology | TechCrunch | `https://techcrunch.com/feed/` |
| Technology | The Verge | `https://www.theverge.com/rss/index.xml` |

## Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰  THE MORNING BRIEFING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅  Thursday, April 16, 2026

📈  ECONOMY & MARKETS
    • USD/TRY: 44.74
    → UK economy grew faster than expected...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍  WORLD NEWS
    → Lyse Doucet: Under fragile ceasefire...
```

## Technical Details

- **Script:** `daily_briefing.py` (Python 3)
- **Location:** `/home/mete/.openclaw/workspace/`
- **Email tool:** himalaya (CLI) at `/home/linuxbrew/.linuxbrew/bin/himalaya`
- **Cron job:** `0 7 * * *`
- **Log:** `/tmp/briefing_cron.log`

## Historical Fixes

### 2026-04-16: CDATA Parsing Fix
**Problem:** RSS feeds with `<title><![CDATA[...]]></title>` returned empty headlines.  
**Solution:** Replaced regex parser with `xml.etree.ElementTree` for proper CDATA handling.  
**Impact:** All headlines now populate correctly.

### 2026-04-16: Email PATH Fix
**Problem:** Cron couldn't find `himalaya` binary.  
**Solution:** Use full path `/home/linuxbrew/.linuxbrew/bin/himalaya`.  
**Impact:** Email delivery now reliable.

## Related

- [[rss-parsing]] — Technical details on XML feed handling
- [[cron-management]] — Cron job patterns and debugging