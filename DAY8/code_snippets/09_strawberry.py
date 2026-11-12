"""
Demo 09: The Strawberry Problem — Letter Counting
Block 6 — Run: uv run python code_snippets/09_strawberry.py
Shows: tokenization prevents character counting; reasoning does the spell-out trick for you
"""
from common import MODEL, REASONING_OFF, client

WORD = "cranberry"
SENTENCE = "The referee preferred raspberry sherbet over a cranberry tart."
QUESTIONS = [
    (f"How many R's are in the word '{WORD}'? Answer with the number only.", WORD.lower().count("r")),
    (f"How many times does the letter 'r' appear in this sentence? Answer with the number only.\n\n{SENTENCE}", SENTENCE.lower().count("r")),
]


def ask(prompt, **effort):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=4000,
        **effort,
    )
    return response.choices[0].message.content.strip()


print("=== 1. Reasoning OFF ===")
for question, truth in QUESTIONS:
    print(f"Q: {question.splitlines()[0]}")
    print(f"   Model says: {ask(question, **REASONING_OFF)}    Correct: {truth}\n")

print(f"{'='*60}")
print("=== 2. Reasoning OFF + spell it out by hand (CoT for characters) ===")
print(ask(
    f"""How many R's are in '{WORD}'?
First, write out each character separated by dashes.
Then count the R's one by one, numbering each one you find.
Finally, give the total.""",
    **REASONING_OFF,
))

print(f"\n{'='*60}")
print("=== 3. Reasoning ON, no prompt tricks ===")
for question, truth in QUESTIONS:
    print(f"Q: {question.splitlines()[0]}")
    print(f"   Model says: {ask(question, reasoning_effort='medium')}    Correct: {truth}\n")

print("The spell-it-out trick from step 2 is what reasoning does internally in step 3.")
