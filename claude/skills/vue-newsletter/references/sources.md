# Vue Newsletter Sources Configuration

Complete list of 25+ sources for the Vue Weekly newsletter, organized by tier.

## Tier 1: Official Sources (Highest Priority)

### GitHub Releases

| Package | Repository | API Endpoint |
|---------|------------|--------------|
| Vue.js | vuejs/core | api.github.com/repos/vuejs/core/releases |
| Nuxt | nuxt/nuxt | api.github.com/repos/nuxt/nuxt/releases |
| Vite | vitejs/vite | api.github.com/repos/vitejs/vite/releases |
| VueUse | vueuse/vueuse | api.github.com/repos/vueuse/vueuse/releases |
| Pinia | vuejs/pinia | api.github.com/repos/vuejs/pinia/releases |
| Vue Router | vuejs/router | api.github.com/repos/vuejs/router/releases |
| Nitro | nitrojs/nitro | api.github.com/repos/nitrojs/nitro/releases |
| Nuxt UI | nuxt/ui | api.github.com/repos/nuxt/ui/releases |
| H3 | unjs/h3 | api.github.com/repos/unjs/h3/releases |
| Vitest | vitest-dev/vitest | api.github.com/repos/vitest-dev/vitest/releases |

### Official Blogs

| Blog | URL | Feed | Notes |
|------|-----|------|-------|
| Vue.js Blog | blog.vuejs.org | blog.vuejs.org/feed.rss | Major announcements |
| Nuxt Blog | nuxt.com/blog | nuxt.com/blog/rss.xml | Nuxt releases, features |
| Vite Blog | vite.dev/blog | (no RSS, use WebSearch) | Vite releases |
| VoidZero Blog | voidzero.dev/blog | (scrape) | Evan You's company - Vite, Rolldown, Oxlint |

## Tier 2: Vue-Specific Newsletters (High Priority)

| Newsletter | URL | Subscribers | Access | Notes |
|------------|-----|-------------|--------|-------|
| Weekly Vue News | weekly-vue.news | 4,600+ | RSS, Telegram, Discord | By Mokkapps, excellent curation |
| Vue.js Feed | vuejsfeed.com | - | RSS | 63 pages of curated content |
| Official Vue News | news.vuejs.org | - | RSS | Official Vue.js news portal |
| Vue.js Developers | vuejsdevelopers.com/newsletter | - | Archives | By Anthony Gore, since 2017 |

## Tier 3: Community News (High Priority)

### Hacker News

**API:** Algolia HN Search API (no auth required, unlimited)

```
Base URL: https://hn.algolia.com/api/v1/search
Parameters:
  - query: search term
  - tags: story (filter to stories only)
  - hitsPerPage: 15-20
  - numericFilters: created_at_i>[timestamp] (filter by date)
```

**Search Queries:**
- `vue.js`
- `vuejs`
- `nuxt`
- `vite`
- `pinia`

**Filter Criteria:**
- Minimum 5 points
- Published in last 7 days
- Deduplicate by URL

### Reddit

**Note:** WebFetch blocked - use WebSearch instead

| Subreddit | Members | URL |
|-----------|---------|-----|
| r/vuejs | ~100k | reddit.com/r/vuejs |
| r/nuxtjs | ~15k | reddit.com/r/nuxtjs |

**Filter Criteria:**
- Minimum 10 upvotes
- Top posts from past week
- Combine both subreddits

### Lobsters

**URL:** lobste.rs/t/javascript

**Access:** Scraping (invitation-only community, high quality)

**Search:** `vue OR nuxt OR vite`

### dev.to

**API:** Forem API (no auth, 30 req/min)

```
Base URL: https://dev.to/api/articles
Parameters:
  - tag: vue, nuxt, vite, vuejs, nuxtjs
  - top: 7 (top articles from last 7 days)
  - per_page: 15
```

### Echo JS

**URL:** echojs.com

**Access:** Scraping (no API)

**Relevance:** General JS news, Vue articles appear regularly

### Frontend Newsletters

| Newsletter | URL | Notes |
|------------|-----|-------|
| Frontend Focus | frontendfoc.us | 723 issue archive, RSS available |
| JavaScript Weekly | javascriptweekly.com | 170k+ subscribers, covers Vue |

## Tier 4: Key Personalities (Medium Priority)

| Person | Role | Blog URL | Content Type |
|--------|------|----------|--------------|
| Anthony Fu | VueUse creator, Vite/Vue core | antfu.me | Technical deep-dives |
| Daniel Roe | Nuxt lead maintainer | roe.dev | Nuxt insights |
| Michael Thiessen | Vue educator | michaelnthiessen.com | Vue tips, patterns |
| Evan You | Vue/Vite creator | evanyou.me | Rare but important |

### Educational Platforms

| Platform | URL | Content Type |
|----------|-----|--------------|
| Vue School | vueschool.io/articles | Tutorials, news |
| Vue Mastery | vuemastery.com/blog | Courses, tutorials |
| Mastering Nuxt | masteringnuxt.com | Nuxt tutorials |
| LearnVue | learnvue.co | Vue tutorials |

## Tier 5: Podcasts & Video (Medium Priority)

### Podcasts

| Podcast | Status | Hosts | URL | Notes |
|---------|--------|-------|-----|-------|
| DejaVue | Active | Michael Thiessen, Alexander Lichter | dejavue.fm | Weekly, guests like Evan You, Daniel Roe |
| Views on Vue | Active | Erik, Steve | Spotify/Apple | 257+ episodes |
| The Official Vue News | Active | Vue Mastery | vuemastery.com | Short 5-minute updates |
| Enjoy the Vue | Hiatus | Various | - | 93 episodes in archive |

### YouTube Channels

