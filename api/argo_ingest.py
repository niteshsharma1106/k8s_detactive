from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.ingest import ingest_event
import logging
import json

argo_logger = logging.getLogger(__name__)
argo_logger.setLevel(logging.INFO)

router = APIRouter()

def normalize_argo_event(payload: dict) -> dict:
    event = payload.get("event", {})
    if not event:
        raise ValueError("Missing 'event' field in Argo payload")

    involved = event.get("involvedObject", {})
    if not involved:
        raise ValueError("Missing 'involvedObject' in Argo event")

    # ALIGN WITH api/ingest.py: Use 'object' key because ingest.py 
    # maps payload["object"] to state["object_ref"]
    return {
        "cluster": payload.get("cluster", "acmclus01"),
        "platform": "openshift",
        "namespace": event.get("namespace"),
        "object": { # Matches payload["object"] in ingest.py
            "kind": involved.get("kind"),
            "name": involved.get("name"),
        },
        "reason": event.get("reason", "Unknown"),
        "message": event.get("message", ""),
        "source": "argo-events",
        "raw_payload": payload # Store the raw data for debugging
    }

@router.post("/ingest/argo", status_code=202)
def ingest_argo_event(payload: dict, background_tasks: BackgroundTasks):
    # Log to terminal
    print("\n--- DEBUG: ARGO PAYLOAD RECEIVED ---")
    print(json.dumps(payload, indent=2))
    print("------------------------------------\n")

    try:
        normalized = normalize_argo_event(payload)
        # Check for key consistency
        background_tasks.add_task(ingest_event, normalized)
        return {"status": "accepted", "incident_id": "pending"}
    except Exception as e:
        print(f"Error in argo_ingest: {e}")
        raise HTTPException(status_code=400, detail=str(e))