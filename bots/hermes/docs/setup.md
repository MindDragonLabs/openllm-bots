# Setup — Hermes ↔ OpenLLM

Copy-paste attach steps for [Hermes Agent](https://hermes-agent.nousresearch.com). Concepts, CLI install, and remote MCP rules live in [shared/openllm-connect.md](../../../shared/openllm-connect.md) — this page is only what you run on the Hermes host.

Verified against `openllm` CLI 2.6.36 and Hermes `mcp add`/`mcp test`.

## 1. Install the OpenLLM CLI

On the machine Hermes runs on (review the script, then run):

```sh
curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash
openllm version
```

If the binary is not on PATH for the Hermes process, use the absolute path (`~/.openllm/bin/openllm` or wherever the installer put it — check `command -v openllm`) in the `--command` below. The npm launcher `npx -y @openllmsh/npm mcp` also works.

## 2. Put the key in Hermes' env file

`hermes config env-path` prints the path: `~/.hermes/.env` for the default profile, `~/.hermes/profiles/<name>/.env` for a named profile. Add:

```sh
OPENLLM_API_KEY=sk-llm-...   # from the openllm.sh dashboard
OPENLLM_CLOUD_ORIGIN=https://openllm.sh   # optional, this is the default
```

Keep the key out of git, skills, and chat logs.

Note: if the OpenLLM daemon already paired on this machine (`~/.openllm/.env`), the MCP server may authenticate without the env var. Set it anyway — profiles and daemons drift apart.

## 3. Register the MCP server

For the default profile:

```sh
hermes mcp add openllm --command openllm --connect-timeout 30 \
  --env 'OPENLLM_API_KEY=${OPENLLM_API_KEY}' 'OPENLLM_CLOUD_ORIGIN=${OPENLLM_CLOUD_ORIGIN}' \
  --args mcp
```

For a named profile, prefix `--profile <name>`. Confirm the enable-all-tools prompt (`y`).

Two `hermes mcp add` pitfalls, both verified the hard way:

- **Flag order matters.** `--args` must come **last**; it greedily swallows everything after it. `--env`/`--connect-timeout` after `--args` end up inside `args` in `config.yaml`, and the server runs without the env block.
- **The tool-enable prompt reads stdin.** Piping through a non-interactive shell gives EOF → "Cancelled" and nothing is saved. Feed it: `printf 'y\n' | hermes mcp add …`.

Resulting `config.yaml` shape (spot-check with `grep -A 8 'openllm:' ~/.hermes/config.yaml`):

```yaml
mcp_servers:
  openllm:
    command: openllm
    args:
      - mcp
    env:
      OPENLLM_API_KEY: ${OPENLLM_API_KEY}
      OPENLLM_CLOUD_ORIGIN: ${OPENLLM_CLOUD_ORIGIN}
    connect_timeout: 30.0
    enabled: true
```

`${VAR}` interpolates from the profile `.env` when Hermes spawns the server.

## 4. Verify

```sh
hermes mcp test openllm     # expect: ✓ Connected, Tools discovered: 43 (2.6.36)
hermes mcp list             # expect: openllm … ✓ enabled
```

Then start a **new session** (`hermes` fresh run, `/reset`, or gateway restart) and make one authenticated call — e.g. the `whoAmI` tool — to confirm the env interpolation reached the server.

## 5. Use it

- Tools appear as `mcp_openllm_<name>` (e.g. `mcp_openllm_api_v1Models_list`).
- Dashboard-style questions → the `openllm-dashboard` skill.
- Implementation work → the `openllm-dev-task` skill.
- Install the skills from [`skills/`](../skills/) into the Hermes profile (`~/.hermes/skills/` or `hermes skills install <url>`).

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `mcp test` connects, 0 tools | Old CLI. `openllm version` ≥ 2.6; reinstall from the official script. |
| Auth errors in tool calls | `OPENLLM_API_KEY` missing from the **profile** `.env` (not just `~/.openllm/.env`). Step 2. |
| `command not found` when Hermes spawns it | Use the absolute binary path in `--command`. |
| Env vars landed inside `args` | Re-add with `--args mcp` last (pitfall above). |
| Tools don't show in-session | MCP loads at session start — new session or `/reload-mcp`. |
