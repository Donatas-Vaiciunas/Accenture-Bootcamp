"""
Demo 05: Zero-Shot vs Few-Shot Ticket Routing
Block 4 — Run: uv run python code_snippets/05_few_shot.py
Shows: few-shot examples teach YOUR label set and format, which the model cannot guess
"""
from common import MODEL, REASONING_OFF, client

SYSTEM = "You route IT support tickets to a queue. Respond with the queue name only."

TICKETS = [
    "I was charged twice for my software licence this month.",
    "My laptop screen flickers when I plug in the docking station.",
    "I can't log in to the HR portal since my password expired.",
]

EXAMPLES = [
    ("The invoice for our team subscription shows the wrong VAT rate.", "FIN-BILLING-L2"),
    ("My keyboard has two dead keys.", "HW-DESKSIDE"),
    ("Please give me access to the finance shared drive.", "IAM-ACCESS"),
]


def route(ticket, examples=()):
    messages = [{"role": "system", "content": SYSTEM}]
    for example_ticket, queue in examples:
        messages.append({"role": "user", "content": example_ticket})
        messages.append({"role": "assistant", "content": queue})
    messages.append({"role": "user", "content": ticket})
    response = client.chat.completions.create(
        model=MODEL, messages=messages, max_completion_tokens=30, **REASONING_OFF
    )
    return response.choices[0].message.content.strip()


print("=== ZERO-SHOT: the model invents queue names ===")
for ticket in TICKETS:
    print(f"  {route(ticket):<28} <- {ticket}")

print("\n=== FEW-SHOT (3 examples): the model uses our queue names ===")
for ticket in TICKETS:
    print(f"  {route(ticket, EXAMPLES):<28} <- {ticket}")

print()
print("Key insight: the model already knows what a billing problem is.")
print("The examples teach the FORMAT and the LABEL SET it could not know.")
