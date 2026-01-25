---
name: vue-newsletter
description: Generate a comprehensive Vue/Nuxt newsletter by researching 25+ sources in parallel. Use when asked to "create newsletter", "vue news", "what's new in vue", "nuxt updates", or "generate vue newsletter". Aggregates GitHub releases, Hacker News, Reddit, dev.to, official blogs, Vue-specific newsletters, podcasts, and key Vue personalities into a curated weekly digest.
---

# Vue Newsletter Generator

Generate a comprehensive Vue/Nuxt newsletter using parallel subagents to fetch from 25+ sources.

## CRITICAL: Recency Rules

**ALL content MUST be published within the last 14 days (2 weeks). NO EXCEPTIONS.**

- Articles, blog posts, tutorials: **max 14 days old**
- GitHub releases: **max 7 days old**
- Podcast episodes: **max 14 days old**
- Social media posts: **max 7 days old**
- Conference talks: **max 14 days old** (unless announcing upcoming events)

**If a source has no recent content within these windows, report "No recent content" - do NOT include older content to fill space.**

When agents return results, they MUST include publication dates. During synthesis, any item without a verifiable date within the allowed window MUST be excluded.

## Source Tiers

| Tier | Sources | Priority |
|------|---------|----------|
| 1 - Official | GitHub Releases, Vue/Nuxt/Vite/VoidZero Blogs | Highest |
| 2 - Vue Newsletters | Weekly Vue News, Vue.js Feed, Vue.js Developers | High |
| 3 - Community | Hacker News, Reddit, dev.to, Echo JS, Lobsters, **Bluesky** | High |
| 4 - Personalities | Anthony Fu, Daniel Roe, Michael Thiessen | Medium |
| 5 - Media | DejaVue Podcast, Vue Mastery, Vue School | Medium |
| 6 - Ecosystem | GitHub Trending, npm trends, Made with Vue.js | Lower |

## Workflow

### Phase 1: Determine Issue Number

```bash
ls ~/Projects/Nuxt/second-brain-nuxt/content/vue-weekly-*.md 2>/dev/null | wc -l
```

Next issue = count + 1

Also verify the newsletter publisher exists:
```bash
ls ~/Projects/Nuxt/second-brain-nuxt/content/newsletters/vue-weekly.md
```

### Phase 2: Parallel Data Collection

Spawn **11 agents IN A SINGLE MESSAGE** to fetch all sources in parallel:

---

**Agent 1 - GitHub Releases:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Fetch GitHub releases from the past 7 days for Vue ecosystem packages.

Use WebFetch to query these GitHub API endpoints (fetch them in parallel):
- https://api.github.com/repos/vuejs/core/releases?per_page=5
- https://api.github.com/repos/nuxt/nuxt/releases?per_page=5
- https://api.github.com/repos/vitejs/vite/releases?per_page=5
- https://api.github.com/repos/vueuse/vueuse/releases?per_page=5
- https://api.github.com/repos/vuejs/pinia/releases?per_page=5
- https://api.github.com/repos/vuejs/router/releases?per_page=5
- https://api.github.com/repos/nitrojs/nitro/releases?per_page=5
- https://api.github.com/repos/nuxt/ui/releases?per_page=5
- https://api.github.com/repos/unjs/h3/releases?per_page=5
- https://api.github.com/repos/vitest-dev/vitest/releases?per_page=5

For each release published in the last 7 days, extract:
- Repository name (e.g., 'Vue.js', 'Nuxt', 'Vite')
- Version tag (e.g., 'v3.6.0')
- Release date
- First 2 sentences of release notes
- Whether it's a prerelease

Return as a markdown table with columns: Package | Version | Date | Highlights | Prerelease"
```

---

**Agent 2 - Official & VoidZero Blogs:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Search for official Vue ecosystem blog posts from the past 14 days.

Use WebSearch to find recent posts from:
- 'site:blog.vuejs.org' (Vue.js official blog)
- 'site:nuxt.com/blog' (Nuxt official blog)
- 'site:vite.dev/blog' (Vite official blog)
- 'site:voidzero.dev/blog' (Evan You's company - Vite, Rolldown, Oxlint)

For each post found, extract:
- Title
- URL
- Publication date (if visible)
- 1-sentence summary of the content

Return as a bullet list with markdown links. If no recent posts found for a blog, note that."
```

---

**Agent 3 - Vue-Specific Newsletters:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Find the latest issues from Vue-specific newsletters.

Use WebSearch to find recent content from:
- 'site:weekly-vue.news' (Weekly Vue News by Mokkapps - 4,600+ subscribers)
- 'site:vuejsfeed.com' (Vue.js Feed - curated news)
- 'site:news.vuejs.org' (Official Vue News)
- 'site:vuejsdevelopers.com' (Vue.js Developers Newsletter)

