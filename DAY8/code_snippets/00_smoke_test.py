"""
Demo 00: Pre-session smoke test
Run the evening before: uv run python code_snippets/00_smoke_test.py
Shows: which deployments answer, and which parameters each one accepts
"""
import os

from anthropic import AnthropicFoundry
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_CANDIDATES = ["gpt-5.4-mini", "gpt-5.6-luna", "gpt-6-luna", "gpt-6.1-terra", "gpt-6.1-sol", "gpt-5.6", "gpt-4.1-mini", "gpt-4.1"]
CLAUDE_CANDIDATES = ["claude-sonnet-5-5", "claude-haiku-5-5", "claude-opus-5-5", "claude-sonnet-4-5"]
MESSAGES = [{"role": "user", "content": "Reply with the single word: ok"}]

client = OpenAI(
    base_url=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    timeout=20,
    max_retries=0,
)
print(f"OpenAI endpoint: {client.base_url}")


def probe(label, call):
    try:
        call()
        return f"{label}: yes"
    except Exception as exc:
        reason = str(getattr(exc, "message", exc)).replace("\n", " ")[:90]
        return f"{label}: NO ({type(exc).__name__}: {reason})"


print("=== OpenAI deployments ===")
for model in OPENAI_CANDIDATES:
    base = probe("answers", lambda: client.chat.completions.create(model=model, messages=MESSAGES, max_completion_tokens=200))
    print(f"\n{model}\n  {base}")
    if "NO" in base:
        continue
    checks = {
        "temperature (default effort)": dict(temperature=0.7),
        "effort=none": dict(reasoning_effort="none"),
        "effort=none + temperature": dict(reasoning_effort="none", temperature=0.7),
        "effort=medium": dict(reasoning_effort="medium"),
        "effort=medium + temperature": dict(reasoning_effort="medium", temperature=0.7),
        "verbosity=low": dict(verbosity="low"),
        "legacy max_tokens": dict(max_tokens=200, max_completion_tokens=None),
    }
    for label, extra in checks.items():
        params = {"model": model, "messages": MESSAGES, "max_completion_tokens": 200, **extra}
        params = {k: v for k, v in params.items() if v is not None}
        print("  " + probe(label, lambda: client.chat.completions.create(**params)))
    print("  " + probe("responses API", lambda: client.responses.create(model=model, input="Reply with the single word: ok")))

print("\n=== Claude deployments ===")
claude = AnthropicFoundry(
    base_url=os.environ.get("AZURE_ANTHROPIC_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_ANTHROPIC_API_KEY"),
)
for model in CLAUDE_CANDIDATES:
    print(f"\n{model}")
    print("  " + probe("answers", lambda: claude.messages.create(model=model, messages=MESSAGES, max_tokens=1024)))
