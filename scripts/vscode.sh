#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPT_DIR")"
VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"

echo "Setting up VSCode..."

# Create VSCode user directory if it doesn't exist
mkdir -p "$VSCODE_USER_DIR"

# Backup and symlink settings.json
if [[ -f "$VSCODE_USER_DIR/settings.json" && ! -L "$VSCODE_USER_DIR/settings.json" ]]; then
    echo "Backing up existing settings.json"
    mv "$VSCODE_USER_DIR/settings.json" "$VSCODE_USER_DIR/settings.json.backup"
fi
rm -f "$VSCODE_USER_DIR/settings.json"
ln -s "$DOTFILES_DIR/vscode/settings.json" "$VSCODE_USER_DIR/settings.json"
echo "  Linked settings.json"

# Backup and symlink keybindings.json
if [[ -f "$VSCODE_USER_DIR/keybindings.json" && ! -L "$VSCODE_USER_DIR/keybindings.json" ]]; then
    echo "Backing up existing keybindings.json"
    mv "$VSCODE_USER_DIR/keybindings.json" "$VSCODE_USER_DIR/keybindings.json.backup"
fi
rm -f "$VSCODE_USER_DIR/keybindings.json"
ln -s "$DOTFILES_DIR/vscode/keybindings.json" "$VSCODE_USER_DIR/keybindings.json"
echo "  Linked keybindings.json"

# Install extensions
if command -v code &> /dev/null; then
    echo "Installing VSCode extensions..."
    while IFS= read -r extension || [[ -n "$extension" ]]; do
        if [[ -n "$extension" ]]; then
            echo "  Installing $extension..."
            code --install-extension "$extension" --force 2>/dev/null || true
        fi
    done < "$DOTFILES_DIR/vscode/extensions.txt"
    echo "Extensions installed!"
else
    echo "VSCode CLI not found. Install extensions manually or add 'code' to PATH."
fi

echo "VSCode setup complete!"
