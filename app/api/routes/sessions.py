from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.sessions import SessionCreate, SessionRead, SessionStatusUpdate
from app.services import features as feature_service
from app.services import sessions as session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    db: Session = Depends(get_db),
):
    if payload.feature_id is not None:
        feature = feature_service.get_feature(db, payload.feature_id)
        if feature is None:
            raise HTTPException(status_code=404, detail="Feature not found")
    return session_service.create_session(db, payload)


@router.get("", response_model=list[SessionRead])
def list_sessions(db: Session = Depends(get_db)):
    return session_service.list_sessions(db)


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = session_service.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.patch("/{session_id}/status", response_model=SessionRead)
def update_session_status(
    session_id: int,
    payload: SessionStatusUpdate,
    db: Session = Depends(get_db),
):
    session = session_service.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_service.update_session_status(db, session, payload.status)

