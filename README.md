# BsidesMCPDemo ðŸ›¡ï¸
**AI-Powered Pentesting with Claude Desktop + MCP**

> BSides Workshop Demo â€” Connect Claude Desktop to real security tools using the Model Context Protocol (MCP)

---

## What You'll Build

```
Claude Desktop â”€â”€â–º MCP Server (server.py) â”€â”€â–º nmap / nikto / gobuster / testssl / pyintruder
                                          â—„â”€â”€ Results back in Claude
```

Ask Claude naturally:
- *"Scan scanme.nmap.org for open ports"*
- *"Check web vulnerabilities on http://testphp.vulnweb.com"*
- *"Run gobuster on http://testphp.vulnweb.com"*
- *"Check SSL/TLS config on example.com:443"*
- *"Fuzz http://testphp.vulnweb.com/userinfo.php?username=$p$ with common usernames"*
- *"Check security headers on https://example.com"*

---

## Tools Available

| Tool | File | What it does |
|------|------|-------------|
| `run_nmap` | `nmap_scanner.py` | Port & service scanning |
| `run_nikto` | `nikto_scanner.py` | Web vulnerability scanning |
| `run_ping` | `ping_tool.py` | Host reachability check |
| `check_security_headers` | `header_scanner.py` | HTTP security header audit |
| `run_gobuster` | `gobuster_scanner.py` | Directory & file brute forcing |
| `run_testssl` | `testssl_scanner.py` | SSL/TLS configuration testing |
| `run_pyintruder` | `pyintruder_tool.py` | Web fuzzer (like Burp Intruder) |

---

## File Structure

```
BsidesMCPDemo/
â”œâ”€â”€ server.py                          # MCP server â€” wires all tools together
â”œâ”€â”€ nmap_scanner.py                    # nmap wrapper
â”œâ”€â”€ nikto_scanner.py                   # nikto wrapper
â”œâ”€â”€ ping_tool.py                       # ping wrapper
â”œâ”€â”€ header_scanner.py                  # security headers checker (curl-based)
â”œâ”€â”€ gobuster_scanner.py                # gobuster wrapper (auto-wordlist fallback)
â”œâ”€â”€ testssl_scanner.py                 # testssl.sh wrapper
â”œâ”€â”€ pyintruder_tool.py                 # pyintruder_cli wrapper
â”œâ”€â”€ pyintruder_cli.py                  # PyIntruder CLI engine (fuzzing core)
â”œâ”€â”€ requirements.txt                   # Python deps (just mcp)
â”œâ”€â”€ claude_desktop_config_windows.json # Claude Desktop config for Windows/WSL
â””â”€â”€ claude_desktop_config_mac_linux.json # Claude Desktop config for macOS/Linux
```

Each tool is one standalone file. Test each one independently before touching MCP.

---

## Prerequisites

### System Tools

**Linux / WSL (Windows users):**
```bash
sudo apt update && sudo apt install -y nmap nikto gobuster curl python3 python3-pip
```

**macOS:**
```bash
brew install nmap nikto gobuster curl python3
```

### testssl.sh (required for SSL scanning)

```bash
git clone --depth 1 https://github.com/drwetter/testssl.sh.git ~/testssl
chmod +x ~/testssl/testssl.sh
```

### PyIntruder CLI (required for web fuzzing)

```bash
git clone https://github.com/hsagnik/pyintruder_cli ~/pyintruder_cli
pip3 install -r ~/pyintruder_cli/requirements.txt --break-system-packages
```

### Wordlists (for gobuster â€” Linux/WSL)

```bash
sudo apt install -y dirb
# Wordlist will be at: /usr/share/dirb/wordlists/common.txt
```

> **macOS:** gobuster_scanner.py auto-falls back to a built-in wordlist if system wordlists aren't found.

---

## Setup

### Step 1 â€” Clone the repo

```bash
git clone https://github.com/kannanprabu/BsidesMCPDemo.git
cd BsidesMCPDemo
```

### Step 2 â€” Install Python dependency

```bash
pip3 install mcp
```

Verify:
```bash
python3 -c "from mcp.server import Server; print('mcp OK')"
```

### Step 3 â€” Test each tool standalone (no MCP needed)

```bash
python3 ping_tool.py scanme.nmap.org
python3 nmap_scanner.py scanme.nmap.org "-T4 -F --open"
python3 nikto_scanner.py http://testphp.vulnweb.com
python3 header_scanner.py https://example.com
python3 gobuster_scanner.py http://testphp.vulnweb.com
python3 testssl_scanner.py example.com:443
python3 pyintruder_tool.py "http://testphp.vulnweb.com/userinfo.php?username=\$p\$"
```

**If a tool fails here, fix it before connecting to Claude Desktop.**

### Step 4 â€” Test the MCP server

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python3 server.py
```

Expected: JSON back with `"name":"BsidesMCPDemo"`. No errors = working.

### Step 5 â€” Configure Claude Desktop

Find the Claude Desktop config file:

| OS | Path |
|----|------|
| Windows | `C:\Users\USERNAME\AppData\Roaming\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

