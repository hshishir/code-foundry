from pathlib import Path

from sqlalchemy.orm import Session

from agents.fake_coder import FakeCoder
from agents.fake_designer import FakeDesigner
from agents.fake_reviewer import FakeReviewer
from app.core.enums import FeatureStatus, SessionPersona, SessionStatus
from app.schemas.features import FeatureCreate
from app.services import features as feature_service
from app.services import sessions as session_service
from workspace.paths import implementation_path, review_path, story_path


def create_feature(db: Session, title: str = "Workflow idea"):
    return feature_service.create_feature(
        db,
        FeatureCreate(title=title, description="A deterministic test feature."),
    )


def test_fake_designer_creates_spec_and_marks_feature_spec_ready(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session)

    result = FakeDesigner().run(db_session, feature, tmp_path)

    db_session.refresh(feature)
    spec = story_path(feature.id, tmp_path)
    assert result.artifact_path == spec
    assert spec.exists()
    assert f"Feature ID: {feature.id}" in spec.read_text(encoding="utf-8")
    assert feature.status == FeatureStatus.SPEC_READY


def test_fake_coder_creates_implementation_artifact_and_marks_implemented(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session)
    feature_service.update_feature_status(
        db_session,
        feature,
        FeatureStatus.SPEC_READY,
    )
    story_path(feature.id, tmp_path).parent.mkdir(parents=True, exist_ok=True)
    story_path(feature.id, tmp_path).write_text("Spec content", encoding="utf-8")

    result = FakeCoder().run(db_session, feature, tmp_path)

    db_session.refresh(feature)
    artifact = implementation_path(feature.id, tmp_path)
    assert result.artifact_path == artifact
    assert artifact.exists()
    assert f"Spec Reference" in artifact.read_text(encoding="utf-8")
    assert feature.status == FeatureStatus.IMPLEMENTED


def test_fake_reviewer_creates_review_artifact_and_marks_reviewed(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session)
    feature_service.update_feature_status(
        db_session,
        feature,
        FeatureStatus.IMPLEMENTED,
    )
    implementation_path(feature.id, tmp_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    implementation_path(feature.id, tmp_path).write_text(
        "Implementation content",
        encoding="utf-8",
    )

    result = FakeReviewer().run(db_session, feature, tmp_path)

    db_session.refresh(feature)
    review = review_path(feature.id, tmp_path)
    assert result.artifact_path == review
    assert review.exists()
    content = review.read_text(encoding="utf-8")
    assert "Decision: approved" in content
    assert feature.status == FeatureStatus.REVIEWED


def test_session_records_are_created_for_each_fake_agent(
    db_session: Session,
    tmp_path: Path,
) -> None:
    feature = create_feature(db_session)

    FakeDesigner().run(db_session, feature, tmp_path)
    FakeCoder().run(db_session, feature, tmp_path)
    FakeReviewer().run(db_session, feature, tmp_path)

    sessions = session_service.list_sessions(db_session)
    assert [session.persona for session in sessions] == [
        SessionPersona.DESIGNER,
        SessionPersona.CODER,
        SessionPersona.REVIEWER,
    ]
    assert all(session.status == SessionStatus.COMPLETED for session in sessions)
    assert all(session.notes for session in sessions)

