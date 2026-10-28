"""Concept 3 - Authorization: a tool hook checks the logged-in user on every call.

    python 03_authorization.py
"""
from agno.agent import Agent
from agno.tools import tool

from common import TOOL_INSTRUCTIONS, banner, local_model


@tool
def get_marks(student_id: str) -> str:
    """Return the marks of one student."""
    return f"{student_id}: 82"


def authorize(function_name, function_call, arguments, run_context):
    """Runs before every tool call. Identity comes from your app, not the model."""
    user, sid = run_context.user_id, arguments.get("student_id")
    if user != sid and user != "faculty-1":
        return f"DENIED: {user} cannot read {sid}"
    return function_call(**arguments)


agent = Agent(
    model=local_model(),
    tools=[get_marks],
    tool_hooks=[authorize],
    instructions=TOOL_INSTRUCTIONS,
)

banner("Authorization demo")
for user in ("s1", "faculty-1"):
    print(f"\n# Request as user {user}")
    run = agent.run("What are the marks of student s2?", user_id=user)
    for t in run.tools or []:
        print("tool call:", t.tool_name, t.tool_args, "->", t.result)
    print("reply:", run.content)
