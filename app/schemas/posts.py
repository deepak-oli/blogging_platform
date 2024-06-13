from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str

class PatchPost(BaseModel):
    title: str = None
    content: str = None

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True