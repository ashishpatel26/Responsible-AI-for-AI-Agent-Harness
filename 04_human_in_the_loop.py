"""Concept 4 - Human-in-the-loop: the run pauses until a person approves.

    python 04_human_in_the_loop.py
"""
from agno.agent import Agent
from agno.tools import tool

from common import TOOL_INSTRUCTIONS, banner, local_model


@tool(requires_confirmation=True)
def send_parent_email(to: str, body: str) -> str:
    """Send an email to a parent (pretend)."""
    return f"sent to {to}"


agent = Agent(model=local_model(), tools=[send_parent_email], instructions=TOOL_INSTRUCTIONS)

banner("Human-in-the-loop demo")
run = agent.run("Email parent@example.com that attendance this month is 61%.")

if run.is_paused:
    for req in run.active_requirements:
        print("Approve?", req.tool_execution.tool_name, req.tool_execution.tool_args)
        ok = input("[y/N] ").strip().lower() == "y"
        req.confirm() if ok else req.reject(note="Not approved by faculty")
    run = agent.continue_run(run)
else:
    print("(The model did not call the tool. Try a larger model or rephrase.)")

print(run.content)
