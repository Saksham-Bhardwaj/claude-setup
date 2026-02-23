#!/usr/bin/env python3
"""
PreToolUse hook — security gate.
Blocks dangerous rm commands and .env file access across all tools.
Exit code 2 = block the tool call. Exit code 0 = allow.
"""

import json
import re
import sys


def is_dangerous_rm(command):
    normalized = " ".join(command.lower().split())
    patterns = [
        r"\brm\s+.*-[a-z]*r[a-z]*f",
        r"\brm\s+.*-[a-z]*f[a-z]*r",
        r"\brm\s+--recursive\s+--force",
        r"\brm\s+--force\s+--recursive",
        r"\brm\s+-r\s+.*-f",
        r"\brm\s+-f\s+.*-r",
    ]
    for p in patterns:
        if re.search(p, normalized):
            return True

    dangerous_paths = [r"/\s", r"/\*", r"~", r"\$HOME", r"\.\.", r"\*"]
    if re.search(r"\brm\s+.*-[a-z]*r", normalized):
        for path in dangerous_paths:
            if re.search(path, normalized):
                return True
    return False


def is_env_access(tool_name, tool_input):
    if tool_name in ("Read", "Edit", "MultiEdit", "Write"):
        fp = tool_input.get("file_path", "")
        if ".env" in fp and not fp.endswith(".env.sample") and not fp.endswith(".env.example"):
            return True
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if re.search(r"\.env\b(?!\.sample)(?!\.example)", cmd):
            return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if is_env_access(tool_name, tool_input):
            print("BLOCKED: .env file access is prohibited. Use .env.sample or .env.example for templates.", file=sys.stderr)
            sys.exit(2)

        if tool_name == "Bash" and is_dangerous_rm(tool_input.get("command", "")):
            print("BLOCKED: Dangerous rm command detected and prevented.", file=sys.stderr)
            sys.exit(2)

        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
