from enum import StrEnum


class FeatureStatus(StrEnum):
    IDEA = "idea"
    SPEC_READY = "spec_ready"
    IMPLEMENTING = "implementing"
    IMPLEMENTED = "implemented"
    REVIEWED = "reviewed"
    BLOCKED = "blocked"


class SessionPersona(StrEnum):
    DESIGNER = "designer"
    CODER = "coder"
    REVIEWER = "reviewer"


class SessionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

