# agent_platform/approval/slack_notifier.py
import os
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#incidents")


def post_incident_to_slack(state: dict):
    incident_id = state["incident_id"]

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "*🚨 Incident Detected*\n"
                    f"*Cluster:* {state['cluster']}\n"
                    f"*Namespace:* {state['namespace']}\n"
                    f"*Object:* {state['object']['kind']} `{state['object']['name']}`\n"
                    f"*Reason:* `{state['event']['reason']}`"
                )
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "*🧠 Root Cause Hypothesis*\n"
                    f"{state['root_cause']['root_cause']}\n"
                    f"_Confidence:_ {state['root_cause']['confidence']}"
                )
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*📋 Proposed Action Plan*\n"
                        + "\n".join(
                            f"• {a['description']} (`{a['risk']}`)"
                            for a in state["action_plan"]
                        )
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "style": "primary",
                    "text": {"type": "plain_text", "text": "Approve"},
                    "value": f"approve:{incident_id}",
                    "action_id": "approve_incident"
                },
                {
                    "type": "button",
                    "style": "danger",
                    "text": {"type": "plain_text", "text": "Reject"},
                    "value": f"reject:{incident_id}",
                    "action_id": "reject_incident"
                }
            ]
        }
    ]

    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": SLACK_CHANNEL,
            "blocks": blocks,
            "text": f"Incident {incident_id} awaiting approval"
        }
    )

    resp.raise_for_status()
    return resp.json()
