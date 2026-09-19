# 09 — Troubleshooting

## 401 / 403 from the gateway

A 401/403 is a question about the **request** before it is a question about
the **key**. Check in order:

1. Was the credential attached at all? A request built without the generated
   auth helper carries nothing — that looks exactly like a wrong key.
2. Is `placement` correct? It must be `bearer_header`
   (`Authorization: Bearer sk-llm…`).
3. Is the base URL right? Confirm against the dashboard; a wrong host fails
   before auth is even evaluated.
4. Is the scoped key revoked, expired, or over its spend cap / in cooldown?
   Check the dashboard.

Only after all four check out should you suspect the key itself — then rotate
via `request_api_access` with `reconnect: true`.

## Key rotation

User revokes or the dashboard shows a new key: re-run `request_api_access`
with identical parameters plus `reconnect: true`, then re-run the scaffold so
the skill picks up the replacement. Test with `models` before resuming work.

## Rate limits / cooldowns

Scoped keys can carry their own cooldowns. On 429: back off, tell the user
how long, and do not retry in a tight loop. Consider routing bulk work to a
different chain.

## Wrong model id

If the gateway rejects a model name, run `models` and show the user what's
actually available. Never guess ids.

## Base URL changes

If the user migrates dashboards or the host changes, the credential's
`api_hosts` must be updated — that means a fresh `request_api_access` (the
host list cannot be edited afterwards) and re-entering the key.
