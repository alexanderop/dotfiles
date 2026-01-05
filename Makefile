.PHONY: install link brew vscode update help

help:
	@echo "Available commands:"
	@echo "  make install  - Run full installation"
	@echo "  make link     - Create symlinks only"
	@echo "  make brew     - Install Homebrew packages only"
	@echo "  make vscode   - Setup VSCode only"
	@echo "  make update   - Export current configs to this repo"

install:
	./install.sh

link:
	./scripts/link.sh

brew:
	./scripts/brew.sh

vscode:
	./scripts/vscode.sh

update:
	@echo "Updating Brewfile..."
	brew bundle dump --file=Brewfile --force
	@echo "Updating VSCode extensions..."
	code --list-extensions | grep -v "^vscjava\." > vscode/extensions.txt
	@echo "Done! Review changes with: git diff"
