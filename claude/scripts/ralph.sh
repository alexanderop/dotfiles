#!/bin/bash
# Ralph - Autonomous agent loop for Claude Code
# Usage: ralph [max_iterations]
#
# Runs Claude Code in a loop to complete user stories from ralph/prd.json
# Each iteration picks the next incomplete story and implements it.

set -e

MAX_ITERATIONS=${1:-10}
RALPH_DIR="$(pwd)/ralph"
PRD_FILE="$RALPH_DIR/prd.json"
PROGRESS_FILE="$RALPH_DIR/progress.txt"
PROMPT_FILE="$RALPH_DIR/prompt.md"
ARCHIVE_DIR="$RALPH_DIR/archive"
LAST_BRANCH_FILE="$RALPH_DIR/.last-branch"
TEMPLATE_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/ralph/references"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_error() { echo -e "${RED}Error: $1${NC}" >&2; }
echo_success() { echo -e "${GREEN}$1${NC}"; }
echo_info() { echo -e "${BLUE}$1${NC}"; }
echo_warn() { echo -e "${YELLOW}$1${NC}"; }

# Validate ralph/ directory exists
if [ ! -d "$RALPH_DIR" ]; then
  echo_error "ralph/ directory not found in current directory"
  echo "Run '/ralph' skill first to initialize"
  exit 1
fi

# Validate prd.json exists
if [ ! -f "$PRD_FILE" ]; then
  echo_error "ralph/prd.json not found"
  echo "Run '/ralph' skill to convert your PRD"
  exit 1
fi

# Copy prompt template if missing
if [ ! -f "$PROMPT_FILE" ]; then
  if [ -f "$TEMPLATE_DIR/prompt-template.md" ]; then
    cp "$TEMPLATE_DIR/prompt-template.md" "$PROMPT_FILE"
    echo_info "Created ralph/prompt.md from template"
  else
    echo_error "ralph/prompt.md not found and no template available"
    echo "Create ralph/prompt.md with agent instructions"
    exit 1
  fi
fi

# Archive previous run if branch changed
if [ -f "$PRD_FILE" ] && [ -f "$LAST_BRANCH_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || echo "")

  if [ -n "$CURRENT_BRANCH" ] && [ -n "$LAST_BRANCH" ] && [ "$CURRENT_BRANCH" != "$LAST_BRANCH" ]; then
    # Archive the previous run
    DATE=$(date +%Y-%m-%d)
    # Strip "ralph/" prefix from branch name for folder
    FOLDER_NAME=$(echo "$LAST_BRANCH" | sed 's|^ralph/||')
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$DATE-$FOLDER_NAME"

    echo_info "Archiving previous run: $LAST_BRANCH"
    mkdir -p "$ARCHIVE_FOLDER"
    [ -f "$PRD_FILE" ] && cp "$PRD_FILE" "$ARCHIVE_FOLDER/"
    [ -f "$PROGRESS_FILE" ] && cp "$PROGRESS_FILE" "$ARCHIVE_FOLDER/"
    echo "   Archived to: $ARCHIVE_FOLDER"

    # Reset progress file for new run
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
  fi
fi

# Track current branch
if [ -f "$PRD_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  if [ -n "$CURRENT_BRANCH" ]; then
    echo "$CURRENT_BRANCH" > "$LAST_BRANCH_FILE"
  fi
fi

# Initialize progress file if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Progress Log" > "$PROGRESS_FILE"
  echo "Started: $(date)" >> "$PROGRESS_FILE"
  echo "" >> "$PROGRESS_FILE"
  echo "## Codebase Patterns" >> "$PROGRESS_FILE"
  echo "(Patterns will be discovered and added here during execution)" >> "$PROGRESS_FILE"
  echo "---" >> "$PROGRESS_FILE"
fi

# Show current status
PROJECT=$(jq -r '.project // "Unknown"' "$PRD_FILE")
BRANCH=$(jq -r '.branchName // "unknown"' "$PRD_FILE")
TOTAL_STORIES=$(jq '.userStories | length' "$PRD_FILE")
COMPLETED=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE")
REMAINING=$((TOTAL_STORIES - COMPLETED))

echo ""
echo_info "========================================"
echo_info "  Ralph - Autonomous Agent Loop"
echo_info "========================================"
echo "  Project: $PROJECT"
echo "  Branch:  $BRANCH"
echo "  Stories: $COMPLETED/$TOTAL_STORIES complete ($REMAINING remaining)"
echo "  Max iterations: $MAX_ITERATIONS"
echo ""

if [ "$REMAINING" -eq 0 ]; then
  echo_success "All stories are already complete!"
  exit 0
fi

echo_warn "Starting in 3 seconds... (Ctrl+C to cancel)"
sleep 3

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "═══════════════════════════════════════════════════════"
  echo "  Ralph Iteration $i of $MAX_ITERATIONS"
  echo "═══════════════════════════════════════════════════════"

  # Run Claude Code with the ralph prompt
  OUTPUT=$(cat "$PROMPT_FILE" | claude --dangerously-skip-permissions 2>&1 | tee /dev/stderr) || true

  # Check for completion signal
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo_success "Ralph completed all tasks!"
    echo "Completed at iteration $i of $MAX_ITERATIONS"
    exit 0
  fi

  # Update remaining count
  COMPLETED=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE")
  REMAINING=$((TOTAL_STORIES - COMPLETED))
  echo ""
  echo_info "Progress: $COMPLETED/$TOTAL_STORIES complete ($REMAINING remaining)"

  if [ "$REMAINING" -eq 0 ]; then
    echo_success "All stories complete!"
    exit 0
  fi

  echo "Continuing to next iteration..."
  sleep 2
done

echo ""
echo_warn "Ralph reached max iterations ($MAX_ITERATIONS) without completing all tasks."
echo "Check $PROGRESS_FILE for status."
echo ""
echo "Remaining stories:"
jq -r '.userStories[] | select(.passes == false) | "  - \(.id): \(.title)"' "$PRD_FILE"
exit 1
