#!/usr/bin/env python3
"""
nikto_scanner.py - Nikto Web Vulnerability Scanner Tool

Standalone test (no MCP needed):
    python3 nikto_scanner.py http://testphp.vulnweb.com
"""

import subprocess
import shlex

BINARY  = "/opt/homebrew/bin/nikto"
#Binary for Windows WSL (uncomment if using on Windows)
#BINARY  = "/usr/bin/nikto"
TIMEOUT = 300


def run_nikto(args: str) -> str:
    cmd = [BINARY] + shlex.split(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        return result.stdout or result.stderr or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Timeout: nikto exceeded {TIMEOUT}s. Try adding -maxtime 60."
    except FileNotFoundError:
        return "nikto not found. Install it: sudo apt install nikto"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://testphp.vulnweb.com"
    print(run_nikto(f"-h {target} -maxtime 60"))