For each newsletter issue or article found from the past 7 days:
- Title/Issue number
- URL
- Key topics covered
- Notable links mentioned

Return as a bullet list grouped by source."
```

---

**Agent 4 - Hacker News:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Fetch Vue-related Hacker News stories from the past 7 days.

Use WebFetch on Algolia HN API (fetch in parallel):
- https://hn.algolia.com/api/v1/search?query=vue.js&tags=story&hitsPerPage=15
- https://hn.algolia.com/api/v1/search?query=vuejs&tags=story&hitsPerPage=15
- https://hn.algolia.com/api/v1/search?query=nuxt&tags=story&hitsPerPage=15
- https://hn.algolia.com/api/v1/search?query=vite&tags=story&hitsPerPage=15
- https://hn.algolia.com/api/v1/search?query=pinia&tags=story&hitsPerPage=10

From the JSON responses, filter for:
- Stories from the last 7 days (check created_at timestamp)
- At least 5 points

Deduplicate by URL. Combine and sort by points (descending).

Return top 10 stories as a markdown table:
| Title | Points | Comments | URL |"
```

---

**Agent 5 - Reddit & Lobsters:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Fetch top posts from Vue communities on Reddit and Lobsters.

Use WebSearch to find top discussions from:
- 'site:reddit.com/r/vuejs' top posts this week
- 'site:reddit.com/r/nuxtjs' top posts this week
- 'site:lobste.rs vue OR nuxt OR vite' recent discussions

For each post with significant engagement:
- Title
- Platform (Reddit/Lobsters)
- Engagement (upvotes/points)
- URL
- Brief description of the discussion

Return top 10 combined as a markdown table:
| Title | Platform | Engagement | Link |"
```

---

**Agent 6 - dev.to Articles:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Fetch top Vue articles from dev.to this week.

Use WebFetch on dev.to API (fetch in parallel):
- https://dev.to/api/articles?tag=vue&top=7&per_page=15
- https://dev.to/api/articles?tag=nuxt&top=7&per_page=15
- https://dev.to/api/articles?tag=vite&top=7&per_page=15
- https://dev.to/api/articles?tag=vuejs&top=7&per_page=15

From the JSON responses, extract:
- title
- user.name (author)
- url
- positive_reactions_count
- comments_count
- reading_time_minutes
- description (first 100 chars)

Deduplicate by article id. Sort by positive_reactions_count descending.

Return top 10 as a markdown list:
- **[Title](url)** by Author - X reactions, Y min read
  Brief description..."
```

---

**Agent 7 - Echo JS & Frontend News:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Find Vue-related articles from JavaScript news aggregators.

Use WebFetch or WebSearch to find recent Vue content from:
- https://www.echojs.com/ (Echo JS - JavaScript news)
- 'site:frontendfoc.us vue OR nuxt OR vite' (Frontend Focus newsletter)
- 'site:javascriptweekly.com vue OR nuxt' (JavaScript Weekly)

For each Vue-related article found from the past 7 days:
- Title
- Source
- URL
- Brief description

Return as a bullet list, max 10 items."
```

---

**Agent 8 - Key Vue Personalities:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Search for blog posts from Vue ecosystem leaders published in the LAST 14 DAYS ONLY.

CRITICAL: Today's date is [INSERT_TODAY_DATE]. Only include posts published after [INSERT_14_DAYS_AGO].
If you cannot verify a post was published within this window, EXCLUDE it.

Use WebSearch to find recent posts:
- 'site:antfu.me' (Anthony Fu - VueUse creator, Vite/Vue core team)
- 'site:roe.dev' (Daniel Roe - Nuxt lead maintainer)
- 'site:michaelnthiessen.com' (Michael Thiessen - Vue tips expert)
- 'site:vueschool.io/articles' (Vue School tutorials)
- 'site:masteringnuxt.com' (Mastering Nuxt)
- 'site:learnvue.co' (LearnVue tutorials)

For each post found, extract:
- Title
- Author/Source
- URL
- **Publication date (REQUIRED - exclude if not verifiable)**
- Brief description of the topic

IMPORTANT: If a site has no posts from the last 14 days, report 'No recent content from [source]' - do NOT include older posts.

Return as a bullet list grouped by author with dates."
```

---

**Agent 9 - Podcasts & Video:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Find recent Vue podcast episodes and video content.

Use WebSearch for:
- 'site:dejavue.fm' recent episodes (DejaVue podcast - Michael Thiessen & Alexander Lichter)
- 'Views on Vue podcast' latest episodes
- 'site:vuemastery.com' new courses or videos
- 'Vue.js conference talks 2025 2026'

For each episode/video found from the past 14 days:
- Title
- Source (podcast name or channel)
- URL
- Guest (if applicable)
- Brief topic description

