#!/usr/bin/env python3
"""Fetch top Vue/Nuxt articles from dev.to via Forem API."""

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Optional
import urllib.request
import urllib.error

TAGS = ["vue", "nuxt", "vite", "vuejs", "nuxtjs"]

def fetch_articles(tag: str, top: int = 7, per_page: int = 15) -> list:
    """Fetch top articles for a tag from dev.to."""
    url = f"https://dev.to/api/articles?tag={tag}&top={top}&per_page={per_page}"

    headers = {
        "Accept": "application/json",
        "User-Agent": "vue-newsletter-bot/1.0",
    }

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            articles = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching tag {tag}: {e.code} {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"Error fetching tag {tag}: {e.reason}", file=sys.stderr)
        return []

    results = []
    for article in articles:
        results.append({
            "id": article["id"],
            "title": article["title"],
            "url": article["url"],
            "published_at": article["published_at"],
            "user": {
                "name": article["user"]["name"],
                "username": article["user"]["username"],
            },
            "tags": article.get("tag_list", []),
            "positive_reactions_count": article.get("positive_reactions_count", 0),
            "comments_count": article.get("comments_count", 0),
            "reading_time_minutes": article.get("reading_time_minutes", 0),
            "description": article.get("description", "")[:200],
            "score": calculate_score(article),
        })

    return results


def calculate_score(article: dict) -> float:
    """Calculate engagement score for article."""
    reactions = article.get("positive_reactions_count", 0)
    comments = article.get("comments_count", 0)
    return reactions + (comments * 2)


def deduplicate_articles(articles: list) -> list:
    """Remove duplicate articles by ID, keeping highest score."""
    seen = {}
    for article in articles:
        article_id = article["id"]
        if article_id not in seen or article["score"] > seen[article_id]["score"]:
            seen[article_id] = article
    return sorted(seen.values(), key=lambda x: x["score"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Fetch dev.to articles for Vue ecosystem")
    parser.add_argument("--days", type=int, default=7, help="Top articles from N days (default: 7)")
    parser.add_argument("--limit", type=int, default=10, help="Max articles to return (default: 10)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--tags", nargs="+", help="Override default tags")
    parser.add_argument("--min-score", type=float, default=5, help="Minimum score threshold (default: 5)")
    args = parser.parse_args()

    tags = args.tags or TAGS
    all_articles = []

    for tag in tags:
        articles = fetch_articles(tag, top=args.days, per_page=20)
        all_articles.extend(articles)

    # Deduplicate and filter
    unique_articles = deduplicate_articles(all_articles)
    filtered = [a for a in unique_articles if a["score"] >= args.min_score]
    top_articles = filtered[:args.limit]

    results = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "devto",
        "tags_searched": tags,
        "days": args.days,
        "total_found": len(all_articles),
        "after_dedup": len(unique_articles),
        "articles": top_articles
    }

    output = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(top_articles)} articles to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
