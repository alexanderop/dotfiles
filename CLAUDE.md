# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a macOS dotfiles repository that manages personal configuration files. It uses symlinks to connect files from this repo to their expected locations in the home directory.

## Commands

```bash
# Full installation (Homebrew, Oh My Zsh, plugins, symlinks, VSCode)
make install

# Individual operations
make link    # Create symlinks only
make brew    # Install Homebrew packages only
make vscode  # Setup VSCode only

# Export current system config back to this repo
make update
```

## Architecture

**Symlink Strategy**: Files in `home/` are symlinked to `~/` and directories in `config/` are symlinked to `~/.config/`. The `scripts/link.sh` script handles backup of existing files before creating symlinks.

**Installation Flow**: `install.sh` runs sequentially:
1. Installs Homebrew (with Apple Silicon PATH setup)
2. Runs Brewfile installation
3. Installs Oh My Zsh + custom plugins (autosuggestions, syntax-highlighting, completions)
4. Creates symlinks
5. Configures VSCode

**VSCode Config**: Settings and keybindings are stored in `vscode/` and symlinked to `~/Library/Application Support/Code/User/`. Extensions are tracked in `extensions.txt`.
