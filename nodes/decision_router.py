#nodes/decision_router.py
from state import IncidentState

def decision_router(state):
    if state.get("status") != "WAITING_FOR_HUMAN":
        return "evidence_collector"

    human = state.get("human_decision", {})
    decision = human.get("decision")

    if decision == "approve":
        return "final_report"

    if decision == "reject":
        return "evidence_collector"

    return "__end__"
