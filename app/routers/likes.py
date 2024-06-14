from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.services.auth import Auth
from app.services.posts import get_post
from app.services import likes

from app.schemas.likes import LikeResponse, UserLike

router = APIRouter(dependencies=[Depends(Auth())])

@router.post("/like/{post_id}", tags=["likes"], response_model=LikeResponse)
def create_like(post_id: int, db:Session = Depends(get_db), dependencies=Depends(Auth())):
    user_id = dependencies['user_id']

    db_post = get_post(db, post_id)

    if not db_post:
        raise HTTPException(db, status_code=404, detail="Post not found")
    
    return likes.create_like(db, post_id, user_id)

@router.delete("/unlike/{post_id}", tags=["likes"], response_model=LikeResponse)
def delete_like(post_id: int, db:Session = Depends(get_db), dependencies=Depends(Auth())):
    user_id = dependencies['user_id']

    db_post = get_post(db, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return likes.delete_like(db, post_id, user_id)

@router.get("/likes/{post_id}", tags=["likes"], response_model=LikeResponse)
def get_post_likes(post_id: int, db:Session = Depends(get_db)):
    db_post = get_post(db, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    return likes.get_post_likes(db, post_id)

@router.get("/user-likes", tags=["likes"], response_model=list[UserLike])
def get_user_likes(db:Session = Depends(get_db), dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    return likes.get_user_likes(db, user_id)
