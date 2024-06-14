from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.services import categories
from app.services.auth import Auth

from app.schemas.categories import Category

router = APIRouter(dependencies=[Depends(Auth())])

@router.get('/categories', tags=["categories"], response_model=list[Category])
def get_categories(db:Session = Depends(get_db)):
    return categories.get_categories(db)

@router.get('/categories/{id}', tags=["categories"], response_model=Category)
def get_category_by_id(id: int, db:Session = Depends(get_db)):
    category = categories.get_category_by_id(db, id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    return category

@router.post('/categories', tags=["categories"], response_model=Category)
def create_category(name: str, db:Session = Depends(get_db)):
    return categories.create_category(db, name)

@router.put('/categories/{id}', tags=["categories"], response_model=Category)
def update_category(id: int, name: str, db:Session = Depends(get_db)):
    return categories.update_category(db, id, name)

@router.delete('/categories/{id}', tags=["categories"], response_model=Category)
def delete_category(id: int, db:Session = Depends(get_db)):
    return categories.delete_category(db, id)