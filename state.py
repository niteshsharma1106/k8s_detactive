#state.py
from typing import TypedDict, List, Optional, Dict, Any


class Hypothesis(TypedDict):
    hypothesis: str
    confidence: float
    status: Optional[str]  # VALID / INVALID / UNKNOWN
    evidence: List[str]


class ActionStep(TypedDict):
    description: str
    command: str
    risk: str


class IncidentState(TypedDict):
    # Identity
    incident_id: str
    cluster: str
    platform: str  # kubernetes | openshift
    namespace: str
    object_ref: Dict[str, str]

    # Incoming signal
    event: Dict[str, Any]

    # Investigation artifacts
    context: Dict[str, Any]
    evidence: List[Dict[str, Any]]
    hypotheses: List[Hypothesis]
    root_cause: Optional[Dict[str, Any]]
    action_plan: List[ActionStep]
    final_report: Optional[dict]

    # Control
    human_decision: Optional[str]  # APPROVED / REJECTED / MORE_DATA
    status: str  # INVESTIGATING / WAITING_FOR_HUMAN / CLOSED
