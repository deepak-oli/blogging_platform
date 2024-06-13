
from fastapi import APIRouter, HTTPException, status

from app.schemas.users import Token, UserCreate, User, Login
from app.services import auth, users


router = APIRouter()


@router.post("/login/", tags=["auth"], response_model=Token)
def login(request: Login):
    return auth.login(request)


@router.post("/register/", tags=["auth"], response_model=User)
def create_user(user: UserCreate):
    db_user = users.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    return users.create_user(user)
