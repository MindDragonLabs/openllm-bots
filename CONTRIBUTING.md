# Contributing

Thank you for helping with [openllm-bots](https://github.com/MindDragonLabs/openllm-bots). This repo is a **standardized multi-bot monorepo**: each orchestrator gets `bots/<name>/`. All bots share OpenLLM as the model fabric.

## Ground rules

- **No secrets.** Never commit `OPENLLM_API_KEY`, provider credentials, `.env` files, or remote MCP URLs you do not control.
- **Do not invent OpenLLM tool names or remote MCP endpoints.** Discover tools from a live `openllm mcp` session. Remote/SSE URLs come only from the OpenLLM dashboard.
- **Keep the role split.** The bot is the orchestrator. OpenLLM is model fabric. GitHub, Vercel, and other products stay on their own connectors.
- **Stubs stay stubs.** Do not add placeholder skills or fake MCP configs for hosts that are not ready.

## Adding `bots/<name>`

1. Pick a lowercase folder name (`bots/muse`, `bots/hermes`, `bots/my-host`, …). Use the same string as `id` in the manifest.
2. Create at least:

   ```text
   bots/<name>/
   ├── README.md
   └── bot.manifest.json
   ```

3. Fill `bot.manifest.json` using this schema:

   ```json
   {
     "id": "<name>",
     "displayName": "Human name",
     "host": "grok-bot | cursor | muse | hermes | other",
     "status": "ready | stub | experimental",
     "description": "…",
     "openllm": {
       "mcp": "stdio",
       "command": "openllm",
       "args": ["mcp"],
       "env": ["OPENLLM_API_KEY", "OPENLLM_CLOUD_ORIGIN"]
     },
     "paths": {
       "skills": "skills",
       "docs": "docs"
     }
   }
   ```

   For a **stub**, `status` is `"stub"`. The README should say the folder is reserved, point at [shared/architecture.md](./shared/architecture.md) and [shared/openllm-connect.md](./shared/openllm-connect.md), and skip fake skills.

4. For a **ready** bot, add host-specific material:

   | Path | Purpose |
   | --- | --- |
   | `skills/<skill>/SKILL.md` | Host-oriented skills (YAML `name` + `description` frontmatter) |
   | `docs/setup.md` | Copy-paste attach steps for that host |
   | `README.md` | How to use this bot; **relative** links into `shared/` |

   Reuse shared docs with relative links from the bot folder (from `bots/<name>/README.md` that is `../../shared/architecture.md`). Canonical copies live in [shared/architecture.md](./shared/architecture.md) and [shared/openllm-connect.md](./shared/openllm-connect.md). Do not duplicate the fabric story in three places unless the host truly needs different wording.

5. **Cursor plugins** live under `bots/<name>/` with `.cursor-plugin/plugin.json`, `mcp.json`, and the usual `skills/`, `rules/`, `commands/` folders. Then register the plugin in [`.cursor-plugin/marketplace.json`](./.cursor-plugin/marketplace.json):

   ```json
   {
     "name": "your-plugin-id",
     "source": "bots/<name>",
     "description": "…"
   }
   ```

   `plugin.json` `homepage` and `repository` should be `https://github.com/MindDragonLabs/openllm-bots`. Logo paths must stay inside the plugin directory (no `..`). Variables stay `OPENLLM_API_KEY` and `OPENLLM_CLOUD_ORIGIN` (default `https://openllm.sh`). Stdio config should match [shared/mcp.stdio.example.json](./shared/mcp.stdio.example.json).

6. Update the bots table in [README.md](./README.md) and add a [CHANGELOG.md](./CHANGELOG.md) entry.

## What not to put in a bot folder

- API keys, sample keys, or “example” remote MCP URLs
- A second copy of OpenLLM that pretends to be GitHub or Vercel
- Skills that hard-code MCP function names instead of discovering the live list

## CLI install

Document the official installer the same way [shared/openllm-connect.md](./shared/openllm-connect.md) does (review, then run):

```sh
curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash
openllm version
```

## Pull requests

- One concern per PR when you can.
- Keep relative links working from the files you touch.
- MIT license already covers contributions.
