from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import FeatureStatus
from app.db.models import Feature
from app.schemas.features import FeatureCreate


def create_feature(db: Session, payload: FeatureCreate) -> Feature:
    feature = Feature(
        title=payload.title,
        description=payload.description,
        status=FeatureStatus.IDEA,
    )
    db.add(feature)
    db.commit()
    db.refresh(feature)
    return feature


def list_features(db: Session) -> list[Feature]:
    return list(db.scalars(select(Feature).order_by(Feature.id)))


def get_feature(db: Session, feature_id: int) -> Feature | None:
    return db.get(Feature, feature_id)


def update_feature_status(
    db: Session,
    feature: Feature,
    status: FeatureStatus,
) -> Feature:
    feature.status = status
    db.add(feature)
    db.commit()
    db.refresh(feature)
    return feature

