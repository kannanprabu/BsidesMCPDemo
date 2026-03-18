#!/usr/bin/env python3
"""
ping_tool.py - Ping Host Reachability Tool

Standalone test (no MCP needed):
    python3 ping_tool.py scanme.nmap.org
"""

import subprocess
import shlex

BINARY  = "/sbin/ping"
#Binary for Windows WSL (uncomment if using on Windows)
#BINARY = "/usr/bin/ping"
TIMEOUT = 30


def run_ping(args: str) -> str:
    cmd = [BINARY] + shlex.split(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        return result.stdout or result.stderr or "(no output)"
    except subprocess.TimeoutExpired:
        return "Timeout: ping exceeded 30s."
    except FileNotFoundError:
        return "ping not found."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    print(run_ping(f"-c 4 {target}"))
