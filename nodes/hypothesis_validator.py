#nodes/hypothesis_validator.py
from state import IncidentState
from llm.llm_utils import invoke_json


def hypothesis_validator(state: IncidentState, llm) -> IncidentState:
    prompt = f"""
You are validating incident hypotheses.

Hypotheses:
{state['hypotheses']}

Evidence:
{state['evidence']}

For each hypothesis, decide if it is VALID or INVALID.

Respond ONLY in JSON:
[
  {{
    "hypothesis": "string",
    "status": "VALID|INVALID",
    "justification": "short explanation"
  }}
]
"""

    validations = invoke_json(llm, prompt)

    for h in state["hypotheses"]:
        match = next(
            (v for v in validations if v["hypothesis"] == h["hypothesis"]),
            None
        )
        if match:
            h["status"] = match["status"]
            h["evidence"].append(match["justification"])

    return state
