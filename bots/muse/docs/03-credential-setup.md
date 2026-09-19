# 03 — Credential setup

Collect the key with `credentials.request_api_access`. Do not ask for the key
in chat, and do not offer to.

## The call

```
credentials.request_api_access(
  provider     = "openllm",
  auth_scheme  = "api_key",
  placement    = "bearer_header",
  api_hosts    = ["<bare hostname from the dashboard, e.g. api.openllm.sh>"],
)
```

- `provider` becomes the connector id `custom.openllm`.
- `placement: bearer_header` matches the OpenAI-compatible
  `Authorization: Bearer sk-llm…` scheme.
- `api_hosts` must be exact: egress to unlisted hosts is refused, and a wrong
  host means sending a fresh card and having the user re-enter the key.

The tool returns a secure entry card (embed token / capture link). Place it on
its own line in your reply with one short reassurance: the key goes straight to
the Secure Vault and nobody, including you, can read it back. Then stop — a
submission from the card resumes the conversation on its own.

## After the key lands

Scaffold the skill so the credential mechanics are generated from authd — do
not hand-write them:

```
/opt/hatch/skills/skill-creator/bin/scaffold-connector-skill --provider openllm
```

It writes `~/workspace/skills/openllm/SKILL.md` whose **Tooling** and **Auth**
sections carry the generated helper import, where the key goes, the allowed
hosts, and the rotation procedure. Leave those two sections as generated.

Copy that helper import into `bin/openllm_cli.py` (FILL). The template
expects a function named `get_bearer_token()` that returns the bearer
token string — confirm the name against scaffold output. Production must
not read `OPENLLM_API_KEY`; that env var is only for `--local-test` /
`OPENLLM_LOCAL_TEST=1`. Fill `ALLOWED_API_HOSTS` from the `api_hosts`
passed to `request_api_access` (or set `OPENLLM_API_HOSTS`).

## Rotation

If the key is revoked, rotated, or a real request carrying it is rejected with
401/403, call `request_api_access` again with the same parameters plus
`reconnect: true`. Replacing is destructive — only do it when the current
credential is proven bad (see `09-troubleshooting.md`).
