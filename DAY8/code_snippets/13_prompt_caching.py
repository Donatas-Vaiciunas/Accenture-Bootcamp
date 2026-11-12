"""
Demo 13: Prompt Caching (Optional)
Block 2 — Run: uv run python code_snippets/13_prompt_caching.py
Shows: the same long prefix sent twice; the second call reads it from the cache
"""
from common import MODEL, REASONING_OFF, client

POLICY = "\n".join(
    f"Rule {number}: Support tickets in category {number} are answered within {number % 7 + 1} working days "
    f"and escalated to tier {number % 3 + 1} when the customer mentions a deadline or a contract."
    for number in range(1, 151)
)
SYSTEM = "You are a support assistant. Answer strictly from this policy.\n\n" + POLICY

for question in ["How fast is category 12 answered?", "Which tier handles escalations for category 40?"]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        max_completion_tokens=100,
        **REASONING_OFF,
    )
    usage = response.usage
    cached = usage.prompt_tokens_details.cached_tokens if usage.prompt_tokens_details else 0
    print(f"Q: {question}")
    print(f"A: {response.choices[0].message.content.strip()}")
    print(f"   input tokens: {usage.prompt_tokens}   read from cache: {cached}\n")

print("Same prefix, second call: most input tokens come from the cache,")
print("billed at about a tenth of the price. Stable part first, question last.")
