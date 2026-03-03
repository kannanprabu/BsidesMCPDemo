#!/usr/bin/env python3
"""
header_scanner.py - HTTP Security Headers Checker

Standalone test (no MCP needed):
    python3 header_scanner.py https://example.com
    python3 header_scanner.py https://lionlilly.com
"""

import subprocess

BINARY  = "/usr/bin/curl"
TIMEOUT = 30

# (http-header-key, display-name, why-it-matters)
SECURITY_HEADERS = [
    ("strict-transport-security",    "HSTS",                    "Enforces HTTPS connections"),
    ("content-security-policy",      "Content-Security-Policy", "Prevents XSS & injection attacks"),
    ("x-frame-options",              "X-Frame-Options",         "Prevents clickjacking"),
    ("x-content-type-options",       "X-Content-Type-Options",  "Prevents MIME type sniffing"),
    ("referrer-policy",              "Referrer-Policy",         "Controls referrer info leakage"),
    ("permissions-policy",           "Permissions-Policy",      "Restricts browser feature access"),
    ("x-xss-protection",             "X-XSS-Protection",        "Legacy XSS browser filter"),
    ("cross-origin-opener-policy",   "COOP",                    "Isolates browsing context"),
    ("cross-origin-embedder-policy", "COEP",                    "Cross-origin embedding control"),
    ("cross-origin-resource-policy", "CORP",                    "Cross-origin resource control"),
]


def check_security_headers(url: str) -> str:
    cmd = [BINARY, "-sI", "--max-time", "15", "-L", url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        raw = result.stdout
        if not raw:
            return "No response received from server."

        # Parse headers into lowercase dict
        headers = {}
        for line in raw.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                headers[k.strip().lower()] = v.strip()

        present, missing = [], []
        for key, name, reason in SECURITY_HEADERS:
            if key in headers:
                present.append(f"  [PASS] {name}: {headers[key]}")
            else:
                missing.append(f"  [FAIL] {name} - {reason}")

        server     = headers.get("server", "Unknown")
        powered_by = headers.get("x-powered-by", "")
        info_disc  = f"\n  [WARN] X-Powered-By: {powered_by} (information disclosure!)" if powered_by else ""

        return (
            f"Security Headers Report: {url}\n"
            f"{'='*60}\n"
            f"Server: {server}{info_disc}\n\n"
            f"PRESENT ({len(present)}/{len(SECURITY_HEADERS)}):\n"
            + ("\n".join(present) or "  (none)") +
            f"\n\nMISSING ({len(missing)}/{len(SECURITY_HEADERS)}):\n"
            + ("\n".join(missing) or "  All headers present!") +
            f"\n\n{'='*60}\n"
            f"Raw Response Headers:\n{raw}"
        )
    except subprocess.TimeoutExpired:
        return "Timeout: No response within 30 seconds."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(check_security_headers(url))
