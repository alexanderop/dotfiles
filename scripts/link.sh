#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPT_DIR")"

echo "Creating symlinks..."

# Home directory files
for file in "$DOTFILES_DIR/home/".*; do
    filename=$(basename "$file")
    if [[ "$filename" != "." && "$filename" != ".." ]]; then
        target="$HOME/$filename"

        # Backup existing file if not a symlink
        if [[ -e "$target" && ! -L "$target" ]]; then
            echo "Backing up $target to $target.backup"
            mv "$target" "$target.backup"
        fi

        # Remove existing symlink
        if [[ -L "$target" ]]; then
            rm "$target"
        fi

        ln -s "$file" "$target"
        echo "  Linked $filename"
    fi
done

# .config directory files
mkdir -p "$HOME/.config"

for dir in "$DOTFILES_DIR/config/"*/; do
    dirname=$(basename "$dir")
    target="$HOME/.config/$dirname"

    # Backup existing directory if not a symlink
    if [[ -e "$target" && ! -L "$target" ]]; then
        echo "Backing up $target to $target.backup"
        mv "$target" "$target.backup"
    fi

    # Remove existing symlink
    if [[ -L "$target" ]]; then
        rm "$target"
    fi

    ln -s "${dir%/}" "$target"
    echo "  Linked .config/$dirname"
done

echo "Symlinks created successfully!"
