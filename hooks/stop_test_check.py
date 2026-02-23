#!/usr/bin/env python3
"""
Stop hook — block completion if tests are failing.
Only activates in projects that have a pytest.ini, pyproject.toml, or package.json.
Uses stop_hook_active to prevent infinite loops (if Claude is already retrying, let it stop).
"""

import json
import subprocess
import sys
from pathlib import Path


def is_dev_ready():
    """Check if the project looks ready to run tests (deps installed)."""
    cwd = Path.cwd()
    import os

    # Python: virtualenv is active
    if os.environ.get("VIRTUAL_ENV"):
        return True

    # Python: local .venv directory exists with installed packages
    venv = cwd / ".venv"
    if venv.is_dir() and (venv / "lib").is_dir():
        return True

    # Node: node_modules exists
    if (cwd / "node_modules").is_dir():
        return True

    return False


def detect_test_runner():
    """Detect which test runner to use based on project files. Returns (command, label) or None."""
    cwd = Path.cwd()

    # Only run tests if the project has dependencies installed
    if not is_dev_ready():
        return None, None

    # Python project
    if (cwd / "pytest.ini").exists() or (cwd / "pyproject.toml").exists():
        if (cwd / "pyproject.toml").exists():
            content = (cwd / "pyproject.toml").read_text()
            if "pytest" in content or "tool.pytest" in content:
                return ["pytest", "--tb=short", "-q"], "pytest"
        if (cwd / "pytest.ini").exists():
            return ["pytest", "--tb=short", "-q"], "pytest"

    # Node project
    pkg = cwd / "package.json"
    if pkg.exists():
        try:
            pkg_data = json.loads(pkg.read_text())
            scripts = pkg_data.get("scripts", {})
            if "test" in scripts and "no test specified" not in scripts["test"]:
                return ["npm", "test", "--", "--silent"], "npm test"
        except (json.JSONDecodeError, KeyError):
            pass

    return None, None


def run_tests(command):
    """Run tests. Returns (passed, output)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return True, ""  # test runner not installed, skip
    except subprocess.TimeoutExpired:
        return False, "Tests timed out after 120 seconds"


def main():
    try:
        data = json.load(sys.stdin)

        # CRITICAL: if stop_hook_active is True, Claude is already retrying after
        # a previous stop-block. Let it stop to avoid infinite loops.
        if data.get("stop_hook_active", False):
            sys.exit(0)

        command, label = detect_test_runner()
        if command is None:
            sys.exit(0)  # no test runner found, don't block

        passed, output = run_tests(command)

        if passed:
            sys.exit(0)
        else:
            # Truncate output to avoid overwhelming Claude
            truncated = output[:800] if len(output) > 800 else output
            print(json.dumps({
                "decision": "block",
                "reason": f"Tests are failing ({label}). Fix them before completing.\n\n{truncated}"
            }))
            sys.exit(0)

    except Exception:
        sys.exit(0)  # fail open


if __name__ == "__main__":
    main()
