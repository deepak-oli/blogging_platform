from fastapi import HTTPException, status

from app.models import posts as models
from app.schemas import posts as schemas
from app.models.categories import PostCategory
from .categories import get_category_by_id


from app.config.database import get_db

db = next(get_db())

def get_posts():
    return db.query(models.Post).all()

def get_post(post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def create_post(user_id: int, post: schemas.PostBase, categories: list[int]):
    for category_id in categories:
        db_category = get_category_by_id(category_id)

        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")    

    db_post = models.Post(
        user_id=user_id,
        **post.model_dump()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    for category_id in categories:
        db_post_category = PostCategory(
            post_id=db_post.id,
            category_id=category_id
        )
        db.add(db_post_category)
        db.commit()
        db.refresh(db_post_category)

    return schemas.PostResponse(
        id=db_post.id, 
        user_id=db_post.user_id, 
        **post.model_dump(),
        categories=[get_category_by_id(category_id) for category_id in categories]            
    )

def update_post(post_id: int, post: schemas.PostBase, categories: list[int]):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    for key, value in vars(post).items():
        setattr(db_post, key, value) if value else None
    db.commit()
    db.refresh(db_post)
    for category_id in categories:
        db_category = get_category_by_id(category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        db_post_category = db.query(PostCategory).filter(PostCategory.post_id == post_id, PostCategory.category_id == category_id).first()
        if db_post_category is None:
            db_post_category = PostCategory(
                post_id=post_id,
                category_id=category_id
            )
            db.add(db_post_category)
            db.commit()
            db.refresh(db_post_category)
    
    # Remove categories that are not in the new list
    db.query(PostCategory).filter(PostCategory.post_id == post_id).filter(~PostCategory.category_id.in_(categories)).delete(synchronize_session=False)
    db.commit()
        
    return schemas.PostResponse(
        id=db_post.id, 
        user_id=db_post.user_id, 
        title=db_post.title,
        content=db_post.content,
        categories=[get_category_by_id(category.id) for category in db_post.categories]
    )

def delete_post(post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post