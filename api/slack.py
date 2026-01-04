# agent_platform/api/slack.py

import json
from fastapi import APIRouter, Request, HTTPException
from state_store import load_state, save_state
from graph_instance import graph

router = APIRouter()


@router.post("/slack/interact")
async def slack_interact(request: Request):
    form = await request.form()
    payload = json.loads(form["payload"])

    action = payload["actions"][0]
    action_value = action["value"]

    decision, incident_id = action_value.split(":")

    state = load_state(incident_id)
    if not state or state["status"] != "WAITING_FOR_HUMAN":
        return {"text": "Incident already processed."}

    state["human_decision"] = {
        "decision": decision,
        "comment": f"Approved via Slack by {payload['user']['username']}"
    }
    state["status"] = "RUNNING"

    save_state(state)

    result = graph.invoke(state)
    save_state(result)

    return {
        "text": f"Incident *{incident_id}* {decision.upper()}D"
    }
