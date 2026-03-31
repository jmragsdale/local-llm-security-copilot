# DEVLOG — Local LLM Security Copilot

## v1.0 — Initial Release

**Motivation:** Working in enterprise environments (Truist, Fiserv) where sending security
logs and configurations to cloud APIs is prohibited by policy. Wanted to explore whether
local LLMs could provide useful security analysis while keeping data fully on-premise.

**LLM evaluation:** Tested prompts across Claude 3.5 Sonnet, ChatGPT-4o, and Gemini 1.5
Pro before tuning the system prompts for local models. Cloud models produced richer
output but local 7B-class models (Mistral, Llama 3) performed well on structured tasks
once system prompts were tightened.

**Key design decisions:**
- Single `requests` dependency — no LangChain or heavy frameworks. Keep it auditable.
- Temperature set to 0.15 by default — security analysis needs consistency, not creativity
- Structured output format enforced in system prompts — makes output parseable downstream
- Auto-detect model from LM Studio API — removes friction for first-time users

**LM Studio notes:** LM Studio exposes an OpenAI-compatible REST API at
`http://localhost:1234/v1` — this means the same client code works against any
OpenAI-compatible endpoint (local or cloud) with just a URL change.

**Next iteration ideas:**
- JSON output mode for SIEM/SOAR integration
- Batch log file processing
- Integration with `ai-iac-security-reviewer` for combined security pipeline
- Slack/Teams webhook for team-facing alerts
