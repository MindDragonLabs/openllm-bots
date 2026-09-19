#!/usr/bin/env python3
"""Template CLI for the emulated OpenLLM connector.

Wraps an OpenAI-compatible gateway (openllm.sh) with stdlib only.

Auth: the sk-llm key is injected at call time by the generated auth helper
(see docs/03-credential-setup.md). This template reads it from the
OPENLLM_API_KEY environment variable for local testing ONLY — the production
skill must never take the key from the environment, a file, or chat.

Usage:
    openllm_cli.py chat --model <id-or-chain> --message "hello"
    openllm_cli.py models
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def _headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _post(base_url, api_key, path, payload, timeout=120):
    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=json.dumps(payload).encode(),
        headers=_headers(api_key),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(2)


def _get(base_url, api_key, path, timeout=30):
    req = urllib.request.Request(
        base_url.rstrip("/") + path, headers=_headers(api_key), method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(2)


def cmd_chat(args, base_url, api_key):
    payload = {
        "model": args.model,
        "messages": [],
    }
    if args.system:
        payload["messages"].append({"role": "system", "content": args.system})
    payload["messages"].append({"role": "user", "content": args.message})
    if args.max_tokens:
        payload["max_tokens"] = args.max_tokens
    if args.temperature is not None:
        payload["temperature"] = args.temperature

    data = _post(base_url, api_key, "/chat/completions", payload)
    choice = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    print(choice)
    print("---")
    print(json.dumps({
        "model_served": data.get("model"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }))


def cmd_models(args, base_url, api_key):
    data = _get(base_url, api_key, "/models")
    for m in data.get("data", []):
        print(m.get("id"))


def main():
    p = argparse.ArgumentParser(description="OpenLLM gateway CLI (template)")
    p.add_argument("--base-url", default=os.environ.get("OPENLLM_BASE_URL"),
                   help="Gateway base URL (from the openllm.sh dashboard)")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("chat", help="Run a chat completion")
    c.add_argument("--model", required=True, help="Model id or chain name")
    c.add_argument("--message", required=True, help="User message")
    c.add_argument("--system", default=None, help="System prompt")
    c.add_argument("--max-tokens", type=int, default=None)
    c.add_argument("--temperature", type=float, default=None)

    sub.add_parser("models", help="List available models/chains")

    args = p.parse_args()
    if not args.base_url:
        print("Set --base-url or OPENLLM_BASE_URL (from the dashboard).",
              file=sys.stderr)
        sys.exit(2)
    # Template only: production skill injects the key via the auth helper.
    api_key = os.environ.get("OPENLLM_API_KEY")
    if not api_key:
        print("OPENLLM_API_KEY is not set (template mode).", file=sys.stderr)
        sys.exit(2)

    if args.cmd == "chat":
        cmd_chat(args, args.base_url, api_key)
    elif args.cmd == "models":
        cmd_models(args, args.base_url, api_key)


if __name__ == "__main__":
    main()
