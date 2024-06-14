from sqlalchemy.orm import Session

from app.models.comments import Comment

from app.schemas.comments import CommentBase


def create_comment(db:Session, post_id: int, comment: CommentBase, user_id: int):
    comment = Comment(**comment.model_dump(), user_id=user_id, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_post_comments(db:Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def get_comment_by_id(db:Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def delete_comment(db:Session, comment_id: int):
    comment = get_comment_by_id(comment_id)
    db.delete(comment)
    db.commit()
    return comment

def update_comment(db:Session, comment_id: int, comment: CommentBase):
    db_comment = get_comment_by_id(comment_id)
    for key, value in vars(comment).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment_user_id(db:Session, user_id:int):
    return db.query(Comment).filter(Comment.user_id == user_id).all()