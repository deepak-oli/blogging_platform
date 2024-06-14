from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.likes import Like
from app.models.posts import Post

def create_like(db:Session, post_id: int, user_id: int):
    db_like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

    if db_like:
        raise HTTPException(status_code=400, detail="Post already liked.")

    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()

    return {"post_id": post_id, "count": len(like.post.likes)}


def delete_like(db:Session, post_id: int, user_id: int):
    like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()

    return {"post_id": post_id, "count": len(like.post.likes)}

def get_post_likes(db:Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post_id": post_id, "count": len(post.likes)}

def get_user_likes(db:Session, user_id: int):
    likes = db.query(Like).filter(Like.user_id == user_id).all()

    return  [{"post_id": like.post_id} for like in likes]
    