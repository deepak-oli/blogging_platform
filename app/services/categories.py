from fastapi import HTTPException, status

from app.config.database import get_db
from app.models.categories import Category

db = next(get_db())

def get_categories():
    categories = db.query(Category).all()
    return categories

def get_category_by_id(id: int):
    category = db.query(Category).filter(Category.id == id).first()
    return category

def create_category(name: str):
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(id: int, name: str):
    db_category = get_category_by_id(id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    category = db.query(Category).filter(Category.id == id).first()
    category.name = name
    db.commit()
    db.refresh(category)
    return category

def delete_category(id: int):
    db_category = get_category_by_id(id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    category = db.query(Category).filter(Category.id == id).first()
    db.delete(category)
    db.commit()
    return category

