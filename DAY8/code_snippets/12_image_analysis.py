"""
Demo 12: Multimodal — Image Analysis via API (Optional)
Nice-to-have N1 — Run: uv run python code_snippets/12_image_analysis.py
Shows: sending an image to the API and getting a description back
"""
import base64
from pathlib import Path

from common import MODEL, client

IMAGE = Path(__file__).parents[1] / "images" / "transformer_architecture.png"
encoded = base64.b64encode(IMAGE.read_bytes()).decode()

print(f"=== Analyzing {IMAGE.name} ===\n")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What does this diagram show? Describe it in 2-3 sentences."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}},
            ],
        }
    ],
    max_completion_tokens=1000,
)

print(response.choices[0].message.content.strip())
print()
print("Key insight: The same API pattern works for text AND images.")
print("Any input, text out is standard on current models.")
