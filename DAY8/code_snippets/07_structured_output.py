"""
Demo 07: Structured Output — Prompt-Only vs Schema-Enforced
Block 5 — Run: uv run python code_snippets/07_structured_output.py
Shows: the difference between asking for JSON and enforcing a schema
"""
from pydantic import BaseModel

from common import MODEL, REASONING_OFF, client

TEXT = """Our trip to Tokyo starts on June 12th, 2026. We're staying for 5 nights
at the Park Hyatt before heading to Kyoto."""

print("=== METHOD 1: Prompt-Only ===")
print("(Ask nicely for JSON — no guarantees)\n")
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Extract travel info as JSON with fields: destination, start_date, stay_duration"},
        {"role": "user", "content": TEXT},
    ],
    **REASONING_OFF,
)
print(response.choices[0].message.content)
print()

print("=== METHOD 2: Schema-Enforced ===")
print("(Pydantic model + parse — guaranteed structure)\n")


class TravelInfo(BaseModel):
    destination: str
    start_date: str
    stay_duration: int


response = client.responses.parse(
    model=MODEL,
    instructions="Extract travel information from the text. Use YYYY-MM-DD for dates.",
    input=TEXT,
    text_format=TravelInfo,
)

travel = response.output_parsed
print(f"Destination:    {travel.destination}")
print(f"Start date:     {travel.start_date}")
print(f"Stay duration:  {travel.stay_duration} nights")
print(f"Python type:    {type(travel).__name__}  (not a string!)")
