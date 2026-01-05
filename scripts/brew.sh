#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPT_DIR")"

echo "Installing Homebrew packages..."

if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew is not installed."
    echo "Install it first: https://brew.sh"
    exit 1
fi

brew bundle --file="$DOTFILES_DIR/Brewfile"

echo "Homebrew packages installed!"
