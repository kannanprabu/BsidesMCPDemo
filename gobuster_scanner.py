#!/usr/bin/env python3
"""
gobuster_scanner.py - Gobuster Directory/File Brute Forcer

Standalone test (no MCP needed):
    python3 gobuster_scanner.py http://testphp.vulnweb.com

Install wordlists: sudo apt install dirb -y
"""

import subprocess
import shlex
import os
import tempfile
import getpass

BINARY  = "/opt/homebrew/bin/gobuster"
#Binary for Windows WSL (uncomment if using on Windows)
#BINARY  = "/usr/bin/gobuster"
TIMEOUT = 300

WORDLIST_CANDIDATES = [
    "/Users/kanna/wordlists/common.txt",
    "/usr/share/dirb/wordlists/common.txt",
    "/usr/share/wordlists/dirb/common.txt",
    "/usr/share/wordlists/common.txt",
]

BUILTIN_WORDLIST = """admin
administrator
login
index
home
about
contact
images
img
css
js
api
upload
uploads
files
backup
config
test
dev
staging
wp-admin
wp-content
wp-includes
phpinfo.php
robots.txt
sitemap.xml
.git
.env
CVS
secured
vendor
pictures
search
user
users
register
dashboard
panel
manage
static
assets
media
downloads
docs
help
support
blog
shop
cart
checkout
account
profile
settings
logout
signin
signup
cgi-bin
scripts
includes
tmp
temp
cache
logs
data
database
install
setup
server
portal
mail
webmail""".strip()


def get_wordlist() -> tuple[str, bool]:
    for path in WORDLIST_CANDIDATES:
        if os.path.exists(path):
            return path, False
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    tmp.write(BUILTIN_WORDLIST)
    tmp.close()
    return tmp.name, True


def run_gobuster(args: str) -> str:
    # Debug info — shows who MCP is running as
    try:
        current_user = getpass.getuser()
    except Exception:
        current_user = "unknown"

    wordlist, is_temp = get_wordlist()
    source = f"built-in fallback (no system wordlist found, running as user: {current_user})" if is_temp else wordlist

    if "-w" not in args:
        args = f"{args} -w {wordlist}"

    cmd = [BINARY] + shlex.split(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        output = result.stdout or result.stderr or "(no output)"
        return f"[User: {current_user}] [Wordlist: {source}]\n\n{output}"
    except subprocess.TimeoutExpired:
        return f"Timeout: gobuster exceeded {TIMEOUT}s."
    except FileNotFoundError:
        return "gobuster not found. Install: sudo apt install gobuster -y"
    except Exception as e:
        return f"Error: {e}"
    finally:
        if is_temp and os.path.exists(wordlist):
            os.unlink(wordlist)


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://testphp.vulnweb.com"
    flags  = sys.argv[2] if len(sys.argv) > 2 else "dir -q --no-error"
    print(run_gobuster(f"{flags} -u {target}"))
