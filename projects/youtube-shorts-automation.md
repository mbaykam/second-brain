---
title: YouTube Shorts Automation
category: project
summary: Turkish YouTube Shorts pipeline using AI video generation
status: in-development
created: 2026-04-17
updated: 2026-04-17
provenance:
  - memory.md^[extracted]
  - daily-notes-2026-04-13^[extracted]
---

# YouTube Shorts Automation

**Status:** In Development 🔄  
**Language:** Turkish  
**Platform:** YouTube Shorts

## Overview

Automated pipeline for creating and uploading Turkish YouTube Shorts using AI-generated video content.

## Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| Video Generation | Kling AI | Image-to-video generation with BGM + voice |
| Voice | Edge TTS / ElevenLabs | Text-to-speech narration |
| Image Sources | Pexels API | Stock photos/backgrounds |
| Upload | YouTube API | Automated publishing |
| Scheduling | Cron | Daily automatic execution |

## Skills Integration

Uses `youtube-shorts-automation` skill from workspace:
- Location: `~/.openclaw/workspace/skills/youtube-shorts-automation/`

## Workflow

1. **Content Planning** → Script/topic selection
2. **Image Selection** → Pull from Pexels or generate
3. **Video Generation** → Kling AI processes image → video
4. **Audio Addition** → TTS narration + background music
5. **Upload** → YouTube API with Turkish metadata
6. **Scheduling** → Cron job for daily posts

## Configuration

- **YouTube API credentials:** Configured and stored
- **Pexels API key:** Available for image retrieval
- **Ollama:** Running locally for LLM inference

## Related Topics

- [[kling-ai]] — Video generation specifics
- [[pexels-api]] — Image sourcing workflow
- [[ollama-setup]] — Local LLM for content generation

## Open Questions

- Caption generation workflow (partially addressed 2026-04-13)
- Optimal posting schedule for Turkish audience
- Content niche focus (general vs specific topic)