Return as a bullet list grouped by source."
```

---

**Agent 10 - Trending & Ecosystem:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Find trending Vue repositories, new packages, and ecosystem updates.

Use WebSearch for:
- 'github trending vue repositories this week'
- 'github trending nuxt repositories'
- 'new vue npm packages'
- 'site:madewithvuejs.com' recent showcases
- 'site:npmtrends.com vue' popular comparisons

Extract up to 15 notable items:
- Repository/package name
- GitHub URL or npm link
- Star count (if available)
- Brief description
- Why it's trending/notable

Return as a markdown table:
| Name | Stars | Description | Link |"
```

---

**Agent 11 - Bluesky:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Fetch Vue/Nuxt discussions from Bluesky using the authenticated API.

STEP 1: Authenticate with Bluesky API
Run this bash command to get an access token:
```bash
curl -s -X POST https://bsky.social/xrpc/com.atproto.server.createSession \
  -H 'Content-Type: application/json' \
  -d '{\"identifier\":\"'$BLUESKY_HANDLE'\",\"password\":\"'$BLUESKY_APP_PASSWORD'\"}' \
  | python3 -c \"import sys,json; print(json.load(sys.stdin)['accessJwt'])\"
```

STEP 2: Search for Vue/Nuxt posts (run these searches with the token)
Use Bash to call the search API with the token from step 1:
- Search 'nuxt' - limit 20
- Search 'vue.js' - limit 20
- Search 'vite' - limit 15
- Search '#vue' hashtag - limit 15

API endpoint: https://bsky.social/xrpc/app.bsky.feed.searchPosts?q={query}&limit={limit}
Header: Authorization: Bearer {token}

STEP 3: Parse and filter results
From the JSON responses, extract posts with:
- 3+ likes (likeCount)
- From the last 7 days (check createdAt)

