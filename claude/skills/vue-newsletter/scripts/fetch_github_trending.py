#!/usr/bin/env python3
"""Fetch trending Vue repositories from GitHub."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
import urllib.request
import urllib.error

def fetch_trending(language: str = "vue", since: str = "weekly") -> list:
    """Fetch trending repos by scraping GitHub trending page."""
    url = f"https://github.com/trending/{language}?since={since}"

    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0 (compatible; vue-newsletter-bot/1.0)",
    }

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            html = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"Error fetching trending: {e.code} {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"Error fetching trending: {e.reason}", file=sys.stderr)
        return []

    return parse_trending_html(html)


def parse_trending_html(html: str) -> list:
    """Parse GitHub trending page HTML to extract repo info."""
    repos = []

    # Find all repo articles
    repo_pattern = r'<article class="Box-row">(.*?)</article>'
    articles = re.findall(repo_pattern, html, re.DOTALL)

    for article in articles[:15]:  # Limit to 15 repos
        repo = parse_repo_article(article)
        if repo:
            repos.append(repo)

    return repos


def parse_repo_article(article: str) -> dict:
    """Parse a single repo article HTML."""
    # Extract repo name (e.g., "/vuejs/core")
    name_match = re.search(r'<h2[^>]*>.*?<a[^>]*href="(/[^"]+)"', article, re.DOTALL)
    if not name_match:
        return None

    full_name = name_match.group(1).strip("/")

    # Extract description
    desc_match = re.search(r'<p class="[^"]*col-9[^"]*"[^>]*>\s*(.*?)\s*</p>', article, re.DOTALL)
    description = ""
    if desc_match:
        description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()

    # Extract stars (total)
    stars_match = re.search(r'<a[^>]*href="[^"]*stargazers[^"]*"[^>]*>\s*([0-9,]+)', article)
    stars = 0
    if stars_match:
        stars = int(stars_match.group(1).replace(",", ""))

    # Extract stars this week/day
    stars_today_match = re.search(r'([0-9,]+)\s+stars?\s+(today|this week|this month)', article, re.IGNORECASE)
    stars_period = 0
    if stars_today_match:
        stars_period = int(stars_today_match.group(1).replace(",", ""))

    # Extract language
    lang_match = re.search(r'<span[^>]*itemprop="programmingLanguage"[^>]*>\s*(.*?)\s*</span>', article)
    language = ""
    if lang_match:
        language = lang_match.group(1).strip()

    return {
        "fullname": full_name,
        "name": full_name.split("/")[-1],
        "url": f"https://github.com/{full_name}",
        "description": description[:300],
        "stars": stars,
        "stars_period": stars_period,
        "language": language,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub trending Vue repositories")
    parser.add_argument("--since", choices=["daily", "weekly", "monthly"], default="weekly",
                        help="Time period (default: weekly)")
    parser.add_argument("--language", default="vue", help="Language filter (default: vue)")
    parser.add_argument("--limit", type=int, default=10, help="Max repos to return (default: 10)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    repos = fetch_trending(args.language, args.since)

    # Also fetch TypeScript repos tagged with vue
    if args.language == "vue":
        ts_repos = fetch_trending("typescript", args.since)
        # Filter for Vue-related TypeScript repos
        vue_ts_repos = [r for r in ts_repos if is_vue_related(r)]
        repos.extend(vue_ts_repos)

    # Sort by stars gained in period, then total stars
    repos.sort(key=lambda x: (x.get("stars_period", 0), x.get("stars", 0)), reverse=True)
    repos = repos[:args.limit]

    results = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "github_trending",
        "language": args.language,
        "since": args.since,
        "repositories": repos
    }

    output = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(repos)} repos to {args.output}", file=sys.stderr)
    else:
        print(output)


def is_vue_related(repo: dict) -> bool:
    """Check if a TypeScript repo is Vue-related based on name/description."""
    keywords = ["vue", "nuxt", "vite", "pinia", "vueuse", "vuetify", "primevue", "radix-vue"]
    text = f"{repo.get('fullname', '')} {repo.get('description', '')}".lower()
    return any(kw in text for kw in keywords)


if __name__ == "__main__":
    main()
