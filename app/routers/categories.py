from fastapi import APIRouter,Depends, HTTPException, status

from app.services import categories
from app.services.auth import Auth
from app.schemas.categories import Category, CategoryBase

router = APIRouter(dependencies=[Depends(Auth())])

@router.get('/categories', tags=["categories"], response_model=list[Category])
def get_categories():
    return categories.get_categories()

@router.get('/categories/{id}', tags=["categories"], response_model=Category)
def get_category_by_id(id: int):
    category = categories.get_category_by_id(id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    return category

@router.post('/categories', tags=["categories"], response_model=CategoryBase)
def create_category(name: str):
    return categories.create_category(name)

@router.put('/categories/{id}', tags=["categories"], response_model=Category)
def update_category(id: int, name: str):
    return categories.update_category(id, name)

@router.delete('/categories/{id}', tags=["categories"], response_model=Category)
def delete_category(id: int):
    return categories.delete_category(id)