# BsidesMCPDemo 🛡️
**AI-Powered Pentesting with Claude Desktop + MCP**

> BSides Workshop Demo — Connect Claude to real security tools using the Model Context Protocol

---

## What You'll Build

Claude Desktop → MCP Server → nmap / nikto / curl → Results back in Claude

Ask Claude naturally:
- *"Scan scanme.nmap.org for open ports"*
- *"Check web vulnerabilities on http://testphp.vulnweb.com"*
- *"Check security headers on https://example.com"*

---

## File Structure

```
BsidesMCPDemo/
├── server.py                        # MCP wiring (thin — don't need to edit this)
├── nmap_scanner.py                  # nmap tool
├── nikto_scanner.py                 # nikto tool
├── ping_tool.py                     # ping tool
├── header_scanner.py                # security headers checker
├── requirements.txt
├── claude_desktop_config_windows.json
└── claude_desktop_config_mac_linux.json
```

Each tool = one file. Debug one file at a time. No magic.

---

## Step 1 — Install System Tools

**Linux / WSL (Windows):**
```bash
sudo apt update && sudo apt install nmap nikto curl -y
```

**macOS:**
```bash
brew install nmap nikto curl
```

---

## Step 2 — Install Python Package

```bash
pip3 install mcp
```

Verify:
```bash
python3 -c "from mcp.server import Server; print('mcp OK')"
```

---

## Step 3 — Clone & Test Each Tool

```bash
git clone https://github.com/kannanprabu/BsidesMCPDemo.git
cd BsidesMCPDemo
```

**Test tools directly — no MCP needed yet:**
```bash
python3 ping_tool.py scanme.nmap.org
python3 nmap_scanner.py scanme.nmap.org "-T4 -F"
python3 nikto_scanner.py http://testphp.vulnweb.com
python3 header_scanner.py https://example.com
```

Each file runs standalone. If a tool fails here, fix it before touching MCP.

---

## Step 4 — Test the MCP Server

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python3 server.py
```

Expected output:
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05", ... "name":"BsidesMCPDemo" ...}}
```

If you see JSON back — you're good. No errors = working.

---

## Step 5 — Configure Claude Desktop

**Find the config file:**

| OS | Path |
|---|---|
| Windows | `C:\Users\USERNAME\AppData\Roaming\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

**Windows (WSL) — paste this:**
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

**macOS/Linux — paste this:**
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

Replace `YOUR_WSL_USERNAME` with your actual username (`echo $USER` in terminal).

---

## Step 6 — Restart Claude Desktop

Close fully and reopen. You should see the 🔌 MCP tools indicator in Claude.

---

## Workshop Exercise — Add Your Own Tool

**Goal:** Add `gobuster` as a new tool in 3 steps.

**Step 1:** Create `gobuster_scanner.py`:
```python
#!/usr/bin/env python3
import subprocess, shlex

BINARY = "/usr/bin/gobuster"

def run_gobuster(args: str) -> str:
    cmd = [BINARY] + shlex.split(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.stdout or result.stderr or "(no output)"

if __name__ == "__main__":
    import sys
    print(run_gobuster(sys.argv[1] if len(sys.argv) > 1 else "--help"))
```

**Step 2:** In `server.py`, add the import at the top:
```python
from gobuster_scanner import run_gobuster
```

**Step 3:** In `server.py`, uncomment the two gobuster lines (Tool + elif).

Restart Claude Desktop. Ask: *"Run gobuster on http://testphp.vulnweb.com"*

---

## Safe Practice Targets

| Target | What it's for |
|---|---|
| `scanme.nmap.org` | Official nmap test server |
| `http://testphp.vulnweb.com` | Vulnerable PHP app (Acunetix) |
| `http://demo.testfire.net` | IBM vulnerable banking demo |
| Your own VMs / lab | Best for deep testing |

⚠️ Only scan systems you own or have explicit written permission to test.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No result received` | Restart Claude Desktop |
| Tool not found | Test standalone first: `python3 nmap_scanner.py target` |
| JSON config error | Validate JSON at jsonlint.com |
| Wrong WSL username | Run `echo $USER` in WSL terminal |
| Nmap times out | Use `-T4 -F` flags for faster scans |

---

## Legal Notice

Unauthorized scanning may violate CFAA and other laws.
Only use on systems you own or have **explicit written permission** to test.

---

**Built for BSides by Kannan Prabu Ramamoorthy 🛡️**
