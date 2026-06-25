from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import SessionPersona, SessionStatus


class SessionCreate(BaseModel):
    feature_id: int | None = None
    persona: SessionPersona
    notes: str | None = None


class SessionStatusUpdate(BaseModel):
    status: SessionStatus


class SessionRead(BaseModel):
    id: int
    feature_id: int | None
    persona: SessionPersona
    status: SessionStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

