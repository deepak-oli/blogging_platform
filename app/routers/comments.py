from fastapi import APIRouter, Depends, HTTPException

from app.services.auth import Auth
from app.services.posts import get_post
from app.services import comments
from app.schemas.comments import CommentBase, Comment

router = APIRouter(dependencies=[Depends(Auth())])

@router.post("/comments/{post_id}", tags=["comments"], response_model=Comment)
def create_comment(post_id: int, comment: CommentBase, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']

    db_post = get_post(post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return comments.create_comment(post_id, comment, user_id)

@router.get("/comments/{post_id}", tags=["comments"], response_model=list[Comment])
def read_comments(post_id: int):
    db_post = get_post(post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    return comments.get_post_comments(post_id)

@router.get("/get-comment/{comment_id}", tags=["comments"], response_model=Comment)
def read_comment(comment_id: int):
    db_comment = comments.get_comment_by_id(comment_id)

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment

@router.delete("/comments/{comment_id}", tags=["comments"], response_model=Comment)
def delete_comment(comment_id: int, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_comment = comments.get_comment_by_id(comment_id)

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return comments.delete_comment(comment_id)

@router.put("/comments/{comment_id}", tags=["comments"], response_model=Comment)
def update_comment(comment_id: int, comment: CommentBase, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_comment = comments.get_comment_by_id(comment_id)

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return comments.update_comment(comment_id, comment)
