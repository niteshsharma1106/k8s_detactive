#api/approval.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from state_store import load_state, save_state
from graph_instance import graph

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/approve")
def approve(payload: dict):
    incident_id = payload.get("incident_id")
    decision = payload.get("decision")
    comment = payload.get("comment", "")

    if not incident_id or not decision:
        raise HTTPException(status_code=400, detail="incident_id and decision are required")

    state = load_state(incident_id)
    if not state:
        raise HTTPException(status_code=404, detail="Incident not found")

    if state.get("status") != "WAITING_FOR_HUMAN":
        raise HTTPException(
            status_code=400,
            detail=f"Incident not awaiting approval (status={state.get('status')})"
        )

    state["human_decision"] = {
        "decision": decision,
        "comment": comment,
    }
    state["status"] = "RUNNING"

    save_state(state)

    # Resume graph
    result = graph.invoke(state)
    save_state(result)

    return {
        "incident_id": incident_id,
        "status": result.get("status"),
    }
