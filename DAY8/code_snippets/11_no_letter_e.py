"""
Demo 11: Constrained Generation — No Letter 'E'
Block 6 — Run: uv run python code_snippets/11_no_letter_e.py
Shows: character-level constraints are hard at the token level; reasoning helps, at a price
"""
from common import MODEL, REASONING_OFF, client, reasoning_tokens

PROMPT = "Write an 8-sentence story about a cat. Do NOT use the letter 'e' anywhere in your response."


def attempt(title, **effort):
    print(f"\n{'='*60}")
    print(f"=== {title} ===")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        max_completion_tokens=8000,
        **effort,
    )
    text = response.choices[0].message.content.strip()
    e_count = text.lower().count("e")
    print(text.replace("e", "[E]").replace("E", "[E]") if e_count else text)
    print(f"\nLetter 'e' count: {e_count}   hidden reasoning tokens: {reasoning_tokens(response)}")


attempt("Reasoning OFF", **REASONING_OFF)
attempt("Reasoning ON (effort = high)", reasoning_effort="high")

print()
print("=" * 60)
print("TEACHING POINT: generation happens at the TOKEN level, not the")
print("CHARACTER level. The token 'the' is atomic — the model cannot")
print("'see inside' it. Reasoning lets it draft, check and rewrite,")
print("and you pay for every hidden token of that.")
