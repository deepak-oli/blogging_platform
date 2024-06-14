from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.categories import Category

def get_categories(db:Session):
    categories = db.query(Category).all()
    return categories

def get_category_by_id(db:Session, id: int):
    category = db.query(Category).filter(Category.id == id).first()
    return category

def create_category(db:Session, name: str):

    db_category = db.query(Category).filter(Category.name == name).first()
    if db_category is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists.")

    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db:Session, id: int, name: str):
    db_category = get_category_by_id(db, id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    category = db.query(Category).filter(Category.id == id).first()
    category.name = name
    db.commit()
    db.refresh(category)
    return category

def delete_category(db:Session, id: int):
    db_category = get_category_by_id(db, id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    category = db.query(Category).filter(Category.id == id).first()
    db.delete(category)
    db.commit()
    return category

