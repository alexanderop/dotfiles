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

### Shell (Zsh)
- Oh My Zsh with robbyrussell theme
- Plugins: git, z, node, npm, yarn, nvm, macos, brew, and more
- External plugins: zsh-autosuggestions, zsh-syntax-highlighting, zsh-completions
- fzf integration (Ctrl+R history, Ctrl+T files)
- eza/bat for better ls/cat
- Custom aliases for navigation, git, and safety

### Git
- Sensible defaults (rebase on pull, auto-upstream)
- Global gitignore for common files
- 20+ aliases (`git s`, `git lg`, `git cob`, `git undo`, etc.)
- VSCode as default editor

### Terminal (Ghostty)
- JetBrains Mono font
- Catppuccin Mocha theme
- Quick terminal (Cmd+`) drop-down
- Split panes and tab keybindings

### Vim
- Line numbers (relative)
- 4-space tabs
- Smart search (case-insensitive unless capitals used)
- Syntax highlighting

### Editor (VSCode)
- Night Owl theme with Fira Code font
- Vim keybindings with custom leader key mappings
- Minimalist UI (no minimap, breadcrumbs, or decorations)
- Extensions: Volar (Vue), ESLint, Copilot, Astro, MDX, Mermaid, Slidev

### CLI Tools (via Homebrew)
- `fnm` - Fast Node Manager
- `pnpm`, `yarn` - Package managers
- `gh` - GitHub CLI
- `ripgrep`, `fd` - Fast search
- `fzf` - Fuzzy finder
- `bat`, `eza` - Better cat/ls
- `jq`, `httpie` - JSON/API tools
- `tldr` - Simplified man pages

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
- Tap to click, three-finger drag
- Finder: show extensions, path bar, list view
- Dock: auto-hide, no recent apps
- Screenshots to Downloads (PNG, no shadow)

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
| `home/.profile` | `~/.profile` |
| `home/.nuxtrc` | `~/.nuxtrc` |
| `config/ghostty/` | `~/.config/ghostty/` |
| `config/gh/` | `~/.config/gh/` |
| `config/git/ignore` | `~/.config/git/ignore` |
| `vscode/settings.json` | `~/Library/Application Support/Code/User/settings.json` |
| `vscode/keybindings.json` | `~/Library/Application Support/Code/User/keybindings.json` |
| `vscode/extensions.txt` | *(installed via script)* |
