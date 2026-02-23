#!/usr/bin/env python3
"""
PostToolUse hook — auto-lint on file write.
Runs ruff on Python files and eslint on TypeScript/TSX files after Write/Edit.
Outputs JSON decision: {"decision": "block", "reason": "..."} to make Claude fix it.
"""

import json
import subprocess
import sys


def lint_python(file_path):
    """Run ruff check on a Python file. Returns (passed, output)."""
    try:
        result = subprocess.run(
            ["ruff", "check", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = (result.stdout or result.stderr or "").strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return True, ""  # ruff not installed, skip
    except subprocess.TimeoutExpired:
        return True, ""  # timeout, don't block


def find_project_eslint(file_path):
    """Walk up from file_path to find a project-local eslint binary."""
    import os
    directory = os.path.dirname(os.path.abspath(file_path))
    while True:
        candidate = os.path.join(directory, "node_modules", ".bin", "eslint")
        if os.path.isfile(candidate):
            return candidate, directory
        parent = os.path.dirname(directory)
        if parent == directory:
            return None, None
        directory = parent


def lint_typescript(file_path):
    """Run eslint on a TypeScript file using the project-local binary. Returns (passed, output)."""
    import os
    eslint_bin, project_root = find_project_eslint(file_path)
    if not eslint_bin:
        return True, ""  # no local eslint found, skip
    try:
        result = subprocess.run(
            [eslint_bin, file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_root,
        )
        output = (result.stdout or result.stderr or "").strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return True, ""  # eslint not installed, skip
    except subprocess.TimeoutExpired:
        return True, ""


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only run on Write or Edit operations
        if tool_name not in ("Write", "Edit", "MultiEdit"):
            print(json.dumps({}))
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path:
            print(json.dumps({}))
            sys.exit(0)

        passed = True
        output = ""

        if file_path.endswith(".py"):
            passed, output = lint_python(file_path)
        elif file_path.endswith((".ts", ".tsx")):
            passed, output = lint_typescript(file_path)
        else:
            print(json.dumps({}))
            sys.exit(0)

        if passed:
            print(json.dumps({}))
        else:
            print(json.dumps({
                "decision": "block",
                "reason": f"Lint errors in {file_path}:\n{output[:500]}"
            }))

        sys.exit(0)
    except Exception:
        print(json.dumps({}))
        sys.exit(0)


if __name__ == "__main__":
    main()
