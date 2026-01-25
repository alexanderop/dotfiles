# Vue Newsletter Ranking Algorithm

How content is scored and ranked for inclusion in Vue Weekly.

## Scoring Formula

```
total_score = base_engagement + recency_bonus + source_weight + quality_bonus
```

## Base Engagement Scores

### Hacker News
```
score = points + (comments * 0.5)

Example:
  - 50 points, 20 comments = 50 + 10 = 60
  - 100 points, 5 comments = 100 + 2.5 = 102.5
```

### Reddit
```
score = upvotes + (comments * 0.3)

Example:
  - 100 upvotes, 30 comments = 100 + 9 = 109
  - 50 upvotes, 100 comments = 50 + 30 = 80
```

### dev.to
```
score = reactions + (comments * 2)

Example:
  - 42 reactions, 8 comments = 42 + 16 = 58
  - 20 reactions, 15 comments = 20 + 30 = 50
```

### GitHub Releases
```
score = 100 (fixed - always high priority)

Prerelease modifier: -20
```

### GitHub Trending
```
score = stars_gained_this_week + (total_stars * 0.01)

Example:
  - 500 stars this week, 10000 total = 500 + 100 = 600
  - 100 stars this week, 50000 total = 100 + 500 = 600
```

## Recency Bonus

| Age | Bonus |
|-----|-------|
| < 24 hours | +20 |
| 1-3 days | +10 |
| 3-5 days | +5 |
| 5-7 days | +0 |
| > 7 days | -10 |

## Source Weight

| Source Type | Weight |
|-------------|--------|
| Official blog post | +50 |
| Key personality blog | +30 |
| Hacker News | +20 |
| Reddit | +10 |
| dev.to | +5 |
| GitHub trending | +5 |

## Quality Bonus

| Indicator | Bonus |
|-----------|-------|
| From Vue/Nuxt/Vite core team member | +25 |
| Major release announcement | +20 |
| Includes code examples | +10 |
| Video/interactive content | +10 |
| Breaking changes covered | +15 |
| Migration guide included | +15 |

## Ranking Examples

### Example 1: Vue 3.5 Release Post on HN
```
Base engagement: 150 points + (80 * 0.5) = 190
Recency: posted today = +20
Source: HN = +20
Quality: major release = +20
TOTAL: 250
```

### Example 2: Tutorial on dev.to
```
Base engagement: 45 reactions + (12 * 2) = 69
Recency: 3 days ago = +5
Source: dev.to = +5
Quality: code examples = +10
TOTAL: 89
```

### Example 3: Anthony Fu Blog Post
```
Base engagement: N/A (blog, use fixed 50)
Recency: 2 days ago = +10
Source: key personality = +30
Quality: from core team = +25
TOTAL: 115
```

### Example 4: Reddit Discussion
```
Base engagement: 85 upvotes + (45 * 0.3) = 98.5
Recency: 5 days ago = +0
Source: Reddit = +10
Quality: none
TOTAL: 108.5
```

## Section Quotas

After ranking, select top items per section:

| Section | Max Items | Selection Criteria |
|---------|-----------|-------------------|
| Releases | All from past 7 days | Max 2 per package |
| Official Announcements | 3 | Only if found |
| Community Highlights | 8 | Top HN + Reddit combined |
| Articles & Tutorials | 8 | Top dev.to + personalities |
| Trending Repos | 5 | Top by stars gained |

## Deduplication Priority

When same content appears on multiple platforms:

1. **Official source** > Community source
2. **Higher engagement** > Lower engagement
3. **Earlier post** > Later repost

Example:
- Vue 3.5 announcement on blog.vuejs.org (keep)
- Same announcement shared on HN (discard, link to official)
- Discussion thread on Reddit about it (keep - different value)

## Minimum Thresholds

Content below these thresholds is excluded:

| Source | Minimum Score |
|--------|---------------|
| Hacker News | 5 points |
| Reddit | 10 upvotes |
| dev.to | 5 reactions |
| GitHub trending | 50 stars this week |

## Editorial Overrides

The ranking algorithm provides suggestions, but editorial judgment applies:

**Always include:**
- Major version releases (Vue 4, Nuxt 4, Vite 6, etc.)
- Security advisories
- Deprecation notices
- Core team announcements

**Consider excluding:**
- Duplicate coverage of same topic
- Low-quality clickbait despite high engagement
- Outdated content that surfaces due to new comments
- Self-promotion without educational value
