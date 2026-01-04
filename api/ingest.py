#api/ingest.py
from fastapi import APIRouter
import uuid
from state_store import save_state
from graph import build_graph
from graph_instance import graph



router = APIRouter()


@router.post("/ingest")
def ingest_event(payload: dict):
    incident_id = str(uuid.uuid4())

    state = {
        "incident_id": incident_id,
        "cluster": payload["cluster"],
        "platform": payload["platform"],
        "namespace": payload["namespace"],
        "object_ref": payload["object"],
        "event": payload,

        "classification": None,
        "evidence": [],
        "hypotheses": [],
        "root_cause": None,
        "action_plan": [],

        "human_decision": None,
        "final_report": None,
        "status": "INVESTIGATING",
        }



    save_state(state)
    result = graph.invoke(state)
    save_state(result)

    return {"incident_id": incident_id, "status": result["status"]}
