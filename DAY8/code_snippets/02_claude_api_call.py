"""
Demo 02: Anthropic Claude API Call
Block 2 — Run: uv run python code_snippets/02_claude_api_call.py
Compare with Demo 01 — spot the 3 differences!
"""
import os

from anthropic import AnthropicFoundry
from dotenv import load_dotenv

load_dotenv()

client = AnthropicFoundry(
    base_url=os.environ.get("AZURE_ANTHROPIC_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_ANTHROPIC_API_KEY"),
)

# Difference 1: system prompt is a SEPARATE parameter, not in messages
# Difference 2: max_tokens is REQUIRED, and it covers thinking + answer
response = client.messages.create(
    model=os.environ.get("CLAUDE_DEMO_MODEL", "claude-sonnet-5-5"),
    system="You are a helpful assistant. Be concise.",
    messages=[
        {"role": "user", "content": "What is artificial intelligence? Answer in 2 sentences."},
    ],
    max_tokens=1024,
    output_config={"effort": "low"},
)

print("=== Response Metadata ===")
print(f"Model:          {response.model}")
print(f"Stop reason:    {response.stop_reason}")        # "stop_reason" not "finish_reason"
print(f"Input tokens:   {response.usage.input_tokens}")  # "input_tokens" not "prompt_tokens"
print(f"Output tokens:  {response.usage.output_tokens}")
# Difference 3: content is a LIST of typed blocks; a thinking block can come first
print(f"Content blocks: {[block.type for block in response.content]}")
print()
print("=== The Answer ===")
print(next(block.text for block in response.content if block.type == "text"))
