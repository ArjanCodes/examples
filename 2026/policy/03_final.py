from dataclasses import replace
from functools import reduce
from typing import Callable

from domain import Request, User
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Policy = Callable[[User, Request], Request]


class Settings(BaseSettings):
    enabled_policies: list[str] = Field(
        default_factory=lambda: [
            "active_user",
            "role_required",
            "mfa_required",
            "grant_access",
        ]
    )

    model_config = SettingsConfigDict(
        env_file="settings.env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
    )


def active_user(user: User, request: Request) -> Request:
    if not user.is_active:
        raise PermissionError("Inactive users cannot make requests")
    return request


def mfa_required(user: User, request: Request) -> Request:
    if request.action == "delete" and not user.has_mfa:
        raise PermissionError("MFA is required for delete actions")
    return request


def role_required(user: User, request: Request) -> Request:
    if request.required_role and request.required_role not in user.roles:
        raise PermissionError(f"Missing required role: {request.required_role}")
    return request


def grant_access(user: User, request: Request) -> Request:
    return replace(request, access_granted=True)


def audit(user: User, request: Request) -> Request:
    if not request.requires_audit:
        return request

    return replace(
        request,
        audit_log=request.audit_log
        + [f"{user.name} performed {request.action} on {request.path}"],
    )


POLICY_REGISTRY: dict[str, Policy] = {
    "active_user": active_user,
    "mfa_required": mfa_required,
    "role_required": role_required,
    "grant_access": grant_access,
    "audit": audit,
}


def get_policies(settings: Settings) -> list[Policy]:
    try:
        return [POLICY_REGISTRY[name] for name in settings.enabled_policies]
    except KeyError as exc:
        valid = ", ".join(sorted(POLICY_REGISTRY))
        raise ValueError(
            f"Unknown policy name: {exc.args[0]!r}. Valid names: {valid}"
        ) from exc


def apply_policies(user: User, request: Request, policies: list[Policy]) -> Request:
    return reduce(lambda current, policy: policy(user, current), policies, request)


def main() -> None:
    settings = Settings()

    user = User(
        name="Arjan",
        is_active=True,
        roles={"admin"},
        has_mfa=True,
        subscription_tier="pro",
    )

    request = Request(
        path="/admin/users",
        action="delete",
        requires_audit=True,
        required_role="admin",
    )

    policies = get_policies(settings)
    result = apply_policies(user, request, policies)

    print("Enabled policies:", settings.enabled_policies)
    print(result)


if __name__ == "__main__":
    main()
