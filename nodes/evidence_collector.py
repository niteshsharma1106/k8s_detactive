from state import IncidentState


def evidence_collector(state: IncidentState, tools) -> IncidentState:
    """
    Evidence collection node.
    Uses tools only (stubbed here).
    No LLM, no reasoning.
    """

    evidence = state.get("evidence", [])

    # Placeholder entries – replaced later by MCP tools
    evidence.append({
        "source": "kubernetes_api",
        "type": "pod_metadata",
        "status": "PENDING",
        "details": "Pod metadata will be fetched via MCP tool"
    })

    evidence.append({
        "source": "kubernetes_api",
        "type": "events",
        "status": "PENDING",
        "details": "Related events will be fetched via MCP tool"
    })

    state["evidence"] = evidence
    return state
