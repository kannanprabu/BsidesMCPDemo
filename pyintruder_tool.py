#!/usr/bin/env python3
"""
pyintruder_tool.py - PyIntruder CLI Web Fuzzer Wrapper

Like Burp Suite Intruder but in the terminal.
Uses $p$ as placeholder for payload injection.

Standalone test (no MCP needed):
    python3 pyintruder_tool.py "http://testphp.vulnweb.com/userinfo.php?username=$p$"

Requires:
    git clone https://github.com/hsagnik/pyintruder_cli ~/pyintruder_cli
    pip3 install -r ~/pyintruder_cli/requirements.txt --break-system-packages
"""

import subprocess
import shlex
import os
import re
import sys
import tempfile
import pathlib

PYINTRUDER = str(pathlib.Path.home() / "pyintruder_cli" / "pyintruder_cli.py")
TIMEOUT    = 300

WORDLIST_CANDIDATES = [
    "/usr/share/dirb/wordlists/common.txt",
    "/usr/share/wordlists/dirb/common.txt",
    "/usr/share/wordlists/common.txt",
]

BUILTIN_WORDLIST = """admin
administrator
login
index
home
test
backup
config
upload
files
api
user
users
dashboard
panel
search
register
settings
logout
signin
signup
guest
anonymous
root
superuser
manager
support
help
info
status
default
public
private
secret
password
pass
passwd
""".strip()


def get_wordlist() -> tuple[str, bool]:
    for path in WORDLIST_CANDIDATES:
        if os.path.exists(path):
            return path, False
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    tmp.write(BUILTIN_WORDLIST)
    tmp.close()
    return tmp.name, True


def run_pyintruder(url: str, args: str = "") -> str:
    if not os.path.exists(PYINTRUDER):
        return (
            f"pyintruder_cli.py not found at {PYINTRUDER}\n"
            "Install:\n"
            "  git clone https://github.com/hsagnik/pyintruder_cli ~/pyintruder_cli\n"
            "  pip3 install -r ~/pyintruder_cli/requirements.txt --break-system-packages"
        )

    if "$p$" not in url and "$p1$" not in url:
        return (
            "Error: URL must contain a position marker $p$\n"
            "Example: http://example.com/page?id=$p$"
        )

    wordlist, is_temp = get_wordlist()
    source = "built-in fallback" if is_temp else wordlist

    if not args:
        args = f"-w {wordlist} -t 5"
    elif "-w" not in args:
        args = f"{args} -w {wordlist}"

    cmd = [sys.executable, PYINTRUDER, "-u", url] + shlex.split(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        output = result.stdout or result.stderr or "(no output)"
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        return f"[Wordlist: {source}]\n\n{output}"
    except subprocess.TimeoutExpired:
        return f"Timeout: pyintruder exceeded {TIMEOUT}s."
    except Exception as e:
        return f"Error: {e}"
    finally:
        if is_temp and os.path.exists(wordlist):
            os.unlink(wordlist)


if __name__ == "__main__":
    url  = sys.argv[1] if len(sys.argv) > 1 else "http://testphp.vulnweb.com/userinfo.php?username=$p$"
    args = sys.argv[2] if len(sys.argv) > 2 else "-t 5 -v"
    print(run_pyintruder(url, args))
