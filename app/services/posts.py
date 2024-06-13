from app.models import posts as models
from app.schemas import posts as schemas

from app.config.database import get_db

db = next(get_db())

def get_posts():
    return db.query(models.Post).all()

def get_post(post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def create_post(user_id: int, post: schemas.PostBase):
    db_post = models.Post(
        user_id=user_id,
        **post.model_dump()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(post_id: int, post: schemas.PostBase | schemas.PatchPost):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    for key, value in vars(post).items():
        setattr(db_post, key, value) if value else None
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post