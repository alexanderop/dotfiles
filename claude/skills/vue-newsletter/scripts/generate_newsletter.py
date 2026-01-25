#!/usr/bin/env python3
"""Orchestrate newsletter generation by running all fetch scripts."""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_fetcher(script_name: str, args: list = None) -> dict:
    """Run a fetcher script and return parsed JSON output."""
    script_path = SCRIPT_DIR / script_name
    cmd = [sys.executable, str(script_path)] + (args or [])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Warning: {script_name} failed: {result.stderr}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"Warning: {script_name} timed out", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: {script_name} returned invalid JSON: {e}", file=sys.stderr)
        return None


def format_releases(data: dict) -> str:
    """Format GitHub releases section."""
    if not data or not data.get("repositories"):
        return ""

    lines = ["## Releases\n"]

    repo_names = {
        "vuejs/core": "Vue.js",
        "nuxt/nuxt": "Nuxt",
        "vitejs/vite": "Vite",
        "vueuse/vueuse": "VueUse",
        "vuejs/pinia": "Pinia",
        "vuejs/router": "Vue Router",
        "unjs/nitro": "Nitro",
        "nuxt/ui": "Nuxt UI",
    }

    for repo_data in data["repositories"]:
        repo = repo_data["repo"]
        name = repo_names.get(repo, repo.split("/")[-1])
        releases = repo_data["releases"]

        if releases:
            lines.append(f"### {name}\n")
            for release in releases[:2]:  # Max 2 releases per repo
                tag = release["tag_name"]
                url = release["html_url"]
                prerelease = " (pre-release)" if release.get("prerelease") else ""
                body = release.get("body", "").split("\n")[0][:100]  # First line
                lines.append(f"- **[{tag}]({url})**{prerelease}")
                if body:
                    lines.append(f"  {body}...")
                lines.append("")

    return "\n".join(lines) if len(lines) > 1 else ""


def format_articles(data: dict) -> str:
    """Format dev.to articles section."""
    if not data or not data.get("articles"):
        return ""

    lines = ["## Community Picks\n"]

    for article in data["articles"][:7]:
        title = article["title"]
        url = article["url"]
        author = article["user"]["name"]
        desc = article.get("description", "")[:150]
        reactions = article.get("positive_reactions_count", 0)

        lines.append(f"### [{title}]({url})")
        lines.append(f"By **{author}** | {reactions} reactions")
        if desc:
            lines.append(f"\n{desc}")
        lines.append("")

    return "\n".join(lines)


def format_trending(data: dict) -> str:
    """Format GitHub trending repos section."""
    if not data or not data.get("repositories"):
        return ""

    lines = ["## Trending Repos\n"]
    lines.append("| Repository | Stars | Description |")
    lines.append("|------------|-------|-------------|")

    for repo in data["repositories"][:7]:
        name = repo["name"]
        url = repo["url"]
        stars = repo.get("stars", 0)
        stars_fmt = f"{stars:,}" if stars >= 1000 else str(stars)
        desc = repo.get("description", "")[:60]
        if len(repo.get("description", "")) > 60:
            desc += "..."

        lines.append(f"| [{name}]({url}) | {stars_fmt} | {desc} |")

    lines.append("")
    return "\n".join(lines)


def generate_tldr(releases: dict, articles: dict, trending: dict) -> str:
    """Generate TL;DR summary section."""
    highlights = []

    # Find most notable release
    if releases and releases.get("repositories"):
        for repo_data in releases["repositories"]:
            if repo_data["repo"] in ["vuejs/core", "nuxt/nuxt"]:
                for release in repo_data["releases"]:
                    if not release.get("prerelease"):
                        highlights.append(f"{repo_data['repo'].split('/')[1].title()} {release['tag_name']}")
                        break

    # Find top article
    top_article = None
    if articles and articles.get("articles"):
        top_article = articles["articles"][0]

    # Build TL;DR
    lines = ["## TL;DR\n"]

    if highlights:
        lines.append(f"> **This week:** {', '.join(highlights[:2])} released\n")
    else:
        lines.append("> **This week:** Community highlights and ecosystem updates\n")

    lines.append("**Must-read:**")
    if top_article:
        lines.append(f"- [{top_article['title']}]({top_article['url']})")
    if trending and trending.get("repositories"):
        top_repo = trending["repositories"][0]
        lines.append(f"- Trending: [{top_repo['name']}]({top_repo['url']})")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Vue newsletter")
    parser.add_argument("--days", type=int, default=7, help="Days to look back (default: 7)")
    parser.add_argument("--output", "-o", help="Output markdown file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data instead of markdown")
    parser.add_argument("--issue", type=int, help="Newsletter issue number")
    args = parser.parse_args()

    print("Fetching GitHub releases...", file=sys.stderr)
    releases = run_fetcher("fetch_github_releases.py", ["--days", str(args.days)])

    print("Fetching dev.to articles...", file=sys.stderr)
    articles = run_fetcher("fetch_devto_articles.py", ["--days", str(args.days)])

    print("Fetching GitHub trending...", file=sys.stderr)
    trending = run_fetcher("fetch_github_trending.py", ["--since", "weekly"])

    if args.json:
        output = json.dumps({
            "releases": releases,
            "articles": articles,
            "trending": trending,
        }, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
        else:
            print(output)
        return

    # Generate markdown newsletter
    today = datetime.now(timezone.utc)
    week_start = today - timedelta(days=args.days)
    date_range = f"{week_start.strftime('%b %d')} - {today.strftime('%b %d, %Y')}"
    issue_num = args.issue or 1

    frontmatter = f"""---
title: "Vue Weekly #{issue_num} - {date_range}"
description: "This week in Vue ecosystem"
type: newsletter
newsletter: vue-weekly
issueNumber: {issue_num}
tags:
  - vue
  - nuxt
  - newsletter
  - vue-weekly
authors:
  - alexander-opalic
summary: "Weekly Vue ecosystem digest"
date: {today.strftime('%Y-%m-%d')}
---
"""

    header = f"""# Vue Weekly #{issue_num}

*{date_range} | Your weekly dose of Vue ecosystem news*

"""

    sections = [
        frontmatter,
        header,
        generate_tldr(releases, articles, trending),
        format_releases(releases),
        format_articles(articles),
        format_trending(trending),
        "\n---\n\n*Curated with care. See something missing? Let me know!*\n",
    ]

    newsletter = "\n".join(s for s in sections if s)

    if args.output:
        with open(args.output, "w") as f:
            f.write(newsletter)
        print(f"Newsletter written to {args.output}", file=sys.stderr)
    else:
        print(newsletter)


if __name__ == "__main__":
    main()
