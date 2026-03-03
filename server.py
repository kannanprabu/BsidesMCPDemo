#!/usr/bin/env python3
"""
server.py - MCP Server (Wiring Only)
======================================
BSides Workshop Demo — AI Pentest Bot with Claude Desktop

Compatible with: mcp >= 1.0.0, Python 3.10+, WSL on Windows, macOS, Linux

Tools available:
    1. run_nmap               - Port scanning
    2. run_nikto              - Web vulnerability scanning
    3. run_ping               - Host reachability
    4. check_security_headers - HTTP security header analysis
    5. run_gobuster           - Directory/file brute forcing
    6. run_testssl            - SSL/TLS configuration testing
    7. run_pyintruder         - Web fuzzing (like Burp Intruder)

HOW TO ADD A NEW TOOL
─────────────────────
1. Create e.g. my_tool.py with a run_my_tool(args) function
2. Import it below
3. Add a Tool() entry in list_tools()
4. Add an elif branch in call_tool()
Restart Claude Desktop. Done!
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Import tools ───────────────────────────────────────────────────────────────
from nmap_scanner     import run_nmap
from nikto_scanner    import run_nikto
from ping_tool        import run_ping
from header_scanner   import check_security_headers
from gobuster_scanner import run_gobuster
from testssl_scanner  import run_testssl
from pyintruder_tool  import run_pyintruder

app = Server("BsidesMCPDemo")

# Blocked shell characters — applied to all arg-based tools
BLOCKED = [";", "&&", "||", "`", "$(", "|", ">", "<"]


def is_safe(text: str) -> tuple[bool, str]:
    for char in BLOCKED:
        if char in text:
            return False, f"Blocked: '{char}' not allowed in args."
    return True, ""


# ── List available tools ───────────────────────────────────────────────────────
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="run_nmap",
            description="Run nmap port scanner. Example: '-T4 -F --open scanme.nmap.org'",
            inputSchema={
                "type": "object",
                "properties": {"args": {"type": "string", "description": "nmap arguments + target"}},
                "required": ["args"]
            }
        ),
        Tool(
            name="run_nikto",
            description="Run nikto web vulnerability scanner. Example: '-h http://testphp.vulnweb.com -maxtime 60'",
            inputSchema={
                "type": "object",
                "properties": {"args": {"type": "string", "description": "nikto arguments"}},
                "required": ["args"]
            }
        ),
        Tool(
            name="run_ping",
            description="Ping a host to check if it is alive. Example: '-c 4 scanme.nmap.org'",
            inputSchema={
                "type": "object",
                "properties": {"args": {"type": "string", "description": "ping arguments + target"}},
                "required": ["args"]
            }
        ),
        Tool(
            name="check_security_headers",
            description="Check HTTP security headers for a URL. Reports HSTS, CSP, X-Frame-Options, COOP, COEP and more.",
            inputSchema={
                "type": "object",
                "properties": {"url": {"type": "string", "description": "Full URL e.g. https://example.com"}},
                "required": ["url"]
            }
        ),
        Tool(
            name="run_gobuster",
            description="Run gobuster directory brute forcer. Example: 'dir -u http://testphp.vulnweb.com -w /usr/share/wordlists/dirb/common.txt -q --no-error'",
            inputSchema={
                "type": "object",
                "properties": {"args": {"type": "string", "description": "gobuster arguments including -u target and -w wordlist"}},
                "required": ["args"]
            }
        ),
        Tool(
            name="run_testssl",
            description="Test SSL/TLS configuration of a host. Example: '--fast example.com:443'",
            inputSchema={
                "type": "object",
                "properties": {"args": {"type": "string", "description": "testssl arguments + target e.g. '--fast example.com:443'"}},
                "required": ["args"]
            }
        ),
        Tool(
            name="run_pyintruder",
            description=(
                "Web fuzzer like Burp Suite Intruder. Use $p$ in URL as injection point. "
                "Example URL: 'http://testphp.vulnweb.com/userinfo.php?username=$p$' "
                "Example args: '-w /usr/share/wordlists/dirb/common.txt -t 5'"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url":  {"type": "string", "description": "Target URL with $p$ marker e.g. http://example.com/page?id=$p$"},
                    "args": {"type": "string", "description": "pyintruder args e.g. '-w /path/to/wordlist.txt -t 10'"}
                },
                "required": ["url"]
            }
        ),
    ]


# ── Route tool calls ───────────────────────────────────────────────────────────
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    args = arguments.get("args", "")

    # Security check for all arg-based tools
    if name != "check_security_headers":
        safe, msg = is_safe(args)
        if not safe:
            return [TextContent(type="text", text=msg)]

    if name == "run_nmap":
        return [TextContent(type="text", text=run_nmap(args))]

    elif name == "run_nikto":
        return [TextContent(type="text", text=run_nikto(args))]

    elif name == "run_ping":
        return [TextContent(type="text", text=run_ping(args))]

    elif name == "check_security_headers":
        return [TextContent(type="text", text=check_security_headers(arguments.get("url", "")))]

    elif name == "run_gobuster":
        return [TextContent(type="text", text=run_gobuster(args))]

    elif name == "run_testssl":
        return [TextContent(type="text", text=run_testssl(args))]

    elif name == "run_pyintruder":
        url = arguments.get("url", "")
        safe, msg = is_safe(url)
        if not safe:
            return [TextContent(type="text", text=msg)]
        return [TextContent(type="text", text=run_pyintruder(url, args))]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Start MCP server ───────────────────────────────────────────────────────────
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
