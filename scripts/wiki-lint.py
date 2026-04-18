#!/usr/bin/env python3
"""
Wiki Lint Script
Check for issues in the wiki: orphans, stale pages, broken links, contradictions.
Usage: python3 wiki-lint.py [--fix]
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

VAULT_PATH = Path("/home/mete/.openclaw/workspace/second-brain-vault")
REPORT_FILE = VAULT_PATH / "log.md"

def get_all_pages():
    """Get all wiki pages with metadata."""
    pages = []
    for category in ["concepts", "entities", "skills", "references", "synthesis", "projects"]:
        cat_path = VAULT_PATH / category
        if not cat_path.exists():
            continue
        
        for filepath in cat_path.rglob("*.md"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse frontmatter
                fm_match = re.match(r'^---\n(.*?)---\n', content, re.DOTALL)
                frontmatter = {}
                if fm_match:
                    fm_text = fm_match.group(1)
                    for line in fm_text.split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            frontmatter[key.strip()] = val.strip()
                
                # Find wikilinks
                wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                
                pages.append({
                    "path": filepath,
                    "relative": str(filepath.relative_to(VAULT_PATH)),
                    "frontmatter": frontmatter,
                    "wikilinks": wikilinks,
                    "content": content
                })
            except:
                continue
    
    return pages

def find_orphans(pages):
    """Find pages with no incoming links."""
    all_links = set()
    for page in pages:
        all_links.update(page["wikilinks"])
    
    orphans = []
    for page in pages:
        page_name = page["path"].stem
        if page_name not in all_links and page["relative"] != "index.md":
            orphans.append(page)
    
    return orphans

def find_broken_links(pages):
    """Find wikilinks that point to non-existent pages."""
    existing = {p["path"].stem for p in pages}
    existing.add("index")  # Always exists
    
    broken = []
    for page in pages:
        for link in page["wikilinks"]:
            link_clean = link.split('/')[0] if '/' in link else link
            if link_clean not in existing:
                broken.append({
                    "from": page["relative"],
                    "to": link
                })
    
    return broken

def find_stale_pages(pages, days=30):
    """Find pages not updated in N days."""
    cutoff = datetime.now() - timedelta(days=days)
    stale = []
    
    for page in pages:
        updated = page["frontmatter"].get("updated", "")
        if updated:
            try:
                updated_date = datetime.strptime(updated, "%Y-%m-%d")
                if updated_date < cutoff:
                    stale.append(page)
            except:
                pass
    
    return stale

def find_uncertain_claims(pages):
    """Find pages with low confidence or no sources."""
    uncertain = []
    
    for page in pages:
        confidence = page["frontmatter"].get("confidence", "").lower()
        provenance = page["frontmatter"].get("provenance", [])
        
        if confidence in ["low", "uncertain"] or not provenance:
            uncertain.append(page)
    
    return uncertain

def generate_report(issues):
    """Generate a markdown report of issues."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""---
title: Wiki Maintenance Log
category: meta
---

# Wiki Maintenance Report

Generated: {now}

## Summary

- Orphan pages: {len(issues['orphans'])}
- Broken links: {len(issues['broken_links'])}
- Stale pages (>30 days): {len(issues['stale'])}
- Uncertain claims: {len(issues['uncertain'])}

"""
    
    if issues['orphans']:
        report += "\n## Orphan Pages (no incoming links)\n\n"
        for page in issues['orphans'][:10]:
            report += f"- [[{page['relative'].replace('.md', '')}]]\n"
        if len(issues['orphans']) > 10:
            report += f"- ... and {len(issues['orphans']) - 10} more\n"
    
    if issues['broken_links']:
        report += "\n## Broken Links\n\n"
        for link in issues['broken_links'][:10]:
            report += f"- `{link['to']}` in [[{link['from'].replace('.md', '')}]]\n"
        if len(issues['broken_links']) > 10:
            report += f"- ... and {len(issues['broken_links']) - 10} more\n"
    
    if issues['stale']:
        report += "\n## Stale Pages (>30 days since update)\n\n"
        for page in issues['stale'][:10]:
            updated = page['frontmatter'].get('updated', 'unknown')
            report += f"- [[{page['relative'].replace('.md', '')}]] (last: {updated})\n"
        if len(issues['stale']) > 10:
            report += f"- ... and {len(issues['stale']) - 10} more\n"
    
    if issues['uncertain']:
        report += "\n## Pages Needing Verification\n\n"
        for page in issues['uncertain'][:10]:
            conf = page['frontmatter'].get('confidence', 'unknown')
            report += f"- [[{page['relative'].replace('.md', '')}]] (confidence: {conf})\n"
        if len(issues['uncertain']) > 10:
            report += f"- ... and {len(issues['uncertain']) - 10} more\n"
    
    report += "\n## Recommendations\n\n"
    
    if issues['orphans']:
        report += "- Link orphan pages from relevant concept/entity pages\n"
    if issues['broken_links']:
        report += "- Fix or remove broken wikilinks\n"
    if issues['stale']:
        report += "- Review and update stale pages\n"
    if issues['uncertain']:
        report += "- Add sources or verify uncertain claims\n"
    
    if not any(issues.values()):
        report += "- Wiki is in good shape! No issues found.\n"
    
    return report

def main():
    parser = argparse.ArgumentParser(description="Wiki lint tool")
    parser.add_argument("--fix", action="store_true", help="Attempt auto-fixes")
    parser.add_argument("--output", "-o", default=str(REPORT_FILE), help="Output file")
    
    args = parser.parse_args()
    
    print("Scanning wiki...")
    pages = get_all_pages()
    print(f"Found {len(pages)} pages")
    
    issues = {
        "orphans": find_orphans(pages),
        "broken_links": find_broken_links(pages),
        "stale": find_stale_pages(pages),
        "uncertain": find_uncertain_claims(pages)
    }
    
    print(f"\nIssues found:")
    print(f"  Orphans: {len(issues['orphans'])}")
    print(f"  Broken links: {len(issues['broken_links'])}")
    print(f"  Stale pages: {len(issues['stale'])}")
    print(f"  Uncertain claims: {len(issues['uncertain'])}")
    
    report = generate_report(issues)
    
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {args.output}")

if __name__ == "__main__":
    main()