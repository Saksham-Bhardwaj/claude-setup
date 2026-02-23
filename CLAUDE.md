# Global Rules

## Planning
- Start every non-trivial task in Plan mode (shift+tab twice). Go back and forth until the plan is solid, then switch to auto-accept mode to execute — a good plan lets Claude one-shot most PRs
- Break complex tasks into small, sequential steps. Use the TodoWrite tool to track them — mark each step done as you finish it, not in batches
- Before coding, identify which files need to change and the dependency order. Change leaf dependencies first, then work upward through callers
- If a task touches more than 3 files, write out the plan explicitly before starting
- When requirements are ambiguous, ask — don't guess. One clarifying question upfront saves a full rewrite later

## Todo Management
- Use the TodoWrite tool proactively for any task with 3+ steps
- Each todo should be a concrete, verifiable action — not vague ("Fix auth" is bad, "Add token validation in authStore refresh handler" is good)
- Only have ONE todo in_progress at a time. Complete it before starting the next
- If you discover new work while implementing, add it as a new todo rather than expanding scope silently
- When blocked on a todo, don't mark it complete — add a new todo for the blocker and address it first

## Context Management
- IMPORTANT: Use subagents for research-heavy or compute-intensive subtasks to keep main context clean and focused
- Offload file exploration, codebase searches, and background research to subagents rather than polluting the main conversation
- Prefer reading only the files you need. Don't speculatively read entire directories — be surgical
- When context gets long, summarize what you know so far before continuing: current understanding, what's left, next step
- For multi-file changes, follow the dependency order from your plan. Finish each file before moving to the next — don't scatter partial edits across files

## Verification
- IMPORTANT: Probably the most important thing — always give yourself a way to verify your work. This 2-3x's the quality of the final result
- Run tests after every code change. Prefer single test files over full suites for speed
- Run typecheck after changes (tsc, mypy, pyright — whatever the project uses). Typechecking and testing are separate steps — do both
- Test in the browser or simulator when working on UI. Open it, click through, iterate until it works and feels right
- If a test fails, read the error carefully and understand the root cause before changing anything
- Never retry the same failing approach. If blocked, try a different strategy or ask
- For long-running tasks, verify your work with a background subagent when done

## Session Discipline
- Keep each session focused on one task. Don't interleave unrelated changes
- After finishing a task, run `/code-simplifier` to clean up before committing
- Use slash commands (`/code-simplifier`, etc.) for repeatable workflows instead of re-prompting from scratch

## Code Style
- Write simple, readable code. No over-engineering
- Don't add features, abstractions, or "improvements" beyond what was asked
- Don't add comments, docstrings, or type annotations to code you didn't change
- Only add error handling at system boundaries (user input, external APIs). Trust internal code
- Three similar lines is better than a premature abstraction
- Avoid backwards-compatibility hacks — if something is unused, delete it completely

## Worktrees
- Use git worktrees for parallel subagents that modify code (isolation: "worktree")
- Don't use worktrees for read-only research or sequential tasks
- Skip worktrees when parallel tasks touch the same files heavily
- Run dependency installs (npm install, pip install, etc.) in each new worktree
- Clean up with `git worktree remove` after merging; run `git worktree prune` periodically

## Git
- Write concise commit messages that explain "why", not "what"
- Don't commit .env files, credentials, or secrets
- Prefer specific `git add <files>` over `git add .`

## Compounding Engineering (CLAUDE.md Maintenance)
- When I correct you on something, update the project-level CLAUDE.md so you don't make that mistake again
- Each project should have its own CLAUDE.md with build commands, test commands, architecture notes, and known gotchas
- CLAUDE.md is a living document — it compounds in value over time. Ruthlessly edit it and keep it concise
- During code review, update CLAUDE.md as part of the PR when you spot patterns or repeated mistakes
