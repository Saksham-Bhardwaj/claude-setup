# Claude Code Setup

My personal [Claude Code](https://claude.com/claude-code) configuration files.

## What's Included

| File | Location | Purpose |
|------|----------|---------|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Global instructions for Claude across all projects |
| `settings.json` | `~/.claude/settings.json` | Permissions and hook configuration |
| `mcp.json` | `~/.mcp.json` | MCP server configuration |
| `hooks/pre_tool_use.py` | `~/.claude/hooks/` | Security gate — blocks dangerous `rm` and `.env` access |
| `hooks/post_tool_use_lint.py` | `~/.claude/hooks/` | Auto-lints Python (ruff) and TypeScript (eslint) after edits |
| `hooks/stop_test_check.py` | `~/.claude/hooks/` | Blocks task completion if tests are failing |

## Quick Setup

```bash
# Clone the repo
git clone https://github.com/Saksham-Bhardwaj/claude-setup.git
cd claude-setup

# Run the install script
./install.sh
```

## Manual Setup

```bash
# Create directories
mkdir -p ~/.claude/hooks

# Copy files
cp CLAUDE.md ~/.claude/CLAUDE.md
cp settings.json ~/.claude/settings.json
cp mcp.json ~/.mcp.json
cp hooks/*.py ~/.claude/hooks/
```

## Hooks

### PreToolUse — Security Gate (`pre_tool_use.py`)
- Blocks `rm -rf` and other dangerous recursive delete commands
- Prevents reading/writing `.env` files (use `.env.sample` or `.env.example` instead)

### PostToolUse — Auto Lint (`post_tool_use_lint.py`)
- Runs `ruff check` on Python files after Write/Edit
- Runs project-local `eslint` on TypeScript/TSX files after Write/Edit
- Blocks the operation and asks Claude to fix lint errors

### Stop — Test Check (`stop_test_check.py`)
- Detects pytest or npm test based on project files
- Runs tests before allowing Claude to complete a task
- Includes infinite-loop prevention via `stop_hook_active`

## MCP Servers

- **puppeteer** — Browser automation via `@modelcontextprotocol/server-puppeteer`
- **github** — GitHub Copilot MCP endpoint
