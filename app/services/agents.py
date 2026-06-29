from dataclasses import dataclass

from app.core.enums import SessionPersona, SessionStatus
from app.db.models import SessionRecord


@dataclass(frozen=True)
class ImplementedAgent:
    persona: SessionPersona
    label: str
    responsibility: str
    artifact: str
    running_sessions: int


AGENT_DETAILS = {
    SessionPersona.DESIGNER: {
        "label": "Fake Designer",
        "responsibility": "Turns ideas into deterministic specs.",
        "artifact": "docs/story_<feature_id>.md",
    },
    SessionPersona.CODER: {
        "label": "Fake Coder",
        "responsibility": "Turns ready specs into implementation artifacts.",
        "artifact": "artifacts/implementation_<feature_id>.md",
    },
    SessionPersona.REVIEWER: {
        "label": "Fake Reviewer",
        "responsibility": "Reviews implementation artifacts and records approval notes.",
        "artifact": "artifacts/review_<feature_id>.md",
    },
}


def list_implemented_agents(sessions: list[SessionRecord]) -> list[ImplementedAgent]:
    running_counts = {persona: 0 for persona in SessionPersona}
    for session in sessions:
        if session.status == SessionStatus.RUNNING:
            running_counts[session.persona] += 1

    return [
        ImplementedAgent(
            persona=persona,
            label=details["label"],
            responsibility=details["responsibility"],
            artifact=details["artifact"],
            running_sessions=running_counts[persona],
        )
        for persona, details in AGENT_DETAILS.items()
    ]
