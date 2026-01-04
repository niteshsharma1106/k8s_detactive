#nodes/final_report.py
from datetime import datetime
from state import IncidentState


def final_report(state: IncidentState) -> IncidentState:
    """
    Finalizes the investigation and produces a human-readable,
    auditable incident report.
    """

    report = {
        "incident_id": state["incident_id"],
        "timestamp": datetime.utcnow().isoformat() + "Z",

        "cluster": state["cluster"],
        "platform": state["platform"],
        "namespace": state["namespace"],
        "object": state["object_ref"],

        "event": state["event"],

        "classification": state["context"].get("classification"),

        "evidence_collected": [
            e.get("type") for e in state.get("evidence", [])
        ],

        "hypotheses": [
            {
                "hypothesis": h["hypothesis"],
                "status": h["status"],
                "confidence": h["confidence"],
                "evidence": h.get("evidence", [])
            }
            for h in state.get("hypotheses", [])
        ],

        "root_cause": state.get("root_cause"),

        "action_plan": state.get("action_plan"),

        "human_decision": state.get("human_decision"),

        "final_status": "RESOLVED"
        if state.get("human_decision") == "APPROVED"
        else "CLOSED_WITHOUT_ACTION",
    }
    state["slack_status"] = "closed"
    state["final_report"] = report
    state["status"] = "CLOSED"

    return state
