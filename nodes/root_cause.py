#nodes/root_cause.py
from state import IncidentState
from llm.llm_utils import invoke_json


def root_cause_analyzer(state: IncidentState, llm) -> IncidentState:
    prompt = f"""
You are an SRE root cause analysis agent.

Validated hypotheses:
{[h for h in state['hypotheses'] if h['status'] == 'VALID']}

Determine the single most likely root cause.

Respond ONLY in JSON:
{{
  "root_cause": "string",
  "confidence": 0.0-1.0,
  "supporting_evidence": ["string"]
}}
"""

    root_cause = invoke_json(llm, prompt)
    state["root_cause"] = root_cause
    return state
