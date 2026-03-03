#!/usr/bin/env python3
"""
testssl_scanner.py - SSL/TLS Configuration Tester

Standalone test (no MCP needed):
    python3 testssl_scanner.py https://example.com
    python3 testssl_scanner.py example.com:443

Requires testssl.sh cloned to ~/testssl:
    git clone --depth 1 https://github.com/drwetter/testssl.sh.git ~/testssl
    chmod +x ~/testssl/testssl.sh
"""

import subprocess
import shlex
import os
import pathlib

# Path to testssl.sh — adjust if installed elsewhere
TESTSSL  = str(pathlib.Path.home() / "testssl" / "testssl.sh")
TIMEOUT  = 300


def run_testssl(args: str) -> str:
    if not os.path.exists(TESTSSL):
        return (
            f"testssl.sh not found at {TESTSSL}\n"
            "Install it:\n"
            "  git clone --depth 1 https://github.com/drwetter/testssl.sh.git ~/testssl\n"
            "  chmod +x ~/testssl/testssl.sh"
        )

    cmd = ["bash", TESTSSL, "--color", "0"] + shlex.split(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        return result.stdout or result.stderr or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Timeout: testssl exceeded {TIMEOUT}s."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "example.com:443"
    # --fast gives a quicker overview scan
    print(run_testssl(f"--fast {target}"))
