---
title: Cron Management
category: skill
summary: Scheduled task automation, PATH issues, and debugging
created: 2026-04-17
updated: 2026-04-17
provenance:
  - daily-notes-2026-04-16^[extracted]
---

# Cron Management

## The PATH Problem

Cron runs with a minimal environment. Common issue:

```bash
# Works in terminal:
himalaya send --to user@example.com

# Fails in cron:
# Error: himalaya: command not found
```

**Root cause:** Cron's PATH doesn't include user-installed binaries.

## Solution: Use Full Paths

```bash
# Instead of:
0 7 * * * himalaya send --to user@example.com

# Use:
0 7 * * * /home/linuxbrew/.linuxbrew/bin/himalaya send --to user@example.com
```

## Finding Full Paths

```bash
which himalaya
# → /home/linuxbrew/.linuxbrew/bin/himalaya

which python3
# → /usr/bin/python3
```

## Active Cron Jobs

```
# Daily Morning Briefing - 7:00 AM
0 7 * * * cd /home/mete/.openclaw/workspace && /usr/bin/python3 daily_briefing.py >> /tmp/briefing_cron.log 2>&1
```

## Best Practices

| Practice | Why |
|----------|-----|
| Use full paths | Avoids PATH issues |
| Redirect output | `>> /tmp/log.log 2>&1` captures errors |
| Set working directory | `cd /path && command` ensures context |
| Log rotation | Prevent logs from growing indefinitely |

## Crontab Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6, Sun=0)
│ │ │ │ │
│ │ │ │ │
* * * * *  command
```

## Common Schedules

| Schedule | Cron Expression |
|----------|-----------------|
| Every minute | `* * * * *` |
| Every hour | `0 * * * *` |
| Daily at 7 AM | `0 7 * * *` |
| Weekly (Sunday) | `0 0 * * 0` |
| Every 10 minutes | `*/10 * * * *` |

## Debugging

```bash
# Check current crontab
crontab -l

# Edit crontab
crontab -e

# View cron logs (Ubuntu/Debian)
grep CRON /var/log/syslog

# Test command with cron's minimal environment
env -i HOME=$HOME PATH=/usr/bin:/bin /path/to/command
```

## Related

- [[daily-morning-briefing]] — Primary cron job example
- [[rss-parsing]] — What the cron job runs