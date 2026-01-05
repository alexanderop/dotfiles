# Dotfiles

Personal configuration files for macOS development.

## Quick Start (Fresh Mac)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/config.git ~/projects/config

# Run the installer
cd ~/projects/config
./install.sh
```

## What's Included

### Shell
- Zsh with Oh My Zsh (robbyrussell theme)
- Plugins: git, z, zsh-autosuggestions, zsh-syntax-highlighting, zsh-completions
- Custom aliases for navigation, git, and safety

### Editor (VSCode)
- Night Owl theme with Fira Code font
- Vim keybindings with custom leader key mappings
- Minimalist UI (no minimap, breadcrumbs, or decorations)

### CLI Tools (via Homebrew)
- `gh` - GitHub CLI
- `ripgrep` - Fast text search
- `fnm` - Fast Node Manager
- `pnpm` - Package manager
- `ast-grep` - AST-based code search
- `tree` - Directory visualization

### Applications
- Ghostty (terminal)
- Obsidian (notes)
- VSCode (editor)
- Claude Code
- OpenCode Desktop

## Manual Commands

```bash
# Install everything
make install

# Just create symlinks
make link

# Just install Homebrew packages
make brew

# Just setup VSCode
make vscode

# Export current config to update this repo
make update
```

## File Structure

| Source | Target |
|--------|--------|
| `home/.zshrc` | `~/.zshrc` |
| `home/.gitconfig` | `~/.gitconfig` |
| `home/.vimrc` | `~/.vimrc` |
| `home/.nuxtrc` | `~/.nuxtrc` |
| `home/.profile` | `~/.profile` |
| `config/gh/` | `~/.config/gh/` |
| `config/git/` | `~/.config/git/` |
| `vscode/settings.json` | `~/Library/.../Code/User/settings.json` |
| `vscode/keybindings.json` | `~/Library/.../Code/User/keybindings.json` |

## After Installation

1. Restart your terminal (or run `source ~/.zshrc`)
2. Install Node.js: `fnm install --lts`
3. Open VSCode and sign in to sync any remaining settings
