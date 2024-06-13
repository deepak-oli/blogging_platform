from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str

class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True