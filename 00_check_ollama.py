"""Step 0: confirm Ollama is running and the model is pulled.

    python 00_check_ollama.py
"""
import sys

import ollama

from common import HOST, MODEL_ID

client = ollama.Client(host=HOST)
try:
    names = [m.model for m in client.list().models]
except Exception as exc:  # server not running
    sys.exit(f"Cannot reach Ollama at {HOST}: {exc}\nStart it with:  ollama serve")

print("Ollama is running. Local models:", ", ".join(names) or "(none)")
if not any(n == MODEL_ID or n.startswith(MODEL_ID + ":") for n in names):
    sys.exit(f"Model '{MODEL_ID}' is not pulled yet. Run:  ollama pull {MODEL_ID}")

reply = client.chat(model=MODEL_ID, messages=[{"role": "user", "content": "Reply with the word ready."}])
print("Model replied:", reply.message.content.strip())
print("All set. Run the demos 01 to 06.")
