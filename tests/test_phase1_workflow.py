from pathlib import Path

from sqlalchemy.orm import Session

from app.core.enums import FeatureStatus, SessionPersona
from app.schemas.features import FeatureCreate
from app.services import features as feature_service
from app.services import sessions as session_service
from orchestrator import workflow
from workspace.paths import story_path


def create_feature(db: Session, title: str):
    return feature_service.create_feature(
        db,
        FeatureCreate(title=title, description=f"{title} description."),
    )


def test_run_once_advances_oldest_eligible_feature(
    db_session: Session,
    tmp_path: Path,
) -> None:
    first = create_feature(db_session, "First eligible")
    second = create_feature(db_session, "Second eligible")

    result = workflow.run_once(db_session, tmp_path)

    db_session.refresh(first)
    db_session.refresh(second)
    assert result.advanced is True
    assert result.feature_id == first.id
    assert first.status == FeatureStatus.SPEC_READY
    assert second.status == FeatureStatus.IDEA
    assert story_path(first.id, tmp_path).exists()


def test_run_feature_advances_only_requested_feature(
    db_session: Session,
    tmp_path: Path,
) -> None:
    first = create_feature(db_session, "Do not touch")
    second = create_feature(db_session, "Requested")

    result = workflow.run_feature(db_session, second.id, tmp_path)

    db_session.refresh(first)
    db_session.refresh(second)
    assert result.advanced is True
    assert result.feature_id == second.id
    assert first.status == FeatureStatus.IDEA
    assert second.status == FeatureStatus.SPEC_READY
    assert not story_path(first.id, tmp_path).exists()
    assert story_path(second.id, tmp_path).exists()


def test_reviewed_feature_is_ignored(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session, "Already reviewed")
    feature_service.update_feature_status(
        db_session,
        feature,
        FeatureStatus.REVIEWED,
    )

    result = workflow.run_feature(db_session, feature.id, tmp_path)

    db_session.refresh(feature)
    assert result.advanced is False
    assert feature.status == FeatureStatus.REVIEWED
    assert session_service.list_sessions(db_session) == []


def test_blocked_feature_is_ignored(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session, "Blocked")
    feature_service.update_feature_status(
        db_session,
        feature,
        FeatureStatus.BLOCKED,
    )

    result = workflow.run_feature(db_session, feature.id, tmp_path)

    db_session.refresh(feature)
    assert result.advanced is False
    assert feature.status == FeatureStatus.BLOCKED
    assert session_service.list_sessions(db_session) == []


def test_run_once_reports_no_work_when_only_terminal_features_exist(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session, "Blocked only")
    feature_service.update_feature_status(
        db_session,
        feature,
        FeatureStatus.BLOCKED,
    )

    result = workflow.run_once(db_session, tmp_path)

    assert result.advanced is False
    assert result.feature_id is None
    assert "No eligible features" in result.message


def test_workflow_result_records_persona(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session, "Persona check")

    result = workflow.run_feature(db_session, feature.id, tmp_path)

    assert result.persona == SessionPersona.DESIGNER

