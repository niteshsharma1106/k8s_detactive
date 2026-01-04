#nodes/event_interpreter.py
from state import IncidentState
from llm.llm_utils import invoke_json


def event_interpreter(state: IncidentState, llm) -> IncidentState:
    prompt = f"""
You are an SRE incident classification agent.

Classify the following Kubernetes/OpenShift event.

Event:
{state['event']}

Respond ONLY in JSON:
{{
  "incident_type": "application|infrastructure|network|security|storage",
  "scope": "pod|deployment|node|cluster",
  "confidence": 0.0-1.0,
  "rationale": "short explanation"
}}
"""

    classification = invoke_json(llm, prompt)

    state["classification"] = classification
    return state
