from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.users import LoginResponse, UserCreate, User, Login

from app.services import auth, users


router = APIRouter()


@router.post("/login/", tags=["auth"], response_model=LoginResponse)
def login(request: Login, db:Session=Depends(get_db)):
    return auth.login(db, request)


@router.post("/register/", tags=["auth"], response_model=User)
def create_user(user: UserCreate, db:Session=Depends(get_db)):
    db_user = users.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    return users.create_user(db, user)
