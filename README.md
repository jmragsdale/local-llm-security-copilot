![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![LM Studio](https://img.shields.io/badge/LM_Studio-Local_LLM-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Air-Gap Ready](https://img.shields.io/badge/Air--Gap-Ready-brightgreen)
![Zero Telemetry](https://img.shields.io/badge/Telemetry-None-blue)

# Local LLM Security Copilot

An AI-powered security analysis toolkit that runs **entirely on your local machine** using [LM Studio](https://lmstudio.ai/). No API keys. No data leaves your network. Built for security teams operating in regulated, air-gapped, or privacy-sensitive environments.

## Why Local?

Most AI security tools send your data to cloud APIs — logs, configs, CVE details, and potentially sensitive infrastructure details go to a third-party server. For teams in **financial services, healthcare, government, or defense**, this is a non-starter.

This copilot runs against a local LLM via LM Studio's OpenAI-compatible API. The same AI capabilities, zero data exfiltration.

| Capability | Cloud LLM | Local LLM (This Tool) |
|---|---|---|
| Log analysis | ✅ | ✅ |
| CVE explanation | ✅ | ✅ |
| Config review | ✅ | ✅ |
| Data leaves network | ❌ Yes | ✅ No |
| API key required | ❌ Yes | ✅ No |
| Works air-gapped | ❌ No | ✅ Yes |
| Cost per query | ❌ Yes | ✅ Free |

## Features

| Command | Description |
|---|---|
| `analyze-logs` | Analyze firewall, web server, auth, or SIEM logs for threats and IOCs |
| `explain-cve` | Translate a CVE into plain-English with CVSS context and remediation steps |
| `review-config` | Audit firewall rules, security groups, or network configs for misconfigurations |
| `chat` | Interactive security Q&A with an expert-prompted local LLM |

## Prerequisites

1. Install [LM Studio](https://lmstudio.ai/) (free, runs on Mac/Windows/Linux)
2. Download a model — recommended:
   - **Mistral 7B Instruct** — fast, solid reasoning
   - **Llama 3 8B Instruct** — strong general capability
   - **Phi-3 Mini** — lightweight, good for low-RAM machines
3. In LM Studio: go to **Local Server** tab → click **Start Server**

## Installation

```bash
git clone https://github.com/jmragsdale/local-llm-security-copilot.git
cd local-llm-security-copilot
pip install -r requirements.txt
```

## Usage

### Analyze security logs
```bash
# From a file
python copilot.py analyze-logs --input samples/firewall_log.txt

# Pipe directly from your system
cat /var/log/auth.log | python copilot.py analyze-logs

# AWS CloudWatch logs
aws logs get-log-events --log-group-name /aws/lambda/myfunction \
  --log-stream-name latest | python copilot.py analyze-logs
```

### Explain a CVE
```bash
python copilot.py explain-cve --input CVE-2021-44228
python copilot.py explain-cve --input "Log4Shell remote code execution vulnerability"
```

### Review a security configuration
```bash
python copilot.py review-config --input samples/security_group.conf
python copilot.py review-config --input my-firewall-rules.txt
```

### Interactive security chat
```bash
python copilot.py chat
```

## Example Output

**`analyze-logs` on `samples/firewall_log.txt`:**

```
## THREAT SUMMARY
Severity: CRITICAL
A Tor exit node (185.220.101.47) conducted an SSH brute-force attack against 10.0.1.22
with 847 attempts in 4 minutes. A separate IP (203.0.113.88) successfully authenticated
via SSH minutes later — likely the same actor rotating IPs. The compromised host then
initiated outbound connections to a suspected Telegram C2 channel, attempted lateral
movement (blocked), queried two suspicious domains via DNS, and exfiltrated ~847MB to
an external CDN IP over HTTPS.

## INDICATORS OF COMPROMISE
- IP: 185.220.101.47 (Tor exit node, brute-force source)
- IP: 203.0.113.88 (successful SSH login post-brute-force)
- IP: 91.108.4.11 (suspected Telegram C2)
- Domain: c2-callback.xyz
- Domain: exfil-staging.xyz
- Host: 10.0.1.22 (compromised)
...
```

## Architecture

```
┌─────────────────────────────────────────────┐
│  copilot.py  (CLI entry point)              │
│    ├── analyze-logs  →  log_analyzer.py     │
│    ├── explain-cve   →  cve_explainer.py    │
│    ├── review-config →  config_reviewer.py  │
│    └── chat          →  direct prompt       │
│                     ↓                       │
│         src/lm_client.py                    │
│         (OpenAI-compatible REST client)     │
└─────────────────┬───────────────────────────┘
                  │  HTTP  localhost:1234
         ┌────────▼────────────┐
         │   LM Studio         │
         │   Local Server      │
         │   (any GGUF model)  │
         └─────────────────────┘
         No external network calls
```

## Tested Models

| Model | Size | Quality | Speed |
|---|---|---|---|
| Mistral 7B Instruct v0.3 | 4.1GB | ⭐⭐⭐⭐ | Fast |
| Llama 3 8B Instruct | 4.7GB | ⭐⭐⭐⭐⭐ | Fast |
| Phi-3 Mini 4K Instruct | 2.2GB | ⭐⭐⭐ | Very Fast |
| Mixtral 8x7B Instruct | 26GB | ⭐⭐⭐⭐⭐ | Slow |

## LLM Provider Comparison

This tool was validated by comparing outputs against multiple LLMs before settling on local deployment as the primary mode:

| Provider | Accuracy | Data Privacy | Cost | Verdict |
|---|---|---|---|---|
| Claude 3.5 Sonnet | ⭐⭐⭐⭐⭐ | ❌ Cloud | Per token | Best quality |
| ChatGPT-4o | ⭐⭐⭐⭐⭐ | ❌ Cloud | Per token | Excellent |
| Gemini 1.5 Pro | ⭐⭐⭐⭐ | ❌ Cloud | Per token | Very good |
| Mistral 7B (local) | ⭐⭐⭐⭐ | ✅ Local | Free | Best for sensitive data |

For non-sensitive use cases, the cloud APIs produce richer output. For regulated environments, local wins by default.

## Use Cases

- **SOC teams** without cloud LLM budget or approval
- **Air-gapped environments** (classified networks, OT/ICS)
- **Regulated industries** where log data cannot leave the network
- **Security training** — understand what logs and CVEs actually mean
- **Pre-commit hooks** — pipe IaC configs through `review-config` before deployment

## Related Projects

- [ai-iac-security-reviewer](https://github.com/jmragsdale/ai-iac-security-reviewer) — AI-powered Terraform/Bicep security review with CI/CD integration
- [iac-policy-pipeline](https://github.com/jmragsdale/iac-policy-pipeline) — OPA policy enforcement pipeline for infrastructure deployments

## Author

**Jermaine Ragsdale** · CISSP · AWS Solutions Architect  
[jmragsdale.com](https://jmragsdale.com) · [LinkedIn](https://linkedin.com/in/jermaine-ragsdale-cissp) · [GitHub](https://github.com/jmragsdale)
