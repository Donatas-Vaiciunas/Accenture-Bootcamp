"""
Demo 04: System Prompt Persona Swap
Block 4 — Run: uv run python code_snippets/04_system_prompts.py
Shows: same question, 3 system prompts = 3 completely different answers
"""
from common import MODEL, REASONING_OFF, client

QUESTION = "Explain what a neural network is."

PERSONAS = {
    "University Professor": "You are a university professor teaching beginners. Use simple language and analogies.",
    "Senior ML Engineer": "You are a senior ML engineer explaining to your team. Be precise and technical.",
    "Stand-Up Comedian": "You are a stand-up comedian explaining tech concepts. Be funny and use jokes.",
}

for name, system_prompt in PERSONAS.items():
    print(f"\n{'='*60}")
    print(f"PERSONA: {name}")
    print(f"{'='*60}")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": QUESTION},
        ],
        max_completion_tokens=200,
        **REASONING_OFF,
    )
    print(response.choices[0].message.content.strip())
