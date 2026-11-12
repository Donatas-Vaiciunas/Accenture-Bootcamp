"""
Demo 03: Temperature Comparison
Block 3 — Run: uv run python code_snippets/03_temperature.py
Shows: same prompt at 3 temperatures with reasoning off, then the same call with reasoning on
"""
from openai import BadRequestError

from common import MODEL, REASONING_OFF, client

PROMPT = "Write a one-sentence opening for a mystery novel."
TEMPERATURES = [0.0, 0.7, 1.5]
RUNS = 3

for temp in TEMPERATURES:
    print(f"\n{'='*60}")
    print(f"TEMPERATURE = {temp}   (reasoning off)")
    print(f"{'='*60}")
    for run in range(1, RUNS + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=temp,
            max_completion_tokens=80,
            **REASONING_OFF,
        )
        print(f"  Run {run}: {response.choices[0].message.content.strip()}")

print(f"\n{'='*60}")
print("SAME CALL, TEMPERATURE = 0.7, REASONING ON")
print(f"{'='*60}")
try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.7,
        reasoning_effort="medium",
        max_completion_tokens=2000,
    )
    print(f"  Accepted on this model: {response.choices[0].message.content.strip()}")
except BadRequestError as error:
    print(f"  {error.status_code} Bad Request")
    print(f"  {error.message}")
    print("\n  With reasoning on, this knob does not exist. The knob is effort.")
