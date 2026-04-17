---
title: Karpathy LLM Wiki Pattern
category: concept
summary: Knowledge compilation vs RAG — building persistent, cross-linked markdown wikis
created: 2026-04-17
updated: 2026-04-17
confidence: high
provenance:
  - research-karpathy-gist^[inferred]
---

# Karpathy LLM Wiki Pattern

> *"Instead of asking an LLM the same questions over and over (or doing RAG every time), compile knowledge once into interconnected markdown files and keep them current."* — Andrej Karpathy

## Core Idea

**RAG (Retrieval-Augmented Generation):**
- Re-derives answers every time by chunking documents
- Runs vector search on each query
- Same work repeated

**LLM Wiki Pattern:**
- Compile knowledge once into structured wiki pages
- Pre-build cross-references
- Query the compiled wiki
- **Result:** At ~100 articles / ~400K words, outperforms RAG for Q&A

## Architecture

### 4-Layer Memory Stack

```
L1: Session JSONL        → Raw conversation logs
L2: Qdrant vectors       → Semantic search (optional)
L3: Daily notes          → Structured summaries
L4: HANDOFF.md / Wiki    → Cross-session project continuity
```

### The Compound Loop

```
Raw sources → Ingest → Compile → Wiki pages
                   ↑                    ↓
                   └──── Query ←───────┘
                        (file back)
```

Every query answer gets filed back → wiki grows → next query has more to work with.

## Workflow

| Phase | Action |
|-------|--------|
| **Ingest** | Drop raw sources into `raw/` folder |
| **Resolve** | Fetch full content (transcripts, articles, PDFs) |
| **Classify** | Extract by type (transcript, paper, article, tweet) |
| **Compile** | Create wiki pages with `[[wikilinks]]` |
| **Cross-link** | Connect related concepts |
| **Bias check** | Add counter-arguments and data gaps |
| **Index** | Update master catalog |

## Safeguards

| Mechanism | Purpose |
|-----------|---------|
| Bias checks | Counter-arguments on every page |
| Validation gate | `explored: false` until human verifies |
| Confidence levels | high/medium/low/uncertain tagging |
| Source tracing | Every claim links to source |

## Directory Structure

```
vault/
├── concepts/           # Global knowledge, ideas, theories
├── entities/           # People, orgs, tools
├── skills/             # How-to knowledge, procedures
├── references/         # Source summaries
├── synthesis/          # Cross-cutting analysis
├── journal/            # Timestamped logs
├── projects/           # Per-project knowledge
│   └── <name>/
│       ├── _project.md
│       ├── concepts/
│       └── skills/
├── index.md            # Auto-maintained catalog
├── log.md              # Operation log
└── .manifest.json      # Ingest tracking
```

## vs Traditional Note-Taking

| Aspect | Traditional | LLM Wiki |
|--------|-------------|----------|
| Creation | Manual | AI-assisted |
| Linking | Manual `[[links]]` | Auto cross-references |
| Updates | Manual | AI-maintained |
| Query | Search | Compiled Q&A |
| Growth | Linear | Compounding |

## Tools

| Tool | Purpose |
|------|---------|
| **Obsidian** | Viewer (graph, backlinks, Dataview) |
| **qmd** | Semantic search for Markdown |
| **LLM agent** | Maintainer (ingest, compile, update) |

## Key Insight

> *"Knowledge should be accessible, not overwhelming. You are curating cognitive load for both yourself and the system."*

## References

- [Karpathy's Original Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [[obsidian-setup]] — This vault's implementation
- [[openclaw-setup]] — Agent integration