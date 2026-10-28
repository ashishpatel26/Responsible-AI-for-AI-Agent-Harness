"""Shared settings for every demo: a local Ollama model, no OpenAI key needed.

Change the model without editing code:
    export OLLAMA_MODEL=llama3.1:8b
    export OLLAMA_HOST=http://localhost:11434
"""
import os

from agno.models.ollama import Ollama

# Pick a model that supports tool calling, e.g. qwen2.5:7b, llama3.1:8b, qwen3:8b
MODEL_ID = os.getenv("OLLAMA_MODEL", "qwen3.5-4b-16k:latest")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Small local models follow tools more reliably with a clear instruction
TOOL_INSTRUCTIONS = [
    "Always use the available tools to answer questions about marks or to send email.",
    "Pass the student id exactly as written by the user, for example s2.",
    "After a tool returns, report its result to the user in one short sentence.",
]


def local_model() -> Ollama:
    """Return the Ollama chat model used by all demos."""
    return Ollama(id=MODEL_ID, host=HOST)


def banner(title: str) -> None:
    print("\n" + "=" * 64 + f"\n{title}\n" + f"model: {MODEL_ID} @ {HOST}\n" + "=" * 64)
