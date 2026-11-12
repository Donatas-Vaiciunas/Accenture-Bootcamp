"""
Demo 01: First OpenAI API Call
Block 2 — Run: uv run python code_snippets/01_first_api_call.py
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
)

response = client.chat.completions.create(
    model=os.environ.get("OPENAI_DEMO_MODEL", "gpt-5.4-mini"),
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Be concise."},
        {"role": "user", "content": "What is artificial intelligence? Answer in 2 sentences."},
    ],
    max_completion_tokens=200,
)

print("=== Response Metadata ===")
print(f"Model:          {response.model}")
print(f"Finish reason:  {response.choices[0].finish_reason}")
print(f"Input tokens:   {response.usage.prompt_tokens}")
print(f"Output tokens:  {response.usage.completion_tokens}")
print(f"Total tokens:   {response.usage.total_tokens}")
print()
print("=== The Answer ===")
print(response.choices[0].message.content)
