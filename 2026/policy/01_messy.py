from domain import Request, User


def process_request(user: User, request: Request) -> Request:
    if not user.is_active:
        raise PermissionError("Inactive users cannot make requests")

    if request.action == "delete" and not user.has_mfa:
        raise PermissionError("MFA is required for delete actions")

    if request.required_role and request.required_role not in user.roles:
        raise PermissionError(f"Missing required role: {request.required_role}")

    if request.requires_audit:
        request.audit_log.append(
            f"{user.name} performed {request.action} on {request.path}"
        )

    request.access_granted = True
    return request


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

    result = process_request(user, request)
    print(result)


if __name__ == "__main__":
    main()
