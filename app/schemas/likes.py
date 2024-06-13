from pydantic import BaseModel


    
class Like(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True

class LikeResponse(BaseModel):
    post_id: int
    count: int

    class Config:
        from_attributes = True

class UserLike(BaseModel):
    post_id: int

    class Config:
        from_attributes = True