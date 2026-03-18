from dataclasses import dataclass, field


@dataclass(slots=True)
class User:
    name: str
    is_active: bool
    roles: set[str]
    has_mfa: bool
    subscription_tier: str


@dataclass(slots=True)
class Request:
    path: str
    action: str
    requires_audit: bool = False
    required_role: str | None = None
    audit_log: list[str] = field(default_factory=list[str])
    access_granted: bool = False
