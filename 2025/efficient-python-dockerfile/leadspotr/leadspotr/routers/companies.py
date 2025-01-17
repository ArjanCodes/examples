from urllib.parse import quote

from fastapi import Body, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..config import settings
from ..db import database
from ..db.crud.company import get_company_by_user_id, update_company
from ..db.crud.submission import get_all_submissions_this_month_count
from ..db.crud.user import create_user, get_user_by_email, get_users_by_company_id
from ..db.models import RoleEnum
from ..db.schemas.company import Company, CompanyUpdate
from ..db.schemas.image import Crop
from ..db.schemas.user import User, UserCreate, UserInviteInput
from ..dependencies.authentication import get_current_user
from ..dependencies.authorization import PermissionChecker, PermissionEnum
from ..email import email_client
from ..utils.file import delete_uploaded_file, upload_file
from ..utils.image import crop_image
from ..utils.string import random_string
from .router import APIRouter

router = APIRouter()

router.prefix = "/companies"


@router.get("/", response_model=Company)
def get_company_by_user(
    db: Session = Depends(database.get_db),
    current_user: User | None = Depends(get_current_user),
) -> Company | None:
    if current_user is None:
        return None

    db_company = get_company_by_user_id(db, user_id=current_user.id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    submissions_this_month_count = get_all_submissions_this_month_count(
        db=db, user_id=current_user.id
    )
    db_company.submissions_cap = (
        db_company.submissions_cap - submissions_this_month_count
    )

    if db_company.submissions_cap < 0:
        db_company.submissions_cap = 0

    return db_company


@router.get(
    "/users",
    response_model=list[User],
)
def get_users_by_company(
    db: Session = Depends(database.get_db),
    current_user: User | None = Depends(get_current_user),
) -> list[User] | None:
    if current_user is None:
        return None

    db_company = get_company_by_user_id(db, user_id=current_user.id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db_users = get_users_by_company_id(db=db, company_id=db_company.id)
    return db_users


@router.put(
    "/",
    response_model=Company,
    dependencies=[
        Depends(PermissionChecker(required_permissions=[PermissionEnum.UPDATE_COMPANY]))
    ],
)
def update(
    company: CompanyUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
) -> Company:
    db_company = get_company_by_user_id(db, user_id=current_user.id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    update_company(db=db, user_id=current_user.id, company=company)

    return db_company


if settings.FEATURES["upload_file"]:

    @router.post(
        "/logo",
        response_model=Company,
        dependencies=[
            Depends(
                PermissionChecker(required_permissions=[PermissionEnum.UPDATE_COMPANY])
            )
        ],
    )
    def upload_logo(
        crop: Crop = Body(...),
        logo: UploadFile | None = File(...),
        db: Session = Depends(database.get_db),
        current_user: User = Depends(get_current_user),
    ) -> Company | None:
        if logo is None:
            raise HTTPException(status_code=400, detail="No file provided")

        db_company = get_company_by_user_id(db, user_id=current_user.id)
        if db_company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        if db_company.logo_url is not None:
            delete_uploaded_file(db_company.logo_url)
            db_company.logo_url = None

        file_data = crop_image(image=logo, crop=crop)

        content_type = logo.content_type

        if content_type is None:
            raise HTTPException(status_code=400, detail="Invalid file type")

        url = upload_file(
            file_data=file_data,
            content_type=content_type,
            folder_name="company-logos",
        )

        update_data = {"logo_url": url}
        db_company = update_company(
            db, user_id=current_user.id, company=CompanyUpdate(**update_data)
        )

        return db_company


if settings.FEATURES["upload_file"]:

    @router.delete(
        "/logo",
        dependencies=[
            Depends(
                PermissionChecker(required_permissions=[PermissionEnum.UPDATE_COMPANY])
            )
        ],
    )
    def delete_logo(
        db: Session = Depends(database.get_db),
        current_user: User = Depends(get_current_user),
    ) -> Company | None:
        db_company = get_company_by_user_id(db, user_id=current_user.id)
        if db_company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        url = db_company.logo_url

        if url is None:
            raise HTTPException(status_code=404, detail="Logo not found")

        delete_uploaded_file(url)

        # Update the logo_url of the company to None using the update_company helper
        update_data = {"logo_url": None}
        db_company = update_company(
            db, user_id=current_user.id, company=CompanyUpdate(**update_data)
        )

        return db_company


@router.post(
    "/invite",
    dependencies=[
        Depends(PermissionChecker(required_permissions=[PermissionEnum.UPDATE_COMPANY]))
    ],
)
def invite_user(
    input: UserInviteInput,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    db_company = get_company_by_user_id(db, user_id=current_user.id)

    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    email = input.email

    invited_user = get_user_by_email(db, email=email)

    if invited_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    if db_company.invite_code is None:
        invite_code = random_string(length=8)

        update_company_input = CompanyUpdate(invite_code=invite_code)
        update_company(db=db, user_id=current_user.id, company=update_company_input)

    create_invited_user = UserCreate(
        email=email, company_id=db_company.id, name="", active=False, role=RoleEnum.user
    )

    # Create user
    invited_user = create_user(db=db, user=create_invited_user)

    confirm_invite_url = f"{settings.FRONTEND_URL}/auth/accept-invite?inviteCode={db_company.invite_code}&email={quote(email)}"

    data = {
        "name": current_user.name,
        "organizationName": db_company.name,
        "confirmInviteUrl": confirm_invite_url,
    }

    try:
        email_client.send_mail(
            recipients=[email],
            subject=f"Invite to join {db_company.name} on Leadspotr",
            data=data,
            template_id=settings.SENDGRID_INVITE_TEMPLATE_ID,
        )
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {"message": "Invite sent to user", "status": 200}
