---
title: Memory Sources
category: reference
summary: Provenance of knowledge extracted into this wiki
created: 2026-04-17
updated: 2026-04-17
---

# Memory Sources

This wiki was bootstrapped from existing OpenClaw memory files.

## Primary Sources

### MEMORY.md
**Path:** `/home/mete/.openclaw/workspace/MEMORY.md`  
**Type:** Curated long-term memory  
**Ingested:** 2026-04-17  
**Pages created:** 5

Extracted knowledge:
- Daily Morning Briefing system
- Verification Layer protocol
- YouTube Shorts Automation project
- Mete's preferences and contacts
- Operating improvements (2026-04-16)

### Daily Notes
**Path:** `/home/mete/.openclaw/workspace/memory/*.md`  
**Count:** 16 files  
**Date range:** 2026-04-13 to 2026-04-17  
**Ingested:** 2026-04-17  
**Pages created:** 3

Notable sessions:
- RSS email fix (CDATA parsing)
- Cron PATH issues resolved
- OpenClaw model switching
- Kling AI setup
- Store skill setup

### Identity Files
**Files:**
- `IDENTITY.md` — BRUT agent identity
- `USER.md` — Mete profile
- `SOUL.md` — Core principles
- `AGENTS.md` — Session startup rules
- `TOOLS.md` — Tool configurations

## Extraction Method

1. **Survey** — Scanned all source files
2. **Classify** — Grouped by topic (projects, concepts, entities, skills)
3. **Distill** — Extracted durable knowledge (not ephemeral chatter)
4. **Cross-link** — Created `[[wikilinks]]` between related pages
5. **Tag** — Added provenance markers (^[extracted], ^[inferred])

## Confidence Levels

| Page | Confidence | Reason |
|------|------------|--------|
| [[daily-morning-briefing]] | High | Explicit system documentation |
| [[verification-layer]] | High | Detailed protocol in MEMORY.md |
| [[brut-agent]] | High | Clear identity files |
| [[karpathy-llm-wiki-pattern]] | Medium | Research synthesis |

## Gaps & Ambiguities

- Session transcripts (`.jsonl`) not deeply parsed — daily summaries sufficient
- Some daily notes are heartbeat-only (no content)
- Ollama configuration details not fully extracted
- YouTube API credentials location not documented

## Future Mining

Potential additional sources:
- `~/.openclaw/agents/*/sessions/*.jsonl` — Full conversation transcripts
- Git history of workspace — Project evolution
- External sources (bookmarks, articles, tweets)

## Related

- [[openclaw-setup]] — Where these sources live
- [[log]] — When extraction happened