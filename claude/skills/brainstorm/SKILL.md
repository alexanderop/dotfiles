---
name: brainstorm
description: |
  Facilitate interactive brainstorming sessions for feature ideas using structured questioning rounds.
  Use when asked to "brainstorm", "explore an idea", "flesh out a feature", "help me think through",
  or when the user presents a raw feature concept that needs refinement. Guides users through
  metrics, visualization, goals, implementation details, and scope to produce a complete feature spec.
---

# Brainstorm

Structured brainstorming that transforms rough ideas into actionable feature specs.

## Process

Use AskUserQuestion tool for each round. Keep 2-4 questions per round.

### Round 1: Core Concept & Metrics

- How should we measure/quantify the core concept?
- What data or signals indicate success?
- What's the primary input/source?

### Round 2: Goals & Value

- What's the primary goal? (multiSelect: true)
- What problem does this solve?

### Round 3: Visualization & UI

- What visualization or UI pattern fits best?
- Where should this live in the app?
- What interaction model?

### Round 4: Implementation Details

- Technical approach specifics
- Edge cases and boundaries
- Configuration options

### Round 5: Scope

- MVP vs full version?
- Out of scope items?

### Round 6: Confirm

Present summary and ask:
- "Yes, plan it" → Implementation planning
- "Tweak the spec" → Return to relevant round
- "Save for later" → Save spec only

## Output

Save to `docs/feature-specs/{feature-slug}.md`:

```markdown
# Feature: {Name}

> {One-line value proposition}

## Overview
{2-3 sentences}

## Goals
{Bulleted list}

## {Domain Section}
{Metrics, data sources, algorithms}

## Visualization / UI
{UI details, interactions}

## Implementation Details
{Technical specifics, edge cases}

## Scope
### MVP
{Minimum version}

### Future Enhancements
- [ ] {Out of scope items}

## Status
**Status:** Spec Complete
**Created:** {date}
**Priority:** TBD
```

## Guidelines

- Adapt questions to feature domain (skip irrelevant rounds)
- Use multiSelect: true for goals
- Keep option descriptions concise
- Always offer "Save for later" at end
