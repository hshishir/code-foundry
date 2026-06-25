from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.features import FeatureCreate, FeatureRead, FeatureStatusUpdate
from app.services import features as feature_service

router = APIRouter(prefix="/features", tags=["features"])


@router.post("", response_model=FeatureRead, status_code=status.HTTP_201_CREATED)
def create_feature(
    payload: FeatureCreate,
    db: Session = Depends(get_db),
):
    return feature_service.create_feature(db, payload)


@router.get("", response_model=list[FeatureRead])
def list_features(db: Session = Depends(get_db)):
    return feature_service.list_features(db)


@router.get("/{feature_id}", response_model=FeatureRead)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = feature_service.get_feature(db, feature_id)
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@router.patch("/{feature_id}/status", response_model=FeatureRead)
def update_feature_status(
    feature_id: int,
    payload: FeatureStatusUpdate,
    db: Session = Depends(get_db),
):
    feature = feature_service.get_feature(db, feature_id)
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature_service.update_feature_status(db, feature, payload.status)

