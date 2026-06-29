from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.enums import SessionPersona, SessionStatus
from app.db.models import Feature, SessionRecord
from app.schemas.sessions import SessionCreate
from app.services import sessions as session_service


@dataclass(frozen=True)
class AgentResult:
    persona: SessionPersona
    feature_id: int
    artifact_path: Path
    summary: str


class FakeAgent:
    persona: SessionPersona

    def create_running_session(self, db: Session, feature: Feature) -> SessionRecord:
        session = session_service.create_session(
            db,
            SessionCreate(feature_id=feature.id, persona=self.persona),
        )
        return session_service.update_session_status(
            db,
            session,
            SessionStatus.RUNNING,
        )

    def complete_session(
        self,
        db: Session,
        session: SessionRecord,
        notes: str,
    ) -> SessionRecord:
        session.notes = notes
        session_service.update_session_status(db, session, SessionStatus.COMPLETED)
        db.refresh(session)
        return session

