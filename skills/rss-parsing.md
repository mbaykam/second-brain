---
title: RSS Parsing
category: skill
summary: Handling RSS/Atom feeds with proper XML parsing, including CDATA
created: 2026-04-17
updated: 2026-04-17
provenance:
  - daily-notes-2026-04-16^[extracted]
---

# RSS Parsing

## The CDATA Problem

Many RSS feeds wrap content in CDATA sections:

```xml
<title><![CDATA[UK economy grew faster than expected]]></title>
```

**Issue:** Regex parsers can't handle this — they return empty strings.

## Solution: Proper XML Parser

Use `xml.etree.ElementTree` (Python) instead of regex:

```python
import xml.etree.ElementTree as ET
import urllib.request

def parse_rss(url):
    """Parse RSS feed with proper CDATA handling."""
    with urllib.request.urlopen(url, timeout=10) as response:
        tree = ET.parse(response)
        root = tree.getroot()
        
        items = []
        for item in root.findall('.//item'):
            title = item.find('title')
            if title is not None:
                # .text automatically handles CDATA
                items.append(title.text)
        return items
```

## Key Differences

| Approach | CDATA Handling | Robustness |
|----------|----------------|------------|
| Regex | ❌ Fails | Fragile |
| xml.etree.ElementTree | ✅ Automatic | Reliable |
| feedparser library | ✅ Built-in | Heavy dependency |

## Common RSS Feed URLs

| Source | URL |
|--------|-----|
| BBC World | `http://feeds.bbci.co.uk/news/world/rss.xml` |
| Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` |
| Daily Sabah | `https://www.dailysabah.com/rss` |
| TechCrunch | `https://techcrunch.com/feed/` |
| The Verge | `https://www.theverge.com/rss/index.xml` |

## Error Handling

```python
try:
    headlines = parse_rss(feed_url)
except ET.ParseError as e:
    # Malformed XML
    headlines = [f"[Parse error: {e}]"]
except urllib.error.URLError as e:
    # Network issue
    headlines = [f"[Fetch error: {e}]"]
```

## Related

- [[daily-morning-briefing]] — Primary use case
- [[cron-management]] — Scheduling automated fetches