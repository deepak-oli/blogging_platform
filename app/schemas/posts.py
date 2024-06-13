from typing import List
from pydantic import BaseModel
from app.schemas.categories import Category


class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    categories: List[int]

class PatchPost(BaseModel):
    title: str | None = None
    content: str| None = None
    categories: List[int] | None = None

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class PostResponse(Post):
    categories: List[Category]

    class Config:
        from_attributes = True