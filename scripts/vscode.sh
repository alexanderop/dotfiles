#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPT_DIR")"

# User directories for both editors
VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
VSCODE_INSIDERS_USER_DIR="$HOME/Library/Application Support/Code - Insiders/User"

setup_vscode_symlinks() {
    local user_dir="$1"
    local label="$2"

    mkdir -p "$user_dir"

    # Backup and symlink settings.json
    if [[ -f "$user_dir/settings.json" && ! -L "$user_dir/settings.json" ]]; then
        echo "  Backing up existing settings.json"
        mv "$user_dir/settings.json" "$user_dir/settings.json.backup"
    fi
    rm -f "$user_dir/settings.json"
    ln -s "$DOTFILES_DIR/vscode/settings.json" "$user_dir/settings.json"
    echo "  Linked settings.json"

    # Backup and symlink keybindings.json
    if [[ -f "$user_dir/keybindings.json" && ! -L "$user_dir/keybindings.json" ]]; then
        echo "  Backing up existing keybindings.json"
        mv "$user_dir/keybindings.json" "$user_dir/keybindings.json.backup"
    fi
    rm -f "$user_dir/keybindings.json"
    ln -s "$DOTFILES_DIR/vscode/keybindings.json" "$user_dir/keybindings.json"
    echo "  Linked keybindings.json"
}

install_extensions() {
    local cli="$1"
    local fallback_cli="$2"
    local label="$3"

    # Try CLI in PATH first, then fallback to app bundle path
    local resolved_cli=""
    if command -v "$cli" &> /dev/null; then
        resolved_cli="$cli"
    elif [[ -x "$fallback_cli" ]]; then
        resolved_cli="$fallback_cli"
    fi

    if [[ -n "$resolved_cli" ]]; then
        echo "Installing $label extensions..."
        while IFS= read -r extension || [[ -n "$extension" ]]; do
            if [[ -n "$extension" ]]; then
                echo "  Installing $extension..."
                "$resolved_cli" --install-extension "$extension" --force 2>/dev/null || true
            fi
        done < "$DOTFILES_DIR/vscode/extensions.txt"
    else
        echo "$label CLI not found. Skipping extensions."
    fi
}

# CLI paths (fallback to app bundle if not in PATH)
VSCODE_CLI="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
VSCODE_INSIDERS_CLI="/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code"

# Setup VSCode
echo "Setting up VSCode..."
setup_vscode_symlinks "$VSCODE_USER_DIR" "VSCode"
install_extensions "code" "$VSCODE_CLI" "VSCode"

# Setup VSCode Insiders
echo ""
echo "Setting up VSCode Insiders..."
setup_vscode_symlinks "$VSCODE_INSIDERS_USER_DIR" "VSCode Insiders"
install_extensions "code-insiders" "$VSCODE_INSIDERS_CLI" "VSCode Insiders"

echo ""
echo "VSCode setup complete!"
