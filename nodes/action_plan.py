#nodes/action_plan.py
from state import IncidentState
from llm.llm_utils import invoke_json


def action_plan_builder(state: IncidentState, llm) -> IncidentState:
    prompt = f"""
You are an SRE remediation planner.

Root Cause:
{state['root_cause']}

Cluster:
{state['cluster']}
Namespace:
{state['namespace']}

Generate a SAFE, HUMAN-APPROVABLE action plan.
DO NOT assume permissions.

Respond ONLY in JSON:
[
  {{
    "description": "string",
    "command": "exact kubectl/oc command",
    "risk": "LOW|MEDIUM|HIGH"
  }}
]
"""

    plan = invoke_json(llm, prompt)

    state["action_plan"] = plan
    state["status"] = "WAITING_FOR_HUMAN"
    return state
