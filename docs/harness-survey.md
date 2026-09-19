# Harness Investigation — OpenLLM Model Fabric Attachment
Date: 2026-09-19 · Host: macmini (macOS 26, arm64) · Repo: MindDragonLabs/openllm-bots

Goal: identify the top ~20 coding-agent harnesses, install on macmini, test each for
OpenLLM attachment (custom OpenAI-compatible base URL or MCP), record verdicts.
"Live" = a real completion routed through the OpenLLM gateway (127.0.0.1:8787/v1).

## Gateway under test
- OpenAI-compatible `/v1` on `http://127.0.0.1:8787/v1` (cloud origin `https://www.openllm.sh`, 307→local daemon)
- Key: `$OPENLLM_API_KEY` from `~/.openllm/.env` (never written into repo)
- Model catalog: 69 entries — chain aliases (`ultra`/`plus`/`lite`) + per-harness ids
  (`claude_code/*`, `cursor/*`, `chatgpt/*`, `kimi_code/*`, `grok/*`).
- Working direct models confirmed: `grok/grok-4.5`, `grok/grok-4.6`, `kimi_code/kimi-for-coding-highspeed`, `kimi_code/k3`.

## Results

| # | Harness | Binary | Ver | OpenLLM attach | Verdict |
|---|---------|--------|-----|----------------|---------|
| 1 | Claude Code | claude | 2.1.278 | ANTHROPIC_BASE_URL | **LIVE** — completed via gateway (benign unknown-model warning) |
| 2 | Codex CLI | codex | 0.153.3 | OPENAI_BASE_URL | **BLOCKED** — ChatGPT-account auth present; rejects custom model ids (known broken auth, needs `codex login`) |
| 3 | OpenCode | opencode | 1.15.7 | config.yaml | pending (has 75+ providers incl. OpenAI-compat) |
| 4 | Gemini CLI | gemini | 0.60.0 | GOOGLE_GEMINI_BASE_URL | **GATED** — expects Gemini-protocol auth, not OpenAI-compat; needs `gemini` auth |
| 5 | Cursor CLI | cursor-agent | 2026.09.15 | — | pending (own model backend) |
| 6 | Devin CLI | devin | 3000.10.31 | — | pending (Devin Cloud) |
| 7 | Grok CLI | grok | 1.0.37 | — | pending (xAI) |
| 8 | Kimi CLI | kimi | 0.43.1 | — | pending (Moonshot) |
| 9 | Qwen Code | qwen | 0.24.1 | OPENAI_BASE_URL | **PARTIAL** — reaches gateway but tool schema (missing `parameters`) rejected with 422 |
| 10 | Goose | goose | 1.51.0 | GOOSE_PROVIDER=openai + OPENAI_BASE_URL | **LIVE** |
| 11 | Aider | aider | 0.86.2 | `--openai-api-base` | **LIVE** (`openai/<model>` prefix + `/v1`) |
| 12 | Crush | crush | 0.95.0 | crush.json provider | **LIVE** (`openai-compat` type, `$OPENLLM_API_KEY`) |
| 13 | Pi | pi | 0.73.1 | ~/.pi/agent/models.json | **LIVE** (custom provider, `openai-completions`) |
| 14 | MiniMax mmx | mmx | 1.0.26 | — | pending (MiniMax token plan; mmx agent setup supports claude/codex/grok/opencode/hermes/pi) |
| 15 | CommandCode | cmd | 1.58.0 | own gateway | works (own 72-model catalog; itself a gateway, not an OpenLLM client) |
| 16 | Amp | — | — | not installed | Sourcegraph; install path unresolved |
| 17 | mcode | — | — | not installed | `curl -fsSL https://filecdn.minimax.chat/public/install.sh | bash` |
| 18 | Claude Squad | claude-squad | 1.0.20 | — | installed; not tested |

## OpenLLM attach methods that WORK (per harness type)

1. **OpenAI-compatible base URL** — Pi, Aider, Crush, Goose. Point `base_url` at
   `http://127.0.0.1:8787/v1`, key from `$OPENLLM_API_KEY`.
2. **Anthropic-compatible base URL** — Claude Code. `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`.
3. **MCP (stdio)** — Hermes (bots/hermes), Cursor (bots/cursor). `openllm mcp` exposes 43 tools.
4. **Env var gateways** — harnesses that read `OPENAI_BASE_URL`/`GOOGLE_GEMINI_BASE_URL` natively.

## Gotchas found

- **OpenLLM chain aliases route per-harness.** `lite` → claude_code (declined) + chatgpt (needs codex CLI signed in). Direct model ids (`grok/grok-4.5`, `kimi_code/*`) are the reliable path.
- **Qwen tool schema** sends a tool without `parameters`; gateway 422s. Either fix on Qwen side (settings) or gateway tolerates missing `parameters`.
- **Codex ChatGPT-account auth** overrides `OPENAI_BASE_URL`; needs `codex login` re-auth or API-key-mode config.
- **Gemini CLI** is Google-protocol only; OpenAI-compat base URL won't work.
- **Crush `providers.json`** is regenerated on `crush models` — use `~/.config/crush/crush.json` (survives).
- **Reasoning models ignore `max_tokens`** (kimi); drop the cap for clean responses.
