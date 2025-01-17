from enum import Enum

from fastapi import Depends, HTTPException

from ..db.models import RoleEnum
from ..db.schemas.user import User
from .authentication import get_current_user


class PermissionEnum(str, Enum):
    # Common permissions
    READ_COMPANY = "read_company"

    # Admin permissions
    UPDATE_COMPANY = "update_company"
    INVITE_USER = "invite_user"
    DELETE_USER = "delete_user"


role_permissions = {
    RoleEnum.admin: [
        PermissionEnum.INVITE_USER,
        PermissionEnum.DELETE_USER,
        PermissionEnum.UPDATE_COMPANY,
    ],
    RoleEnum.user: [PermissionEnum.READ_COMPANY],
}


def get_permissions_by_role(role: RoleEnum) -> list[PermissionEnum]:
    return role_permissions.get(role, [])


class PermissionChecker:
    def __init__(self, required_permissions: list[PermissionEnum]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, current_user: User | None = Depends(get_current_user)) -> bool:
        if current_user is None:
            raise HTTPException(status_code=403, detail="Not authenticated")

        permissions = get_permissions_by_role(current_user.role)
        for permission in self.required_permissions:
            if permission not in permissions:
                raise HTTPException(status_code=403, detail="Not authorized")

        return True
