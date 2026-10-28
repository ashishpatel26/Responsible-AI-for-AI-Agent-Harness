"""Concept 2 - Privacy: mask PII (email, PAN, Aadhaar) before the model sees it.

    python 02_privacy.py
"""
from agno.agent import Agent
from agno.guardrails import PIIDetectionGuardrail

from common import banner, local_model

pii = PIIDetectionGuardrail(
    mask_pii=True,  # replace matches with asterisks instead of blocking
    custom_patterns={
        "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "PAN": r"\b[A-Z]{5}\d{4}[A-Z]\b",
    },
)

agent = Agent(model=local_model(), pre_hooks=[pii])

banner("Privacy demo")
run = agent.run("Draft feedback for priya@college.edu, PAN ABCDE1234F", user_id="faculty-7")

print("\n# What the model actually received:")
for m in run.messages or []:
    if m.role == "user":
        print(m.content)
print("\n# Model reply:")
print(run.content)
