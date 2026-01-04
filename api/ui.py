from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from state_store import list_states, load_state

router = APIRouter()
templates = Jinja2Templates(directory="ui/templates")


@router.get("/ui/incidents")
def list_incidents(request: Request):
    incidents = list_states()
    return templates.TemplateResponse(
        "incidents.html",
        {"request": request, "incidents": incidents},
    )


@router.get("/ui/incidents/{incident_id}")
def incident_detail(request: Request, incident_id: str):
    state = load_state(incident_id)
    return templates.TemplateResponse(
        "incident_detail.html",
        {"request": request, "state": state},
    )
