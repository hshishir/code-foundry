from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import FeatureStatus


class FeatureCreate(BaseModel):
    title: str
    description: str


class FeatureStatusUpdate(BaseModel):
    status: FeatureStatus


class FeatureRead(BaseModel):
    id: int
    title: str
    description: str
    status: FeatureStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

