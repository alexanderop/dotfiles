---
name: conversation-search
description: Search past Claude Code conversation history. Use when asked to recall, find, or search for anything from previous conversations - including content discussed, links shared, problems solved, topics covered, things posted, or work done together. Triggers include "what did we do today", "summary of our work", "what did we work on", "from our conversations", "what did we discuss", "which X was about Y", "recall when we", "find where we talked about", "search history", "what did I share/post/send you about", "how did we fix", or any reference to past sessions or collaborative work.
---

# Conversation History Search

Search past Claude Code conversations to find content, solutions, and topics from previous sessions.

## When to Use

Use this skill when the user asks:
- "What did we do today?" or "Summary of our work"
- "What did we work on this week?"
- "Which newsletter/article/link was about X?"
- "Tell me from our conversations about Y"
- "What did I share/post/send you regarding Z?"
- "Find where we discussed X"
- "Recall what we talked about"
- "How did we fix X before?"
- "What was the solution for Y?"
- "Search history for Z"

**Important:** Never infer work history from git status alone - always search conversation history to understand what was actually discussed and worked on together.

## Quick Start

### Daily Digest (Fastest for "What did we do today?")

```bash
# Get today's work summary - ONE command, instant answer
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --digest today

# Yesterday's digest
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --digest yesterday

# Specific date
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --digest 2026-01-04

# Filter to specific project
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --digest today --project ~/Projects/nuxt/secondBrain
```

### Keyword Search with Date Filters

```bash
# Search only today's sessions
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --today "newsletter"

# Search yesterday
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --yesterday "bug fix"

# Search last N days
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --days 7 "refactor"

# Search since a specific date
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --since 2026-01-01 "feature"
```

## Full Usage

```bash
python3 ~/.claude/skills/conversation-search/scripts/search_history.py "<query>" [options]
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --digest [DATE] [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--project <path>` | Search only a specific project |
| `--limit <n>` | Maximum results (default: 5) |
| `--format json\|text` | Output format (default: text) |
| `--today` | Only sessions from today |
| `--yesterday` | Only sessions from yesterday |
| `--days N` | Sessions from last N days |
| `--since YYYY-MM-DD` | Sessions since date |
| `--digest [DATE]` | Show daily digest (today, yesterday, or YYYY-MM-DD) |

### Examples

```bash
# Find how a specific error was fixed
python3 ~/.claude/skills/conversation-search/scripts/search_history.py "EMFILE error"

# Search for a feature implementation (last 3 days only)
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --days 3 "vitest browser mode"

# Search within a specific project
python3 ~/.claude/skills/conversation-search/scripts/search_history.py "nuxt content" --project ~/Projects/nuxt/secondBrain

# Get JSON output for programmatic use
python3 ~/.claude/skills/conversation-search/scripts/search_history.py --digest today --format json
```

## Output

### Digest Mode Output

```
## January 04, 2026 - 4 sessions

### 1. Newsletter System Implementation
   Session: `2da9ab0b`
   Branch: `main`
   Files: content.config.ts, NewsletterCard.vue, NewsletterHeader.vue
   Commands: 6 executed

### 2. Conversation Search Skill Update
   Session: `96d4355d`
   Branch: `main`
   Files: SKILL.md, search_history.py
   Commands: 2 executed
```

### Search Mode Output

Results include:
- **Score**: Relevance ranking
- **Problem**: The original issue or request
- **Solution**: How it was resolved
- **Commands Run**: Bash commands executed during the fix
- **Session ID**: For locating the full conversation

## Workflow

### For "What did we do today?" questions:
1. Run `--digest today` (or `--digest yesterday`, etc.)
2. Present the formatted summary to the user

### For specific topic searches:
1. Use `--today` or `--days N` to narrow the time range first
2. Add keyword query to find relevant sessions
3. If more detail needed, read the full JSONL file:
   ```bash
   cat ~/.claude/projects/<encoded-path>/<session-id>.jsonl | head -100
   ```

## Tips

- **Use `--digest` for temporal questions** - It's much faster than keyword search
- **Combine date filters with keywords** - `--today "newsletter"` is faster than just `"newsletter"`
- Use specific technical terms (error messages, tool names)
- Try broader terms if specific search fails
- Commands run are useful for recreating solutions