| Channel | Focus | Subscribers |
|---------|-------|-------------|
| Vue Mastery | Vue tutorials | 61.5K |
| Vue School | Vue/Nuxt courses | - |
| LearnVue | Vue tutorials | - |
| Program with Erik | Vue.js tutorials | - |

### Conferences

| Event | Dates | URL |
|-------|-------|-----|
| Vue.js Amsterdam | March 12-13, 2025 | vuejs.amsterdam |
| VueConf US | May 19-21, 2025 | - |
| Nuxt Nation | TBD 2025 | - |
| Vue.js Nation | Jan 29-30, 2025 | events.vuejs.org |
| ViteConf | October 10, 2025 | viteconf.amsterdam |

## Tier 6: Ecosystem (Lower Priority)

### GitHub Trending

**Method:** WebSearch (no direct API)

Search queries:
- `github trending vue repositories this week`
- `github trending nuxt repositories`
- `github trending typescript vue`

### Package Trackers

| Tool | URL | Access | Data Available |
|------|-----|--------|----------------|
| npm trends | npmtrends.com | Scraping | Download comparisons |
| Bundlephobia | bundlephobia.com | API/CLI | Package size analysis |
| Star History | star-history.com | GitHub API | Star count over time |

### Project Showcases

| Platform | URL | Content |
|----------|-----|---------|
| Made with Vue.js | madewithvuejs.com | Project gallery |
| Vue.js Examples | vuejsexamples.com | Code examples |
| Vue.js Projects | vuejsprojects.com | Examples, components |

## Social Media Accounts

### Twitter/X

| Account | Handle | Role |
|---------|--------|------|
| Vue.js Official | @vuejs | Official account |
| Evan You | @youyuxi | Vue creator |
| Anthony Fu | @antfu7 | Vue core team |
| Daniel Roe | @danielcroe | Nuxt lead |
| Vue Newsletter | @VueNewsletter | Official news |

### Bluesky (Authenticated API)

**API:** AT Protocol - `app.bsky.feed.searchPosts`

```
Base URL: https://bsky.social/xrpc/app.bsky.feed.searchPosts
Authentication: Required (App Password + createSession)
Rate Limit: 3000 requests per 5 minutes

Parameters:
  - q: search query (supports OR, hashtags, from:user)
  - limit: results per page (max 100)
  - since: YYYY-MM-DDTHH:MM:SSZ
  - until: YYYY-MM-DDTHH:MM:SSZ
```

**Search Queries:**
- `nuxt`
- `vue.js`
- `vite`
- `#vue`

**Filter Criteria:**
- Minimum 3 likes
- Published in last 7 days
- Deduplicate by post URI

**Key Accounts:**

| Account | Handle | Notes |
|---------|--------|-------|
| Nuxt Official | @nuxt.com | Official Nuxt account |
| Daniel Roe | @danielroe.dev | Nuxt lead, 13k+ followers |
| Made with Vue.js | @madewithvuejs.com | Project showcases |
| Vue Starter Pack | thealexlichter.com | Curated developer list |

### Discord

| Server | Members | Invite |
|--------|---------|--------|
| Vue Land | 122,444 | discord.gg/vue |
| Nuxt | 31,866 | discord.com/invite/nuxt |
| Nuxt Content | 893 | discord.com/invite/sBXDm6e8SP |

### Mastodon

| Resource | URL |
|----------|-----|
| FediDevs Vue | fedidevs.com/vue/ |

## API Authentication

| Service | Auth Required | Rate Limit | How to Get |
|---------|---------------|------------|------------|
| GitHub | Optional | 60/hr → 5000/hr | github.com/settings/tokens |
| Hacker News | No | Unlimited | N/A |
| Reddit | No (JSON) | Blocked by WebFetch | Use WebSearch |
| Bluesky | Yes (App Password) | 3000/5min | bsky.app/settings/app-passwords |
| dev.to | No | 30/min | N/A |
| Echo JS | No | No limit | N/A |
| Lobsters | No | No limit | N/A |

## WebFetch Accessibility

| Source | Status | Notes |
|--------|--------|-------|
| GitHub API | Accessible | JSON responses |
| Hacker News API | Accessible | JSON responses |
| Reddit | Blocked | Use WebSearch instead |
| dev.to API | Accessible | JSON responses |
| Bluesky API | Requires Auth | Use Bash with curl (env vars in ~/.zshrc) |
| Echo JS | Accessible | HTML scraping |
| Lobsters | Accessible | HTML scraping |
| Weekly Vue News | Accessible | RSS/HTML |
| VoidZero Blog | Accessible | HTML |
| Vue.js Feed | Accessible | RSS/HTML |
| DejaVue | Accessible | RSS |
| npm trends | Accessible | HTML scraping |

## Source Quality Guidelines

### High Quality Indicators
- Official announcement from core team
- High engagement (100+ points/upvotes)
- From known Vue ecosystem contributor
- Covers new release or feature
- Practical tutorial with code examples
- Picked by Weekly Vue News or similar curated newsletter

### Low Quality Indicators
- Clickbait titles
- Outdated content (references Vue 2 without migration context)
- Low engagement despite being old
- Duplicate/repost of existing content
- Pure promotion without educational value

## Deduplication Rules

1. **Same URL on multiple platforms:** Keep the one with highest engagement
2. **Same topic, different articles:** Keep the most comprehensive one
3. **Official + community coverage:** Keep both if they add different value
4. **Cross-posted by author:** Keep original source only
5. **Newsletter picks:** Prioritize items featured in Weekly Vue News

## Reports & Surveys

| Resource | URL | Frequency |
|----------|-----|-----------|
| State of Vue.js Report | monterail.com/stateofvue | Annual |
| State of JS Survey | stateofjs.com | Annual |
