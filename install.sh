#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing Claude Code configuration..."

# Create directories
mkdir -p ~/.claude/hooks

# Copy files
cp "$SCRIPT_DIR/CLAUDE.md" ~/.claude/CLAUDE.md
cp "$SCRIPT_DIR/settings.json" ~/.claude/settings.json
cp "$SCRIPT_DIR/mcp.json" ~/.mcp.json
cp "$SCRIPT_DIR/hooks/"*.py ~/.claude/hooks/

echo "Done. Files installed:"
echo "  ~/.claude/CLAUDE.md"
echo "  ~/.claude/settings.json"
echo "  ~/.mcp.json"
echo "  ~/.claude/hooks/pre_tool_use.py"
echo "  ~/.claude/hooks/post_tool_use_lint.py"
echo "  ~/.claude/hooks/stop_test_check.py"
