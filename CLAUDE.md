# Global Rules

## Planning & Todos
- Start non-trivial tasks in Plan mode. Go back and forth until solid, then auto-accept to execute
- Use TodoWrite for any task with 3+ steps. Each todo = a concrete, verifiable action. Only ONE in_progress at a time
- Before coding, identify files and dependency order. Change leaf dependencies first, work upward
- If a task touches 3+ files, write out the plan first. When ambiguous, ask — don't guess
- If you discover new work while implementing, add a new todo rather than expanding scope silently

## Context Management
- IMPORTANT: Use subagents for research-heavy subtasks to keep main context clean
- Read only the files you need — be surgical. Follow dependency order; finish each file before moving to the next
- When context gets long, summarize current understanding, what's left, and next step before continuing

## Verification
- IMPORTANT: Always verify your work — this 2-3x's quality. Run tests after every code change (single files over full suites)
- Run typecheck after changes (tsc, mypy, pyright). Typechecking and testing are separate steps — do both
- Test UI in browser/simulator. Never retry the same failing approach — try a different strategy or ask

## Session Discipline
- Keep each session focused on one task. Run `/code-simplifier` before committing

## Code Style
- Write simple, readable code. Don't add features, abstractions, or annotations beyond what was asked
- Only add error handling at system boundaries. Three similar lines > premature abstraction
- If something is unused, delete it completely

## Worktrees
- Use git worktrees for parallel subagents that modify code (isolation: "worktree")
- Don't use worktrees for read-only research or sequential tasks
- Skip worktrees when parallel tasks touch the same files heavily
- Run dependency installs in each new worktree. Clean up with `git worktree remove` after merging

## Git
- Write concise commit messages that explain "why", not "what"
- Don't commit .env files, credentials, or secrets
- Prefer specific `git add <files>` over `git add .`

## Compounding Engineering (CLAUDE.md Maintenance)
- When I correct you, update the project-level CLAUDE.md so you don't repeat it
- Each project should have its own CLAUDE.md with build/test commands, architecture notes, and gotchas
- CLAUDE.md is a living document — ruthlessly edit it and keep it concise
