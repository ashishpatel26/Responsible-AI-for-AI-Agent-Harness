"""Concept 5 - Trust: audit every run and evaluate before release.

    python 05_trust.py
"""
from agno.agent import Agent
from agno.eval.reliability import ReliabilityEval
from agno.tools import tool

from common import TOOL_INSTRUCTIONS, banner, local_model


@tool
def get_marks(student_id: str) -> str:
    """Return the marks of one student."""
    return f"{student_id}: 82"


def audit(run_output, run_context):
    """Post-hook: one audit record per run (send it to your log store in production)."""
    print({"user": run_context.user_id,
           "run": run_output.run_id,
           "tools": [t.tool_name for t in run_output.tools or []]})


agent = Agent(model=local_model(), tools=[get_marks], post_hooks=[audit],
              instructions=TOOL_INSTRUCTIONS)

banner("Trust demo")
resp = agent.run("What are the marks of student s1?", user_id="s1")
result = ReliabilityEval(agent_response=resp, expected_tool_calls=["get_marks"]).run(print_results=True)
