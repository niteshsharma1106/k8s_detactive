from fastapi import APIRouter
from state_store import list_states

router = APIRouter()

@router.get("/incidents")
def list_incidents(status: str | None = None):
    incidents = list_states()
    if status:
        incidents = [i for i in incidents if i["status"] == status]
    return incidents
