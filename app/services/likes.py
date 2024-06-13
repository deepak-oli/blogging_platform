from fastapi import HTTPException
from app.config.database import get_db

from app.models.likes import Like
from app.models.posts import Post

db = next(get_db())

def create_like(post_id: int, user_id: int):
    db_like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

    if db_like:
        raise HTTPException(status_code=400, detail="Post already liked.")

    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()

    return {"post_id": post_id, "count": len(like.post.likes)}


def delete_like(post_id: int, user_id: int):
    like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()

    return {"post_id": post_id, "count": len(like.post.likes)}

def get_post_likes(post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post_id": post_id, "count": len(post.likes)}

def get_user_likes(user_id: int):
    likes = db.query(Like).filter(Like.user_id == user_id).all()

    return  [{"post_id": like.post_id} for like in likes]
    