"""
Demo 06: Chain-of-Thought — from prompt trick to API parameter
Block 4 — Run: uv run python code_snippets/06_cot.py
Shows: the same problem with reasoning off, with a hand-written CoT prompt, and with reasoning on
"""
import time

from common import MODEL, REASONING_OFF, client, reasoning_tokens

PROBLEM = """When I was 6, my sister was half my age. Now I am 70.
In a room there are me, my sister, and our mother, who was 25 when I was born.
What is the sum of our three ages?"""

RUNS = [
    ("Reasoning off, answer only", PROBLEM + "\nAnswer with the number only.", REASONING_OFF),
    ("Reasoning off, 'think step by step' (the 2022 trick)", PROBLEM + "\n\nLet's think step by step.", REASONING_OFF),
    ("Reasoning effort = low (the 2026 parameter)", PROBLEM, {"reasoning_effort": "low"}),
    ("Reasoning effort = high", PROBLEM, {"reasoning_effort": "high"}),
]

for title, prompt, effort in RUNS:
    print(f"\n{'='*60}")
    print(title)
    print(f"{'='*60}")
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=4000,
        **effort,
    )
    elapsed = time.perf_counter() - started
    print(response.choices[0].message.content.strip())
    print(f"\n  visible output tokens: {response.usage.completion_tokens - reasoning_tokens(response)}")
    print(f"  hidden reasoning tokens (billed): {reasoning_tokens(response)}")
    print(f"  time: {elapsed:.1f}s")

print()
print("Correct answer: 232  (me 70 + sister 67, three years younger + mother 95)")
