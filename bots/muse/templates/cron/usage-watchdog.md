# Template: OpenLLM spend watchdog (cron job body)

Use with `cron.add`. Fill in the bracketed values.

- id: `openllm-spend-watchdog`
- title: `OpenLLM spend watchdog`
- mode: `task`
- schedule: daily, flexible_time: true (pick an hour that fits; the runtime
  chooses the minute)
- predicted_connector_permissions: the usage endpoint actually used, e.g.
  `[{"connector":"custom.openllm","method":"usage.read"}]` — adjust to the
  real method name once the skill exists.

## Body

> Check the user's openllm.sh spend for the scoped `muse-connector` key
> against its cap ([FILL: cap, e.g. $25/mo]).
>
> 1. Query gateway usage for the key by running `bin/openllm_cli.py usage`
>    (the skill's usage path). FILL `--usage-path` if the dashboard
>    documents a path other than `/usage`.
> 2. If spend < 80% of cap: stay silent (no user message).
> 3. If 80–95%: send the user a short note with current spend vs. cap.
> 4. If > 95%: warn clearly and suggest pausing batched work until the cap
>    resets or is raised.
>
> Log one line to the daily memory log: date, tokens used, spend vs. cap.
> Never log prompts or completions.
