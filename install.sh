#!/bin/bash
set -e

DOTFILES_DIR="$HOME/dotfiles"
cd "$DOTFILES_DIR"

echo "========================================"
echo "  Dotfiles Installation"
echo "========================================"

# 1. Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH for Apple Silicon
    if [[ -d "/opt/homebrew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$HOME/.zprofile"
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

# 2. Install packages from Brewfile
echo ""
echo "Installing Homebrew packages..."
"$DOTFILES_DIR/scripts/brew.sh"

# 3. Install Oh My Zsh if not present
if [[ ! -d "$HOME/.oh-my-zsh" ]]; then
    echo ""
    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# 4. Install Zsh plugins
echo ""
echo "Installing Zsh plugins..."
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

if [[ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
fi

if [[ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
fi

if [[ ! -d "$ZSH_CUSTOM/plugins/zsh-completions" ]]; then
    git clone https://github.com/zsh-users/zsh-completions "$ZSH_CUSTOM/plugins/zsh-completions"
fi

# 5. Create symlinks
echo ""
echo "Creating symlinks..."
"$DOTFILES_DIR/scripts/link.sh"

# 6. Setup VSCode
echo ""
echo "Setting up VSCode..."
"$DOTFILES_DIR/scripts/vscode.sh"

# 7. Setup Claude Code
echo ""
echo "Setting up Claude Code..."
"$DOTFILES_DIR/scripts/claude.sh"

# 8. Configure macOS defaults (optional, asks user)
echo ""
read -p "Configure macOS system preferences? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$DOTFILES_DIR/scripts/macos.sh"
fi

echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Restart your terminal (or run: source ~/.zshrc)"
echo "  2. Run 'fnm install --lts' to install Node.js"
echo "  3. Run 'pnpm create vue@latest' to create a Vue project"
echo "  4. Open VSCode and sign in to sync settings"
echo "  5. Claude Code skills and commands are ready to use"
echo ""
