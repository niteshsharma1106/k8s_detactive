#state_store.py
import json
import os
from typing import List, Dict

STATE_DIR = os.getenv("STATE_DIR", "./state")

os.makedirs(STATE_DIR, exist_ok=True)


def _state_path(incident_id: str) -> str:
    return os.path.join(STATE_DIR, f"{incident_id}.json")


def save_state(state: dict):
    incident_id = state["incident_id"]
    with open(_state_path(incident_id), "w") as f:
        json.dump(state, f, indent=2)


def load_state(incident_id: str) -> dict | None:
    path = _state_path(incident_id)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def list_states() -> List[Dict]:
    """
    Return lightweight summaries of all incidents.
    Used by UI / dashboards.
    """
    incidents = []

    for fname in os.listdir(STATE_DIR):
        if not fname.endswith(".json"):
            continue

        with open(os.path.join(STATE_DIR, fname)) as f:
            state = json.load(f)

            incidents.append({
                "incident_id": state["incident_id"],
                "status": state.get("status"),
                "cluster": state.get("cluster"),
                "namespace": state.get("namespace"),
                "object": state.get("object"),
                "reason": state.get("event", {}).get("reason"),
                "timestamp": state.get("timestamp"),
            })

    return incidents
