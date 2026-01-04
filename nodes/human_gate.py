#nodes/human_gate.py
from state import IncidentState
from langgraph.types import interrupt

def human_gate(state):
    if state.get("status") != "WAITING_FOR_HUMAN":
        state["status"] = "WAITING_FOR_HUMAN"
        interrupt("Awaiting human approval")
    return state