#!/usr/bin/env python3
"""Fetch recent releases from Vue ecosystem repositories via GitHub API."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional
import urllib.request
import urllib.error

REPOSITORIES = [
    "vuejs/core",
    "nuxt/nuxt",
    "vitejs/vite",
    "vueuse/vueuse",
    "vuejs/pinia",
    "vuejs/router",
    "unjs/nitro",
    "nuxt/ui",
]

def fetch_releases(repo: str, days: int = 7, token: Optional[str] = None) -> list:
    """Fetch releases from a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/releases?per_page=10"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "vue-newsletter-bot/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            releases = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching {repo}: {e.code} {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"Error fetching {repo}: {e.reason}", file=sys.stderr)
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    recent = []

    for release in releases:
        published = release.get("published_at")
        if not published:
            continue

        pub_date = datetime.fromisoformat(published.replace("Z", "+00:00"))
        if pub_date < cutoff:
            continue

        recent.append({
            "tag_name": release["tag_name"],
            "name": release.get("name") or release["tag_name"],
            "published_at": published,
            "html_url": release["html_url"],
            "body": (release.get("body") or "")[:500],  # Truncate long bodies
            "prerelease": release.get("prerelease", False),
        })

    return recent


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub releases for Vue ecosystem")
    parser.add_argument("--days", type=int, default=7, help="Days to look back (default: 7)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--repos", nargs="+", help="Override default repositories")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repos = args.repos or REPOSITORIES

    results = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "github_releases",
        "days": args.days,
        "repositories": []
    }

    for repo in repos:
        releases = fetch_releases(repo, args.days, token)
        if releases:
            results["repositories"].append({
                "repo": repo,
                "releases": releases
            })

    output = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(results['repositories'])} repos to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
