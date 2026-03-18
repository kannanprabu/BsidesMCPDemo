#!/usr/bin/env python3
"""
nmap_scanner.py - Nmap Port Scanner Tool

Standalone test (no MCP needed):
    python3 nmap_scanner.py scanme.nmap.org
    python3 nmap_scanner.py scanme.nmap.org "-T4 -F --open"
"""

import subprocess
import shlex

BINARY  = "/opt/homebrew/bin/nmap"
#Binary for Windows WSL(uncomment if using on Windows)
#BINARY  = "/usr/bin/nmap"
TIMEOUT = 300  # seconds


def run_nmap(args: str) -> str:
    cmd = [BINARY] + shlex.split(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        return result.stdout or result.stderr or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Timeout: nmap exceeded {TIMEOUT}s. Try adding -T4 -F for faster scans."
    except FileNotFoundError:
        return "nmap not found. Install it: sudo apt install nmap"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    flags  = sys.argv[2] if len(sys.argv) > 2 else "-T4 -F --open"
    print(run_nmap(f"{flags} {target}"))
