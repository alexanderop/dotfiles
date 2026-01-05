# Dotfiles

Personal configuration files for macOS development.

## Quick Start (Fresh Mac)

```bash
# Clone the repository
git clone https://github.com/alexanderop/dotfiles.git ~/projects/config

# Run the installer
cd ~/projects/config
./install.sh
```

## What's Included

### Shell
- Zsh with Oh My Zsh (robbyrussell theme)
- Plugins: git, z, zsh-autosuggestions, zsh-syntax-highlighting, zsh-completions
- Custom aliases for navigation, git, and safety
- fzf integration (Ctrl+R history, Ctrl+T files)
- eza/bat for better ls/cat

### Git
- Sensible defaults (rebase on pull, auto-upstream)
- 20+ aliases (`git s`, `git lg`, `git cob`, `git undo`, etc.)
- VSCode as default editor

### Terminal (Ghostty)
- JetBrains Mono font
- Catppuccin Mocha theme
- Quick terminal (Cmd+`) drop-down
- Split panes and tab keybindings

### Editor (VSCode)
- Night Owl theme with Fira Code font
- Vim keybindings with custom leader key mappings
- Minimalist UI (no minimap, breadcrumbs, or decorations)

### CLI Tools (via Homebrew)
- `fnm` - Fast Node Manager
- `pnpm`, `yarn` - Package managers
- `gh` - GitHub CLI
- `ripgrep`, `fd` - Fast search
- `fzf` - Fuzzy finder
- `bat`, `eza` - Better cat/ls
- `jq`, `httpie` - JSON/API tools

### Applications
- Ghostty (terminal)
- VSCode (editor)
- Obsidian (notes)
- Raycast (launcher)
- Rectangle (window management)
- Arc (browser)
- Claude Code, OpenCode

### macOS Defaults
- Fast key repeat
- Tap to click
- Finder: show extensions, path bar, list view
- Dock: auto-hide, no recent apps
- Screenshots to Downloads

## Commands

```bash
make install   # Full installation
make link      # Create symlinks only
make brew      # Install Homebrew packages only
make vscode    # Setup VSCode only
make macos     # Configure macOS preferences
make update    # Export current config to repo
```

## After Installation

```bash
# 1. Restart terminal or reload
source ~/.zshrc

# 2. Install Node.js
fnm install --lts

# 3. Create a Vue project
pnpm create vue@latest
```

## File Structure

| Source | Target |
|--------|--------|
| `home/.zshrc` | `~/.zshrc` |
| `home/.gitconfig` | `~/.gitconfig` |
| `home/.vimrc` | `~/.vimrc` |
| `config/ghostty/` | `~/.config/ghostty/` |
| `config/gh/` | `~/.config/gh/` |
| `vscode/settings.json` | `~/Library/.../Code/User/settings.json` |
