"""Shared client and model names for the Day 8 demos. Model names come from .env so a deployment rename needs no code change."""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.environ.get("OPENAI_DEMO_MODEL", "gpt-5.4-mini")

client = OpenAI(
    base_url=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
)

# gpt-4.x has no reasoning to switch off and rejects the parameter.
REASONING_OFF = {} if MODEL.startswith("gpt-4") else {"reasoning_effort": "none"}


def reasoning_tokens(response):
    details = response.usage.completion_tokens_details
    return (details.reasoning_tokens or 0) if details else 0
