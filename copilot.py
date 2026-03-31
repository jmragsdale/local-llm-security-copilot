#!/usr/bin/env python3
"""
Local LLM Security Copilot
---------------------------
AI-powered security analysis that runs entirely on your local machine.
Powered by LM Studio. No data leaves your network.

Usage:
  python copilot.py analyze-logs --input samples/firewall_log.txt
  python copilot.py explain-cve --input CVE-2024-1234
  python copilot.py review-config --input samples/security_group.conf
  python copilot.py chat
"""

import argparse
import sys
from pathlib import Path

from src.lm_client import LMStudioClient
from src.tasks.log_analyzer import analyze_logs
from src.tasks.cve_explainer import explain_cve
from src.tasks.config_reviewer import review_config

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║   LOCAL LLM SECURITY COPILOT  ·  v1.0                       ║
║   Powered by LM Studio  ·  Air-gap ready  ·  Zero telemetry ║
╚══════════════════════════════════════════════════════════════╝
"""

CHAT_SYSTEM_PROMPT = """You are an expert cybersecurity consultant with deep expertise in:
- Cloud security architecture (AWS, Azure, GCP)
- Zero-trust network design and implementation
- Compliance frameworks: NIST CSF, PCI-DSS, HIPAA, SOC2, FedRAMP
- Threat modeling, vulnerability management, and incident response
- Infrastructure-as-Code security (Terraform, Bicep, CloudFormation)
- SIEM, EDR, and security automation

Provide expert, actionable guidance. Be direct and specific.
When recommending tools or configurations, give real examples."""


def get_input(args_input: str, prompt_text: str) -> str:
    """Resolve input from file path, inline string, or stdin."""
    if args_input:
        p = Path(args_input)
        if p.is_file():
            return p.read_text(encoding="utf-8")
        return args_input  # treat as inline text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return input(prompt_text).strip()


def cmd_analyze_logs(args, client):
    content = get_input(args.input, "Paste log content (then press Enter + Ctrl-D): ")
    if not content:
        print("[ERROR] No log content provided. Use --input <file> or pipe log data.")
        sys.exit(1)
    print("\n[*] Analyzing security logs...\n" + "─" * 60)
    print(analyze_logs(content, client))


def cmd_explain_cve(args, client):
    content = get_input(args.input, "Enter CVE ID or description: ")
    if not content:
        print("[ERROR] No CVE provided. Use --input CVE-2024-XXXX or a description.")
        sys.exit(1)
    print(f"\n[*] Researching: {content}\n" + "─" * 60)
    print(explain_cve(content, client))


def cmd_review_config(args, client):
    content = get_input(args.input, "Paste configuration (then press Enter + Ctrl-D): ")
    if not content:
        print("[ERROR] No config provided. Use --input <file> or pipe config data.")
        sys.exit(1)
    print("\n[*] Reviewing security configuration...\n" + "─" * 60)
    print(review_config(content, client))


def cmd_chat(client):
    print("[*] Security chat mode  ·  type 'exit' to quit\n" + "─" * 60)
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if user_input.lower() in ("exit", "quit", "q", ""):
            break
        print("\nCopilot: ", end="", flush=True)
        response = client.chat(CHAT_SYSTEM_PROMPT, user_input)
        print(response)
    print("\n[*] Session ended.")


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="AI-powered security analysis — runs entirely on your local machine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python copilot.py analyze-logs --input samples/firewall_log.txt
  python copilot.py analyze-logs --input samples/nginx_access.log
  python copilot.py explain-cve --input CVE-2021-44228
  python copilot.py explain-cve --input "Log4Shell remote code execution"
  python copilot.py review-config --input samples/security_group.conf
  python copilot.py chat
  cat /var/log/auth.log | python copilot.py analyze-logs
        """,
    )
    parser.add_argument(
        "command",
        choices=["analyze-logs", "explain-cve", "review-config", "chat"],
        help="Task to run",
    )
    parser.add_argument("--input", "-i", metavar="FILE_OR_TEXT",
                        help="Input file path or inline text/CVE ID")
    parser.add_argument("--url", default="http://localhost:1234/v1",
                        help="LM Studio API base URL (default: http://localhost:1234/v1)")
    parser.add_argument("--model", metavar="MODEL_ID",
                        help="Override model ID (auto-detected from LM Studio by default)")

    args = parser.parse_args()

    try:
        client = LMStudioClient(base_url=args.url, model=args.model)
    except RuntimeError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    dispatch = {
        "analyze-logs":   lambda: cmd_analyze_logs(args, client),
        "explain-cve":    lambda: cmd_explain_cve(args, client),
        "review-config":  lambda: cmd_review_config(args, client),
        "chat":           lambda: cmd_chat(client),
    }
    dispatch[args.command]()


if __name__ == "__main__":
    main()
