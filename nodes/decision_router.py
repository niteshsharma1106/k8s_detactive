#nodes/decision_router.py
from state import IncidentState

def decision_router(state):
    human = state.get("human_decision")

    # If no decision object exists, or if the internal decision is empty, STOP.
    if not human or not human.get("decision"):
        return "__end__"  # This stops the recursion

    decision = human.get("decision")

    if decision == "approve":
        return "final_report"

    if decision == "reject":
        return "evidence_collector"

    return "__end__"
