from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import SessionStatus
from app.db.models import SessionRecord
from app.schemas.sessions import SessionCreate


def create_session(db: Session, payload: SessionCreate) -> SessionRecord:
    session = SessionRecord(
        feature_id=payload.feature_id,
        persona=payload.persona,
        status=SessionStatus.PENDING,
        notes=payload.notes,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def list_sessions(db: Session) -> list[SessionRecord]:
    return list(
        db.scalars(
            select(SessionRecord)
            .options(selectinload(SessionRecord.feature))
            .order_by(SessionRecord.id)
        )
    )


def get_session(db: Session, session_id: int) -> SessionRecord | None:
    return db.get(SessionRecord, session_id)


def update_session_status(
    db: Session,
    session: SessionRecord,
    status: SessionStatus,
) -> SessionRecord:
    session.status = status
    db.add(session)
    db.commit()
    db.refresh(session)
    return session
