---
title: OpenClaw Setup
category: skill
summary: OpenClaw agent configuration, workspace structure, and workflows
created: 2026-04-17
updated: 2026-04-17
provenance:
  - memory.md^[extracted]
  - daily-notes-2026-04-13^[extracted]
---

# OpenClaw Setup

## Workspace Structure

```
~/.openclaw/
├── workspace/              # Primary working directory
│   ├── MEMORY.md          # Long-term memory (curated)
│   ├── AGENTS.md          # Agent behavior guidelines
│   ├── SOUL.md            # Identity and core principles
│   ├── USER.md            # User profile
│   ├── IDENTITY.md        # Agent identity (BRUT)
│   ├── TOOLS.md           # Local tool configurations
│   ├── HEARTBEAT.md       # Periodic task checklist
│   ├── BOOTSTRAP.md       # First-run guide
│   ├── PROCESS.md         # Task execution protocol
│   ├── memory/            # Daily notes (YYYY-MM-DD.md)
│   └── skills/            # Installed skills
├── agents/                # Per-agent data
│   └── <agentId>/
│       ├── agent/
│       └── sessions/      # Session transcripts (.jsonl)
└── openclaw.json         # Global config
```

## Key Files

| File | Purpose |
|------|---------|
| `MEMORY.md` | Curated long-term memory (loaded every session) |
| `memory/*.md` | Daily raw logs (today + yesterday auto-loaded) |
| `AGENTS.md` | Session startup sequence, safety rules, group chat behavior |
| `SOUL.md` | Who the agent is, core truths, verification layer |

## Model Configuration

**Default Model:** `moonshot/kimi-k2.5` (Kimi)  
**Cron/Heartbeat Model:** `moonshot/kimi-k2.5` unless specified otherwise

## Active Cron Jobs

```
0 7 * * *  → Daily Morning Briefing (Python script + email)
```

## Session Startup Sequence

1. Check timestamp of last message (>30 min → ask about fresh start)
2. Load `SOUL.md` — who the agent is
3. Load `USER.md` — who they're helping
4. Load `IDENTITY.md` — agent identity
5. Load today's memory file (`memory/YYYY-MM-DD.md`)
6. Load `MEMORY.md` (main session only)

## Heartbeat Protocol

When receiving heartbeat poll:
1. Read `HEARTBEAT.md` for task list
2. Check each task for attention needed
3. If nothing needs attention → reply `HEARTBEAT_OK`
4. If attention needed → reply with alert text

## Tools Available

| Category | Tools |
|----------|-------|
| File | read, write, edit |
| System | exec, process |
| Web | web_search (Brave), web_fetch, browser |
| Memory | memory_search, memory_get |
| Agents | sessions_spawn, subagents, sessions_send |
| Messaging | message (Telegram native) |

## Skills Directory

Skills installed at `~/.openclaw/skills/` and `~/.agents/skills/`

Currently installed:
- `youtube-shorts-automation` — Video generation pipeline
- `wiki-update`, `wiki-query` (from obsidian-wiki) — Knowledge management

## Daily Note Format

```markdown
# Session: YYYY-MM-DD HH:MM:SS UTC

- **Session Key**: agent:main:main
- **Session ID**: UUID
- **Source**: telegram

## Conversation Summary

user: [message summary]
assistant: [response summary]
```

## Related

- [[brut-agent]] — Agent identity details
- [[cron-management]] — Scheduled task patterns
- [[verification-layer]] — Task execution protocol