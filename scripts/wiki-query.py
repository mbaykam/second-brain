#!/usr/bin/env python3
"""
Wiki Query Script
Query the wiki and file answers back to grow the knowledge base.
Usage: python3 wiki-query.py "Your question here" [--file-back]
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path("/home/mete/.openclaw/workspace/second-brain-vault")

def find_relevant_pages(query, limit=5):
    """Find wiki pages relevant to the query using simple keyword matching."""
    query_terms = set(re.findall(r'\w+', query.lower()))
    
    matches = []
    for category in ["concepts", "entities", "skills", "references", "synthesis"]:
        cat_path = VAULT_PATH / category
        if not cat_path.exists():
            continue
        
        for filepath in cat_path.glob("*.md"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Simple scoring: count matching terms
                score = sum(1 for term in query_terms if term in content)
                if score > 0:
                    matches.append({
                        "path": filepath,
                        "relative": filepath.relative_to(VAULT_PATH),
                        "score": score
                    })
            except:
                continue
    
    # Sort by score and return top matches
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:limit]

def extract_page_content(filepath, max_chars=2000):
    """Extract relevant content from a wiki page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove frontmatter
        content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)
        
        # Return first N chars
        return content[:max_chars].strip()
    except:
        return ""

def file_back_answer(question, answer, category="synthesis"):
    """File the answer back into the wiki as a new page."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M")
    
    # Create slug from question
    slug = re.sub(r'[^\w\s-]', '', question.lower())[:50]
    slug = re.sub(r'[-\s]+', '_', slug).strip('_')
    
    filename = f"q_{date_str}_{slug}.md"
    filepath = VAULT_PATH / category / filename
    
    # Ensure directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    frontmatter = f"""---
title: "Q: {question}"
category: {category}
created: {date_str}
updated: {date_str}
confidence: high
query_type: faq
provenance:
  - wiki_query
---

"""
    
    content = f"""## Question

{question}

## Answer

{answer}

## Related Pages

"""
    
    with open(filepath, 'w') as f:
        f.write(frontmatter + content)
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Query the wiki")
    parser.add_argument("query", help="Your question")
    parser.add_argument("--file-back", "-f", action="store_true", help="File the answer back to wiki")
    parser.add_argument("--category", "-c", default="synthesis", help="Category for filed answers")
    
    args = parser.parse_args()
    
    print(f"Query: {args.query}\n")
    
    # Find relevant pages
    pages = find_relevant_pages(args.query)
    
    if not pages:
        print("No relevant pages found in the wiki.")
        return
    
    print(f"Found {len(pages)} relevant pages:\n")
    
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['relative']} (relevance: {page['score']})")
        content = extract_page_content(page['path'], 500)
        if content:
            print(f"   Preview: {content[:200]}...")
        print()
    
    if args.file_back:
        print("\n[Use with an LLM to generate an answer, then file it back]")
        print("Example workflow:")
        print("  1. Read the relevant pages above")
        print("  2. Ask an LLM to answer based on that content")
        print("  3. File back: python3 wiki-query.py 'question' --file-back")

if __name__ == "__main__":
    main()