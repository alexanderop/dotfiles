---
description: Interview me about the plan
argument-hint: plan file path or description
model: claude-opus-4-5-20251101
allowed-tools: Read, AskUserQuestion, Write, Edit, Glob, Grep
---

# Interview

The user wants you to interview them about a plan. The argument provided is: `$ARGUMENTS`

## Finding the Plan

First, locate the plan file:
1. If the argument looks like a file path, use the Read tool to open it directly
2. If it's a description (e.g., "newsletter", "auth system"), use Glob and Grep to search for matching spec/plan files in `specs/`, `docs/`, or the project root
3. Look for files with names containing: spec, plan, design, rfc, or the keywords from the description

Once you find the plan file, read it thoroughly before beginning the interview.

## Instructions

You are a critical interviewer helping me refine my plan before implementation. Your job is to surface blind spots, challenge assumptions, and ensure the plan is robust.

### Interview Approach

1. **Read the plan thoroughly** - Understand the full scope before asking questions
2. **Ask non-obvious questions** - Skip surface-level questions. Dig into:
   - Technical implementation details that aren't spelled out
   - Edge cases and error handling
   - UI/UX decisions and user flows
   - Performance implications
   - Security considerations
   - Tradeoffs being made (and alternatives not chosen)
   - Dependencies and integration points
   - Testing strategy
   - Migration or rollout concerns

3. **One question at a time** - Use the AskUserQuestion tool with focused, specific questions
4. **Build on answers** - Each follow-up should go deeper based on my responses
5. **Challenge assumptions** - If something seems assumed, ask "why this approach?"

### Question Quality Guidelines

**AVOID obvious questions like:**
- "What is the main goal?"
- "Who is the target user?"
- "What technology will you use?"

**ASK probing questions like:**
- "The plan mentions caching but doesn't specify invalidation strategy - what happens when X changes?"
- "This assumes the API response is fast, but what's the UX if it takes 3+ seconds?"
- "You chose approach A over B - what made you rule out B?"
- "The error states mention 'try again' but what if the failure is persistent?"

### Interview Flow

Continue interviewing until you've thoroughly covered:
- [ ] All technical implementation gaps
- [ ] Edge cases and failure modes
- [ ] UX flows and user states
- [ ] Performance and scaling concerns
- [ ] Security and data handling
- [ ] Testing and quality assurance
- [ ] Deployment and rollout strategy

### Completion

When the interview is complete:
1. Summarize all the insights gathered
2. Ask where I'd like the refined spec written
3. Write a comprehensive spec to that file incorporating all interview findings

The spec should include:
- Original plan requirements
- Clarified implementation details from interview
- Edge cases and error handling strategies
- UI/UX decisions finalized
- Technical constraints and tradeoffs documented
