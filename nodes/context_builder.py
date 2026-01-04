#nodes/context_builder.py
from state import IncidentState


def context_builder(state: IncidentState) -> IncidentState:
    """
    Deterministic context enrichment.
    No reasoning. No LLM.
    """

    context = state.get("context", {})

    context.update({
        "cluster": state["cluster"],
        "platform": state["platform"],
        "namespace": state["namespace"],
        "object": {
            "kind": state["object_ref"].get("kind"),
            "name": state["object_ref"].get("name"),
        },
        "investigation_stage": "context_built"
    })

    state["context"] = context
    return state
