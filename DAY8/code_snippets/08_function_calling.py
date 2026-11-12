"""
Demo 08: Function Calling
Block 5 — Run: uv run python code_snippets/08_function_calling.py
Shows: the model decides to call a function and generates structured arguments.
The model does NOT execute the function — YOUR code does.
"""
import json

from common import MODEL, client

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name, e.g. 'Tokyo' or 'Berlin'"},
                "unit": {"type": ["string", "null"], "enum": ["celsius", "fahrenheit", None]},
            },
            "required": ["location", "unit"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def get_weather(location, unit):
    return {"location": location, "temperature": 12, "unit": unit or "celsius", "conditions": "light rain"}


response = client.responses.create(
    model=MODEL,
    input="What's the weather like in Tokyo?",
    tools=tools,
)

call = next(item for item in response.output if item.type == "function_call")
args = json.loads(call.arguments)

print("=== Step 1: the model asks for a tool call ===")
print(f"Function:  {call.name}")
print(f"Arguments: {call.arguments}")
print()
print("The model did NOT get the weather. It told us WHAT to fetch.")

result = get_weather(**args)
print("\n=== Step 2: OUR code runs the function ===")
print(f"Result:    {result}")

final = client.responses.create(
    model=MODEL,
    previous_response_id=response.id,
    input=[{"type": "function_call_output", "call_id": call.call_id, "output": json.dumps(result)}],
    tools=tools,
)
print("\n=== Step 3: the model answers with our result ===")
print(final.output_text)
print()
print("Once = function calling. In a loop until the model stops asking = an agent (Day 13).")
