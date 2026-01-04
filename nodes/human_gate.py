#nodes/human_gate.py
from state import IncidentState
from langgraph.types import interrupt

def human_gate(state):
    """
    Human-in-the-loop checkpoint.
    First pass pauses execution.
    After approval/reject, just pass through.
    """
    if state.get("status") == "WAITING_FOR_HUMAN":
        return state

    # After human decision, DO NOT modify state here
    return state
