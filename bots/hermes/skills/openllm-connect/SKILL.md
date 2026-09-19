---
name: openllm-connect
description: Attach, verify, or repair the OpenLLM MCP server on Hermes. Use when mcp_openllm tools are missing, auth fails, or the server will not start.
---

# Connect OpenLLM MCP (Hermes)

Wire the official unified MCP server (`openllm mcp`) into a Hermes profile. Full copy-paste: [docs/setup.md](../../docs/setup.md). Concepts: [shared/openllm-connect.md](../../../../shared/openllm-connect.md).

## Checklist (in order)

1. `openllm version` on the Hermes host — CLI present and ≥ 2.6.
2. `OPENLLM_API_KEY` (and optional `OPENLLM_CLOUD_ORIGIN`) in the **profile** `.env` — `hermes config env-path` for the path. Not just `~/.openllm/.env`: daemon pairing does not automatically authenticate a profile.
3. Register (default profile shown; add `--profile <name>` otherwise):

   ```sh
   hermes mcp add openllm --command openllm --connect-timeout 30 \
     --env 'OPENLLM_API_KEY=${OPENLLM_API_KEY}' 'OPENLLM_CLOUD_ORIGIN=${OPENLLM_CLOUD_ORIGIN}' \
     --args mcp
   ```

   Pitfalls (verified): `--args` swallows everything after it — keep it **last**; the tool-enable prompt needs stdin — pipe `printf 'y\n' |` in scripts.

4. `hermes mcp test openllm` — expect Connected + ~43 tools on CLI 2.6.36 (live count wins).
5. New session (`/reset`, fresh `hermes` run, gateway restart) — MCP loads at session start.

## Verify auth, not just connection

`mcp test` proves transport. Make one authenticated call — `whoAmI` or `api_user_me` — and check it returns your account, not an error. Env interpolation (`${OPENLLM_API_KEY}` from profile `.env` → server env) is the usual silent failure.

## Remote MCP / SSE

Only if the OpenLLM dashboard shows a real MCP/SSE URL: `hermes mcp add openllm --url <URL_FROM_DASHBOARD> --auth header`. Never invent the URL. Default stays stdio.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server fails to start / `command not found` | Absolute binary path in `--command` (`command -v openllm`), or `npx -y @openllmsh/npm mcp`. |
| Connected but auth errors | Key missing from **profile** `.env`; typo; wrong account → `OPENLLM_CLOUD_ORIGIN` (host origin, no `/v1`). |
| Env vars inside `args` in config.yaml | Re-add; `--args mcp` must be the last flag. |
| 0 tools discovered | Old CLI; upgrade. |
| Tools missing in a live session | New session or `/reload-mcp`. |
| Wrong Hermes profile touched | `--profile <name>` on every command; config lives at `~/.hermes/profiles/<name>/config.yaml`. |
