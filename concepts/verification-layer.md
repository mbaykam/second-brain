---
title: Verification Layer
category: concept
summary: Systematic check-and-test protocol for reliable task execution
created: 2026-04-17
updated: 2026-04-17
confidence: high
provenance:
  - memory.md^[extracted]
---

# Verification Layer

> *"A task is NOT complete when the command runs - it's complete when you've VERIFIED it worked."*

## Core Principle

Systematic verification protocol integrated into all operations. Prevents silent failures and assumptions of success.

## The 4-Phase Protocol

### Phase 1: Plan
- [ ] Understand what success looks like
- [ ] Identify how to verify success
- [ ] Note potential failure points

### Phase 2: Execute
- [ ] Run the command/write the file/send the message
- [ ] Capture output and errors

### Phase 3: VERIFY (Critical)
- [ ] Check exit codes / success status
- [ ] Verify outputs match expectations
- [ ] Test that it actually works
- [ ] For files: read them back
- [ ] For emails: confirm proper formatting/attachments
- [ ] For web: check response status and content

### Phase 4: Confirm
- [ ] Report success with evidence
- [ ] Or report failure with diagnostic info

## Verification Patterns

| Operation | Verification Method |
|-----------|---------------------|
| **File operations** | `write file → read file back → compare to expected` |
| **Email sending** | `compose → send → check for errors → verify attachments` |
| **Command execution** | `run → check exit code → verify outputs → test result` |
| **File edits** | `edit → read back → check context unchanged → verify syntax` |
| **Web operations** | `fetch → check status → verify content contains expected data` |

## Red Flags (Extra Care Needed)

- Silent failures (command ran but produced no output)
- Zero-byte files
- Generic success messages without details
- User reports something "doesn't work"
- External dependencies (email servers, web APIs)
- File format conversions (Markdown→PDF, etc.)

## Origin

**Date:** 2026-04-16  
**Trigger:** Email attachment failed ("noname" file, couldn't open). Realized success was assumed based on command output rather than verified results.  
**Files updated:**
- `SOUL.md` — Added as core principle
- `AGENTS.md` — Added Verification Checklist to Safety section
- `PROCESS.md` — Created detailed task execution protocol

## Key Insight

> *"A command completing ≠ task succeeding. Always verify outputs, file contents, email delivery, etc."*

## Counter-Arguments

- Adds time overhead to simple operations
- May be excessive for low-risk tasks

## Data Gaps

- No automated verification tracking (manual checklist only)
- No failure rate metrics collected