For each qualifying post, extract:
- Author handle
- Post text (first 100 chars)
- Like count
- Repost count
- Post URL (format: https://bsky.app/profile/{author}/post/{postId})
- Created date

Deduplicate by post URI. Sort by likes descending.

Return top 10 posts as markdown:
| Author | Likes | Text | Link |"
```

---

**Collect all results** using TaskOutput (blocking) for each agent.

### Phase 3: Content Synthesis

After collecting all data, spawn 2 agents **IN A SINGLE MESSAGE**:

---

**Agent 12 - Section Compiler:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Compile the following raw data into newsletter sections.

CRITICAL DATE FILTER: Today is [INSERT_TODAY_DATE].
- Releases: ONLY from last 7 days (after [INSERT_7_DAYS_AGO])
- Articles/Tutorials: ONLY from last 14 days (after [INSERT_14_DAYS_AGO])
- Podcasts/Videos: ONLY from last 14 days
- Social posts: ONLY from last 7 days

**EXCLUDE any content older than these windows. Better to have fewer items than stale content.**

RAW DATA:
{paste all agent outputs here}

Create these sections in order:
1. ## Releases - Group by package, max 2 releases per package (7 days max)
2. ## Official Announcements - From official blogs, VoidZero (14 days max)
3. ## Community Highlights - Best from HN, Reddit, Lobsters, Bluesky, max 10 items (7 days max)
4. ## Articles & Tutorials - From dev.to, Echo JS, personalities, newsletters, max 10 items (14 days max)
5. ## Podcast & Video - Recent episodes and talks, max 5 items (14 days max)
6. ## Trending Repos - Top 5 trending repositories (this week only)
7. ## Project Showcase - Notable projects from Made with Vue.js, max 3 (14 days max)

Rules:
- **STRICT: Exclude ANY item without a verifiable date within the allowed window**
- Deduplicate: same article appearing on multiple platforms = keep once with highest engagement
- Use markdown links for all URLs
- Keep descriptions concise (1 line max)
- Add brief editorial comment for standout items
- Prioritize: Official > Newsletter picks > HN > Reddit > dev.to
- If a section has no qualifying content, write 'No recent [section type] this week'

Return the compiled markdown sections."
```

---

**Agent 13 - TL;DR Generator:**

```
Task tool with subagent_type: "general-purpose"
prompt: "Generate a TL;DR summary for this newsletter.

NEWSLETTER CONTENT:
{paste compiled sections}

Create:
1. A 1-sentence 'This week in Vue' summary
2. 3-5 bullet points of 'Must-Read' highlights with links
3. A 'Week Theme' if there's a common thread (optional)
4. Any breaking changes or security advisories to highlight

Format as:
## TL;DR

> **This week:** [summary sentence]

**Must-read:**
- [Highlight 1](link)
- [Highlight 2](link)
...

**Week theme:** [theme if applicable]"
```

---

### Phase 4: Assemble Newsletter

Combine all parts into the final newsletter with this structure:

```markdown
---
title: "Vue Weekly #[N] - [START_DATE] - [END_DATE]"
description: "This week in Vue ecosystem"
type: newsletter
newsletter: vue-weekly
issueNumber: [N]
tags:
  - vue
  - nuxt
  - newsletter
  - vue-weekly
authors:
  - alexander-opalic
summary: "[1-sentence summary from TL;DR]"
date: [YYYY-MM-DD]
---

# Vue Weekly #[N]

*[DATE_RANGE] | Your weekly dose of Vue ecosystem news*

[TL;DR section]

[Releases section]

[Official Announcements section - if any]

[Community Highlights section]

[Articles & Tutorials section]

[Podcast & Video section - if any]

[Trending Repos section]

[Project Showcase section - if any]

---

*Curated with care. Found something interesting? Reply to share!*
```

### Phase 5: User Review (BLOCKING GATE)

Present the assembled newsletter to the user.

Use AskUserQuestion tool with options:
- "Looks good - save it"
- "I want to edit some sections"
- "Add more content to a section"
- "Remove some items"

**Do NOT save without explicit user approval.**

### Phase 6: Save & Integrate

After approval, write to:
```
~/Projects/Nuxt/second-brain-nuxt/content/vue-weekly-[N].md
```

Verify the file was created:
```bash
head -20 ~/Projects/Nuxt/second-brain-nuxt/content/vue-weekly-[N].md
```

## Fallback: Python Scripts

If API fetching fails, use the legacy Python scripts as fallback:

```bash
# GitHub releases only
python3 ~/.claude/skills/vue-newsletter/scripts/fetch_github_releases.py

# dev.to articles only
python3 ~/.claude/skills/vue-newsletter/scripts/fetch_devto_articles.py --days 7 --limit 10

# Full generation (limited sources)
python3 ~/.claude/skills/vue-newsletter/scripts/generate_newsletter.py --issue [N]
```

## API Rate Limits

| Source | Endpoint | Limit |
|--------|----------|-------|
| GitHub | api.github.com | 60/hr (5000 with GITHUB_TOKEN) |
| Hacker News | hn.algolia.com | Unlimited |
| Reddit | reddit.com/*.json | Blocked by WebFetch - use WebSearch |
| dev.to | dev.to/api | 30/min |
| Bluesky | bsky.social/xrpc | 3000/5min (authenticated) |
| Echo JS | echojs.com | No limit (scraping) |
| Lobsters | lobste.rs | No limit (scraping) |

## Bluesky Authentication

Requires environment variables (already configured in ~/.zshrc):
- `BLUESKY_HANDLE` - Your Bluesky handle (e.g., alexvue.bsky.social)
- `BLUESKY_APP_PASSWORD` - App password from bsky.app/settings/app-passwords

The agent authenticates via `com.atproto.server.createSession` to get a JWT token,
then uses `app.bsky.feed.searchPosts` to search for Vue/Nuxt posts.

## Ranking Algorithm

When deduplicating/ranking content:

```
score = engagement + recency_bonus + source_weight

engagement:
  HN: points + (comments * 0.5)
  Reddit: upvotes + (comments * 0.3)
  Lobsters: points + (comments * 0.5)
  Bluesky: likes + (reposts * 2)
  dev.to: reactions + (comments * 2)

recency_bonus:
  < 1 day old: +20
  1-3 days: +10
  3-7 days: +0
  7-14 days: -10 (articles/podcasts only)
  > 14 days: EXCLUDE (do not include)

source_weight:
  Official blog: +50
  VoidZero blog: +45
  Weekly Vue News pick: +40
  Key personality: +30
  Hacker News: +20
  Bluesky: +18
  Lobsters: +15
  Reddit: +10
  dev.to: +5
  Echo JS: +5
```

## Second Brain Integration

The newsletter uses these frontmatter fields:
- `type: newsletter` - Content type
- `newsletter: vue-weekly` - Links to publisher
- `issueNumber: N` - Sequential issue number
- `authors: [alexander-opalic]` - Curator

Publisher file at `content/newsletters/vue-weekly.md` must exist.

## Social Accounts to Monitor

For manual additions or future automation:

| Platform | Account | Notes |
|----------|---------|-------|
| Twitter/X | @vuejs, @nuaboratory | Official accounts |
| Twitter/X | @youyuxi, @antfu7, @danielcroe | Core team |
| Bluesky | @nuxt.com | Official Nuxt account |
| Bluesky | @danielroe.dev | Nuxt lead, 13k+ followers |
| Bluesky | @madewithvuejs.com | Vue project showcases |
| Discord | Vue Land (122k), Nuxt (32k) | Community discussions |

### Bluesky Search Queries Used

The agent searches these terms:
- `nuxt` - Nuxt framework discussions
- `vue.js` - Vue.js discussions
- `vite` - Vite build tool
- `#vue` - Vue hashtag
