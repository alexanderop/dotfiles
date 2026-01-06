#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_MEM_DIR="$HOME/.claude-mem"

echo "Setting up Claude Code..."

# Create directories if they don't exist
mkdir -p "$CLAUDE_DIR"
mkdir -p "$CLAUDE_MEM_DIR"

# Backup and symlink settings.json
if [[ -f "$CLAUDE_DIR/settings.json" && ! -L "$CLAUDE_DIR/settings.json" ]]; then
    echo "Backing up existing settings.json"
    mv "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.backup"
fi
rm -f "$CLAUDE_DIR/settings.json"
ln -s "$DOTFILES_DIR/claude/settings.json" "$CLAUDE_DIR/settings.json"
echo "  Linked settings.json"

# Backup and symlink skills directory
if [[ -d "$CLAUDE_DIR/skills" && ! -L "$CLAUDE_DIR/skills" ]]; then
    echo "Backing up existing skills/"
    mv "$CLAUDE_DIR/skills" "$CLAUDE_DIR/skills.backup"
fi
rm -f "$CLAUDE_DIR/skills"
ln -s "$DOTFILES_DIR/claude/skills" "$CLAUDE_DIR/skills"
echo "  Linked skills/"

# Backup and symlink commands directory
if [[ -d "$CLAUDE_DIR/commands" && ! -L "$CLAUDE_DIR/commands" ]]; then
    echo "Backing up existing commands/"
    mv "$CLAUDE_DIR/commands" "$CLAUDE_DIR/commands.backup"
fi
rm -f "$CLAUDE_DIR/commands"
ln -s "$DOTFILES_DIR/claude/commands" "$CLAUDE_DIR/commands"
echo "  Linked commands/"

# Backup and symlink agents directory
if [[ -d "$CLAUDE_DIR/agents" && ! -L "$CLAUDE_DIR/agents" ]]; then
    echo "Backing up existing agents/"
    mv "$CLAUDE_DIR/agents" "$CLAUDE_DIR/agents.backup"
fi
rm -f "$CLAUDE_DIR/agents"
ln -s "$DOTFILES_DIR/claude/agents" "$CLAUDE_DIR/agents"
echo "  Linked agents/"

# Backup and symlink claude-mem settings.json
if [[ -f "$CLAUDE_MEM_DIR/settings.json" && ! -L "$CLAUDE_MEM_DIR/settings.json" ]]; then
    echo "Backing up existing claude-mem/settings.json"
    mv "$CLAUDE_MEM_DIR/settings.json" "$CLAUDE_MEM_DIR/settings.json.backup"
fi
rm -f "$CLAUDE_MEM_DIR/settings.json"
ln -s "$DOTFILES_DIR/claude-mem/settings.json" "$CLAUDE_MEM_DIR/settings.json"
echo "  Linked claude-mem/settings.json"

echo "Claude Code setup complete!"