**Windows (WSL) â€” use `claude_desktop_config_windows.json`:**
```json
{
  "mcpServers": {
    "pentest": {
      "command": "wsl",
      "args": ["python3", "/home/YOUR_WSL_USERNAME/BsidesMCPDemo/server.py"]
    }
  }
}
```

**macOS / Linux â€” use `claude_desktop_config_mac_linux.json`:**
```json
{
  "mcpServers": {
    "pentest": {
      "command": "python3",
      "args": ["/home/YOUR_USERNAME/BsidesMCPDemo/server.py"]
    }
  }
}
```

Replace `YOUR_WSL_USERNAME` / `YOUR_USERNAME` with your actual username (`echo $USER` in terminal).

### Step 6 â€” Restart Claude Desktop

Close fully and reopen. Look for the ðŸ”Œ MCP tools indicator in Claude.

---

## How the Code Works

### server.py â€” The wiring layer

`server.py` is intentionally thin â€” it just registers tools and routes calls. All logic lives in the individual tool files.

```
list_tools()  â†’  declares 7 tools to Claude
call_tool()   â†’  routes each call to the right function
is_safe()     â†’  blocks shell injection characters (; && || ` $( | > <)
```

### Tool files â€” one function each

Every tool exports a single function:

```python
run_nmap(args: str) -> str
run_nikto(args: str) -> str
run_ping(args: str) -> str
check_security_headers(url: str) -> str
run_gobuster(args: str) -> str
run_testssl(args: str) -> str
run_pyintruder(url: str, args: str) -> str
```

### gobuster_scanner.py â€” Wordlist auto-fallback

If no system wordlist is found, gobuster_scanner automatically writes a built-in wordlist to a temp file and uses that. You'll see the source reported in the output:
```
[User: yourname] [Wordlist: /usr/share/dirb/wordlists/common.txt]
```

### testssl_scanner.py â€” Expects ~/testssl

Looks for testssl.sh at `~/testssl/testssl.sh`. If not found, returns a clear install message.

### pyintruder_tool.py â€” Expects ~/pyintruder_cli

Wraps the `pyintruder_cli.py` engine. Use `$p$` as the injection point in the URL:
```
http://example.com/page?id=$p$
```

---

## Workshop Exercise â€” How to Add a New Tool

Adding a tool is 3 steps:

**Step 1:** Create `my_tool.py` with one function:
```python
#!/usr/bin/env python3
import subprocess, shlex

def run_my_tool(args: str) -> str:
    cmd = ["/usr/bin/my_tool"] + shlex.split(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.stdout or result.stderr or "(no output)"

if __name__ == "__main__":
    import sys
    print(run_my_tool(sys.argv[1] if len(sys.argv) > 1 else "--help"))
```

**Step 2:** Add the import to `server.py`:
```python
from my_tool import run_my_tool
```

**Step 3:** Add a `Tool()` entry in `list_tools()` and an `elif` in `call_tool()` in `server.py`.

Restart Claude Desktop. Done.

---

## Safe Practice Targets

| Target | What it's for |
|--------|--------------|
| `scanme.nmap.org` | Official nmap test server |
| `http://testphp.vulnweb.com` | Intentionally vulnerable PHP app (Acunetix) |
| `http://demo.testfire.net` | IBM vulnerable banking demo |
| Your own VMs / lab | Best for deep testing |

> âš ï¸ **Only scan systems you own or have explicit written permission to test.**

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No result received` | Restart Claude Desktop fully (quit, not just close window) |
| Tool not found in Claude | Check JSON config syntax at [jsonlint.com](https://jsonlint.com) |
| Tool returns error | Test standalone first: `python3 nmap_scanner.py scanme.nmap.org` |
| Wrong WSL username | Run `echo $USER` in your WSL terminal |
| nmap/nikto times out | Add `-T4 -F` (nmap) or `-maxtime 60` (nikto) |
| gobuster "no wordlist" | `sudo apt install dirb -y` or let the built-in fallback handle it |
| testssl not found | `git clone --depth 1 https://github.com/drwetter/testssl.sh.git ~/testssl` |
| pyintruder not found | `git clone https://github.com/hsagnik/pyintruder_cli ~/pyintruder_cli` |
| `$p$` not in URL error | pyintruder requires `$p$` in the URL: `http://target/page?id=$p$` |
| macOS: `brew: command not found` | Install Homebrew: `https://brew.sh` |

---

## Requirements

```
mcp>=1.0.0
```

Python 3.10+ required (uses `match`/`tuple[str, bool]` type hints).

---

## Legal Notice

Unauthorized scanning may violate the CFAA and other applicable laws.  
Only use these tools on systems you own or have **explicit written permission** to test.

---

**Built for BSides by Kannan Prabu Ramamoorthy ðŸ›¡ï¸**