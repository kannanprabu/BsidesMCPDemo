# BSidesMCPDemo — Workshop Cheat Sheet
## "Where exactly do I make changes?"

---

## The Only File You Ever Edit: server.py

Every new tool needs exactly 2 changes in server.py. Nothing else.

---

## Adding a New Tool — 3 Steps

### Step 1 — Create my_tool.py (new file, no edits to existing files)

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

---

### Step 2 — server.py LINES 32-39 (Import block)

Add your import after the existing imports:

```python
# LINE 33
from nmap_scanner     import run_nmap
from nikto_scanner    import run_nikto
from ping_tool        import run_ping
from header_scanner   import check_security_headers
from gobuster_scanner import run_gobuster
from testssl_scanner  import run_testssl
from pyintruder_tool  import run_pyintruder
from my_tool          import run_my_tool     # ADD THIS at line 40
```

---

### Step 3a — server.py LINES 57-128 (Tool declaration in list_tools)

Add a new Tool() block inside the return [...] list, before the closing ] on line 128:

```python
        Tool(
            name="run_my_tool",
            description="What your tool does. Example: '--flag target'",
            inputSchema={
                "type": "object",
                "properties": {"args": {"type": "string", "description": "tool args + target"}},
                "required": ["args"]
            }
        ),   # ADD BEFORE ] on line 128
```

---

### Step 3b — server.py LINES 143-169 (Route in call_tool)

Add an elif before the final else on line 168:

```python
    elif name == "run_pyintruder":     # existing line 161
        ...
    elif name == "run_my_tool":        # ADD THIS before line 168
        return [TextContent(type="text", text=run_my_tool(args))]

    else:                              # line 168 - do not touch
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
```

---

## Full server.py Map

```
LINE  1- 25   docstring / tool list / how-to instructions
LINE 27- 30   imports (asyncio, mcp)
LINE 32- 39   CHANGE 1: TOOL IMPORTS  <-- add new import here
LINE 41        app = Server("BsidesMCPDemo")
LINE 43- 51   is_safe() shell injection blocker
LINE 54-128   CHANGE 2a: list_tools()  <-- add Tool() block here
LINE 131-169  CHANGE 2b: call_tool()   <-- add elif route here
LINE 172-179  main() / asyncio.run     <-- do not touch
```

---

## Quick Reference: All 7 Tools

### 1. nmap_scanner.py
```bash
# Standalone
python3 nmap_scanner.py scanme.nmap.org "-T4 -F --open"

# Ask Claude
"Scan scanme.nmap.org for open ports"
"Run nmap on 192.168.1.1"
```

### 2. nikto_scanner.py
```bash
# Standalone
python3 nikto_scanner.py http://testphp.vulnweb.com

# Ask Claude
"Check web vulnerabilities on http://testphp.vulnweb.com"
```

### 3. ping_tool.py
```bash
# Standalone
python3 ping_tool.py scanme.nmap.org

# Ask Claude
"Is scanme.nmap.org alive?"
"Ping testphp.vulnweb.com"
```

### 4. header_scanner.py
```bash
# Standalone
python3 header_scanner.py https://example.com

# Ask Claude
"Check security headers on https://example.com"
```

### 5. gobuster_scanner.py
```bash
# Standalone
python3 gobuster_scanner.py http://testphp.vulnweb.com

# Ask Claude
"Run gobuster on http://testphp.vulnweb.com"
```

### 6. testssl_scanner.py (requires ~/testssl cloned first)
```bash
# Install
git clone --depth 1 https://github.com/drwetter/testssl.sh.git ~/testssl

# Standalone
python3 testssl_scanner.py example.com:443

# Ask Claude
"Check SSL config on example.com"
```

### 7. pyintruder_tool.py (requires ~/pyintruder_cli cloned first)
```bash
# Install
git clone https://github.com/hsagnik/pyintruder_cli ~/pyintruder_cli
pip3 install -r ~/pyintruder_cli/requirements.txt --break-system-packages

# Standalone
python3 pyintruder_tool.py "http://testphp.vulnweb.com/userinfo.php?username=$p$"

# Ask Claude
"Fuzz http://testphp.vulnweb.com/userinfo.php?username=$p$"
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Claude does not see tool | Restart Claude Desktop fully |
| ImportError in server.py | Is my_tool.py in the same folder as server.py? |
| Tool runs but wrong output | Test standalone first: python3 my_tool.py args |
| Unknown tool: name | Did you add the elif in call_tool()? |
| Shell injection blocked | Args contain ; && or pipe - remove them |
| testssl not found | Clone: git clone --depth 1 https://github.com/drwetter/testssl.sh.git ~/testssl |
| pyintruder not found | Clone: git clone https://github.com/hsagnik/pyintruder_cli ~/pyintruder_cli |

---

## Safe Practice Targets

| Target | Use for |
|--------|---------|
| scanme.nmap.org | nmap, ping |
| http://testphp.vulnweb.com | nikto, gobuster, pyintruder, headers |
| example.com:443 | testssl, headers |
| Your own VM | Everything |

WARNING: Only scan systems you own or have explicit written permission to test.

---

Built for BSides by Kannan Prabu Ramamoorthy
