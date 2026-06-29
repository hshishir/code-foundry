from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from agents.base import AgentResult
from agents.fake_coder import FakeCoder
from agents.fake_designer import FakeDesigner
from agents.fake_reviewer import FakeReviewer
from app.core.enums import FeatureStatus, SessionPersona
from app.db.models import Feature
from app.services import features as feature_service


@dataclass(frozen=True)
class WorkflowAction:
    persona: SessionPersona
    target_status: FeatureStatus


@dataclass(frozen=True)
class WorkflowResult:
    advanced: bool
    message: str
    feature_id: int | None = None
    persona: SessionPersona | None = None
    artifact_path: Path | None = None


ELIGIBLE_STATUSES = {
    FeatureStatus.IDEA,
    FeatureStatus.SPEC_READY,
    FeatureStatus.IMPLEMENTED,
}


def next_action_for_feature(feature: Feature) -> WorkflowAction | None:
    if feature.status == FeatureStatus.IDEA:
        return WorkflowAction(SessionPersona.DESIGNER, FeatureStatus.SPEC_READY)
    if feature.status == FeatureStatus.SPEC_READY:
        return WorkflowAction(SessionPersona.CODER, FeatureStatus.IMPLEMENTED)
    if feature.status == FeatureStatus.IMPLEMENTED:
        return WorkflowAction(SessionPersona.REVIEWER, FeatureStatus.REVIEWED)
    return None


def oldest_eligible_feature(db: Session) -> Feature | None:
    for feature in feature_service.list_features(db):
        if feature.status in ELIGIBLE_STATUSES:
            return feature
    return None


def advance_feature(
    db: Session,
    feature: Feature,
    workspace_root: Path | str | None = None,
) -> WorkflowResult:
    action = next_action_for_feature(feature)
    if action is None:
        return WorkflowResult(
            advanced=False,
            feature_id=feature.id,
            message=(
                f"Feature {feature.id} is {feature.status.value}; "
                "no eligible workflow action."
            ),
        )

    result = run_agent_for_action(db, feature, action, workspace_root)
    return WorkflowResult(
        advanced=True,
        message=f"{result.summary}; wrote {result.artifact_path}",
        feature_id=feature.id,
        persona=result.persona,
        artifact_path=result.artifact_path,
    )


def run_agent_for_action(
    db: Session,
    feature: Feature,
    action: WorkflowAction,
    workspace_root: Path | str | None = None,
) -> AgentResult:
    if action.persona == SessionPersona.DESIGNER:
        return FakeDesigner().run(db, feature, workspace_root)
    if action.persona == SessionPersona.CODER:
        return FakeCoder().run(db, feature, workspace_root)
    if action.persona == SessionPersona.REVIEWER:
        return FakeReviewer().run(db, feature, workspace_root)
    raise ValueError(f"Unsupported persona: {action.persona}")


def run_once(
    db: Session,
    workspace_root: Path | str | None = None,
) -> WorkflowResult:
    feature = oldest_eligible_feature(db)
    if feature is None:
        return WorkflowResult(
            advanced=False,
            message="No eligible features to advance.",
        )
    return advance_feature(db, feature, workspace_root)


def run_feature(
    db: Session,
    feature_id: int,
    workspace_root: Path | str | None = None,
) -> WorkflowResult:
    feature = feature_service.get_feature(db, feature_id)
    if feature is None:
        return WorkflowResult(
            advanced=False,
            feature_id=feature_id,
            message=f"Feature {feature_id} was not found.",
        )
    return advance_feature(db, feature, workspace_root)

