#!/usr/bin/env python3
"""
Wiki Ingestion Script
Processes raw sources and compiles them into wiki pages.
Usage: python3 wiki-ingest.py [--source PATH] [--type TYPE]
"""

import os
import sys
import json
import re
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

VAULT_PATH = Path("/home/mete/.openclaw/workspace/second-brain-vault")
RAW_PATH = VAULT_PATH / "_raw"
MANIFEST_FILE = VAULT_PATH / ".manifest.json"

# Content type detectors
CONTENT_PATTERNS = {
    "transcript": [r"speaker:", r"transcript", r"\[\d{2}:\d{2}:\d{2}\]"],
    "paper": [r"abstract", r"introduction", r"references", r"doi:"],
    "article": [r"published", r"author:", r"url:"],
    "tweet_thread": [r"@\w+", r"#\w+", r"\n\d+\.\s+"],
    "meeting": [r"attendees:", r"agenda:", r"action items:"],
}

def load_manifest():
    """Load the ingestion manifest."""
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, 'r') as f:
            return json.load(f)
    return {"ingested": [], "last_update": None}

def save_manifest(manifest):
    """Save the ingestion manifest."""
    manifest["last_update"] = datetime.now().isoformat()
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2)

def compute_hash(filepath):
    """Compute MD5 hash of file content."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def detect_content_type(content):
    """Detect the type of content."""
    content_lower = content.lower()
    scores = {}
    
    for content_type, patterns in CONTENT_PATTERNS.items():
        score = sum(1 for pattern in patterns if re.search(pattern, content_lower))
        if score > 0:
            scores[content_type] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "note"

def slugify(text):
    """Convert text to URL-safe slug."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')

def create_wiki_page(title, category, content, source_path=None):
    """Create a properly formatted wiki page."""
    now = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    
    frontmatter = f"""---
title: {title}
category: {category}
created: {now}
updated: {now}
confidence: medium
provenance:
  - {source_path or 'manual'}
---

"""
    
    # Add backlinks section at end
    backlinks = f"""

## Related

<!-- Auto-generated cross-references -->
- [[index]]

## Sources

- {source_path or 'manual entry'}
"""
    
    return frontmatter + content + backlinks

def ingest_file(filepath, file_type=None):
    """Ingest a single file into the wiki."""
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return False
    
    # Check if already ingested
    manifest = load_manifest()
    file_hash = compute_hash(filepath)
    
    for entry in manifest["ingested"]:
        if entry.get("hash") == file_hash:
            print(f"Skipping: Already ingested ({filepath.name})")
            return False
    
    # Read and process content
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Auto-detect type if not specified
    if not file_type:
        file_type = detect_content_type(content)
    
    # Extract title from first heading or filename
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = filepath.stem.replace('_', ' ').title()
    
    # Determine category folder
    category_map = {
        "transcript": "references",
        "paper": "references",
        "article": "references",
        "tweet_thread": "references",
        "meeting": "journal",
        "note": "concepts",
    }
    category = category_map.get(file_type, "concepts")
    
    # Create wiki page
    wiki_content = create_wiki_page(title, category, content, str(filepath))
    output_path = VAULT_PATH / category / f"{slugify(title)}.md"
    
    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    with open(output_path, 'w') as f:
        f.write(wiki_content)
    
    # Update manifest
    manifest["ingested"].append({
        "source": str(filepath),
        "hash": file_hash,
        "output": str(output_path),
        "type": file_type,
        "date": datetime.now().isoformat()
    })
    save_manifest(manifest)
    
    print(f"✓ Ingested: {filepath.name} → {output_path.relative_to(VAULT_PATH)}")
    return True

def process_raw_folder():
    """Process all files in the _raw folder."""
    if not RAW_PATH.exists():
        print(f"Raw folder not found: {RAW_PATH}")
        return
    
    processed = 0
    for filepath in RAW_PATH.iterdir():
        if filepath.is_file() and filepath.suffix in ['.md', '.txt']:
            if ingest_file(filepath):
                processed += 1
    
    print(f"\nProcessed {processed} new files")

def update_index():
    """Update the main index.md with current wiki state."""
    index_path = VAULT_PATH / "index.md"
    
    # Collect all pages
    pages = []
    for category in ["concepts", "entities", "skills", "references", "synthesis"]:
        cat_path = VAULT_PATH / category
        if cat_path.exists():
            for filepath in cat_path.glob("*.md"):
                pages.append({
                    "title": filepath.stem.replace('_', ' ').title(),
                    "category": category,
                    "path": f"{category}/{filepath.name}"
                })
    
    # Build index content
    content = f"""---
title: Wiki Index
category: meta
created: 2026-04-17
updated: {datetime.now().strftime("%Y-%m-%d")}
---

# Wiki Index

Auto-generated catalog of all wiki pages.

Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Stats

- Total pages: {len(pages)}
- Concepts: {len([p for p in pages if p['category'] == 'concepts'])}
- Entities: {len([p for p in pages if p['category'] == 'entities'])}
- Skills: {len([p for p in pages if p['category'] == 'skills'])}
- References: {len([p for p in pages if p['category'] == 'references'])}

## Pages by Category

"""
    
    # Group by category
    by_category = {}
    for page in pages:
        cat = page["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(page)
    
    for category, cat_pages in sorted(by_category.items()):
        content += f"\n### {category.title()}\n\n"
        for page in sorted(cat_pages, key=lambda x: x["title"]):
            content += f"- [[{page['path'].replace('.md', '')}|{page['title']}]]\n"
    
    with open(index_path, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated index: {len(pages)} pages")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wiki ingestion script")
    parser.add_argument("--source", "-s", help="Specific file to ingest")
    parser.add_argument("--type", "-t", help="Content type (transcript, paper, article, etc.)")
    parser.add_argument("--index", "-i", action="store_true", help="Update index only")
    parser.add_argument("--all", "-a", action="store_true", help="Process all files in _raw folder")
    
    args = parser.parse_args()
    
    if args.index:
        update_index()
    elif args.source:
        ingest_file(args.source, args.type)
        update_index()
    elif args.all:
        process_raw_folder()
        update_index()
    else:
        # Default: process raw folder
        process_raw_folder()
        update_index()