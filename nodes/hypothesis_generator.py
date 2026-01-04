#nodes/hypothesis_generator.py
from state import IncidentState
from llm.llm_utils import invoke_json


def hypothesis_generator(state: IncidentState, llm) -> IncidentState:
    prompt = f"""
You are an SRE investigator.

Based on the incident classification and evidence summary below,
generate plausible hypotheses.

Classification:
{state['context'].get('classification')}

Evidence Summary:
{state['evidence']}

Respond ONLY in JSON:
[
  {{
    "hypothesis": "string",
    "confidence": 0.0-1.0
  }}
]
"""

    hypotheses = invoke_json(llm, prompt)

    state["hypotheses"] = [
        {   
            "hypothesis": h["hypothesis"],
            "confidence": h["confidence"],
            "status": "UNKNOWN",
            "evidence": []
        }
        for h in hypotheses
    ]

    return state
