#ui/api_client.py
import requests

API_URL = "http://127.0.0.1:8000"

def get_incidents(status=None):
    params = {"status": status} if status else {}
    return requests.get(f"{API_URL}/incidents", params=params).json()

def approve_incident(incident_id, decision, comment=""):
    return requests.post(
        f"{API_URL}/approve",
        json={
            "incident_id": incident_id,
            "decision": decision,
            "comment": comment,
        },
    ).json()
