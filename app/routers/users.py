from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.users import User

from app.services.auth import Auth
from app.services import users

from app.utils.password_hash import verify_password

router = APIRouter()


@router.get("/users/", tags=["users"], response_model=list[User])
def read_users(db:Session = Depends(get_db), dependencies=Depends(Auth())):
    db_users = users.get_users(db)
    return db_users


@router.get("/users/{user_id}", tags=["users"], response_model=User)
def read_user(user_id: int, db:Session = Depends(get_db), dependencies=Depends(Auth())):
    db_user = users.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user


# @router.put("/users/{user_id}", tags=["users"], response_model=User)
# def update_user(user_id: int, user: UserCreate, dependencies=Depends(Auth())):
#     if dependencies['user_id'] != user_id:
#         raise HTTPException(status_code=403, detail="Forbidden.")
#     db_user = users.get_user(user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found.")
#     return users.update_user(user_id, user)

@router.post("/change-password/", tags=["users"], response_model=User)
def update_password(current_password: str, new_password: str, db:Session = Depends(get_db),  dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_user = users.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    if not verify_password(current_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    return users.update_password(db, user_id, new_password)


@router.delete("/users/{user_id}", tags=["users"], response_model=User)
def delete_user(user_id: int, db:Session = Depends(get_db), dependencies=Depends(Auth())):
    if dependencies['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden.")
    db_user = users.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return users.delete_user(db, user_id)
