from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import FeatureStatus, SessionPersona, SessionStatus
from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def enum_values(enum_class: type) -> list[str]:
    return [member.value for member in enum_class]


class Feature(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[FeatureStatus] = mapped_column(
        Enum(FeatureStatus, native_enum=False, values_callable=enum_values),
        default=FeatureStatus.IDEA,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    sessions: Mapped[list["SessionRecord"]] = relationship(
        back_populates="feature",
        cascade="all, delete-orphan",
    )


class SessionRecord(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    feature_id: Mapped[int | None] = mapped_column(
        ForeignKey("features.id"),
        nullable=True,
    )
    persona: Mapped[SessionPersona] = mapped_column(
        Enum(SessionPersona, native_enum=False, values_callable=enum_values),
        nullable=False,
    )
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, native_enum=False, values_callable=enum_values),
        default=SessionStatus.PENDING,
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    feature: Mapped[Feature | None] = relationship(back_populates="sessions")
