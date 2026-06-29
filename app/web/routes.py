from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.enums import FeatureStatus
from app.db.database import get_db
from app.schemas.features import FeatureCreate
from app.schemas.sessions import SessionRead
from app.services import agents as agent_service
from app.services import features as feature_service
from app.services import sessions as session_service

templates = Jinja2Templates(directory="app/web/templates")

router = APIRouter(tags=["web"])


def wants_html(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "text/html" in accept


def feature_counts(features: list) -> dict[str, int]:
    counts = {status.value: 0 for status in FeatureStatus}
    for feature in features:
        counts[feature.status.value] += 1
    return counts


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    features = feature_service.list_features(db)
    sessions = session_service.list_sessions(db)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "features": features,
            "implemented_agents": agent_service.list_implemented_agents(sessions),
            "counts": feature_counts(features),
            "total_features": len(features),
            "feature_statuses": list(FeatureStatus),
        },
    )


@router.post("/features/create")
def create_feature_from_form(
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):
    feature_service.create_feature(
        db,
        FeatureCreate(title=title.strip(), description=description.strip()),
    )
    return RedirectResponse(
        url="/?toast=feature-created",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/features/{feature_id}/view", response_class=HTMLResponse)
def feature_detail(
    feature_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    feature = feature_service.get_feature(db, feature_id)
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    related_sessions = [
        session
        for session in session_service.list_sessions(db)
        if session.feature_id == feature.id
    ]
    return templates.TemplateResponse(
        request,
        "feature_detail.html",
        {
            "feature": feature,
            "sessions": related_sessions,
            "feature_statuses": list(FeatureStatus),
        },
    )


@router.post("/features/{feature_id}/status")
def update_feature_status_from_form(
    feature_id: int,
    status_value: FeatureStatus = Form(..., alias="status"),
    db: Session = Depends(get_db),
):
    feature = feature_service.get_feature(db, feature_id)
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    feature_service.update_feature_status(db, feature, status_value)
    return RedirectResponse(
        url=f"/features/{feature_id}/view?toast=status-updated",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/sessions")
def sessions_page(request: Request, db: Session = Depends(get_db)):
    sessions = session_service.list_sessions(db)
    if not wants_html(request):
        payload = [
            SessionRead.model_validate(session).model_dump(mode="json")
            for session in sessions
        ]
        return JSONResponse(content=payload)
    return templates.TemplateResponse(
        request,
        "sessions.html",
        {"sessions": sessions},
    )
