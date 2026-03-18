from typing import Protocol

from domain import Request, User


class RequestPolicy(Protocol):
    def apply(self, user: User, request: Request) -> None: ...


class ActiveUserPolicy:
    def apply(self, user: User, request: Request) -> None:
        if not user.is_active:
            raise PermissionError("Inactive users cannot make requests")


class MfaRequiredPolicy:
    def apply(self, user: User, request: Request) -> None:
        if request.action == "delete" and not user.has_mfa:
            raise PermissionError("MFA is required for delete actions")


class RoleRequiredPolicy:
    def apply(self, user: User, request: Request) -> None:
        if request.required_role and request.required_role not in user.roles:
            raise PermissionError(f"Missing required role: {request.required_role}")


class AuditPolicy:
    def apply(self, user: User, request: Request) -> None:
        if request.requires_audit:
            request.audit_log.append(
                f"{user.name} performed {request.action} on {request.path}"
            )


class GrantAccessPolicy:
    def apply(self, user: User, request: Request) -> None:
        request.access_granted = True


class CompositePolicy:
    def __init__(self, policies: list[RequestPolicy]) -> None:
        self.policies = policies

    def apply(self, user: User, request: Request) -> None:
        for policy in self.policies:
            policy.apply(user, request)


def main() -> None:
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

    policy = CompositePolicy(
        [
            ActiveUserPolicy(),
            MfaRequiredPolicy(),
            RoleRequiredPolicy(),
            AuditPolicy(),
            GrantAccessPolicy(),
        ]
    )

    policy.apply(user, request)
    print(request)


if __name__ == "__main__":
    main()
