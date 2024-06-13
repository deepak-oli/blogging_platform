from fastapi import APIRouter, Depends, HTTPException,status

from app.services import posts
from app.services.auth import Auth


router = APIRouter(dependencies=[Depends(Auth())])

@router.get("/posts/", tags=["posts"], response_model=list[posts.schemas.PostResponse])
def read_posts():
    return posts.get_posts()

@router.post("/posts/", tags=["posts"])
def create_post(new_post: posts.schemas.PostCreate, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']

    post = new_post.model_copy().model_dump()
    categories = post.pop('categories', None)


    if categories is None or len(categories) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categories is required.")

    for category_id in categories:
        db_category = posts.get_category_by_id(category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    return posts.create_post(user_id, posts.schemas.PostBase(**post), categories)


@router.get("/posts/{post_id}", tags=["posts"])
def read_post(post_id: int):
    db_post =  posts.get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return db_post

@router.put("/posts/{post_id}", tags=["posts"])
def update_post(post_id: int, new_post: posts.schemas.PostCreate, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_post  = posts.get_post(post_id)

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    
    post = new_post.model_copy().model_dump()
    categories = post.pop('categories',None)

    if categories is None or len(categories) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categories is required.")

    for category_id in categories:
        db_category = posts.get_category_by_id(category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

    return posts.update_post(post_id, posts.schemas.PostBase(**post), categories)

@router.delete("/posts/{post_id}", tags=["posts"])
def delete_post(post_id: int, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_post = posts.get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return posts.delete_post(post_id)


# @router.patch("/posts/{post_id}", tags=["posts"])
# def patch_post(post_id: int, new_post: posts.schemas.PatchPost, dependencies=Depends(Auth())):
#     user_id = dependencies['user_id']
#     db_post  = posts.get_post(post_id)

#     if db_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

#     if db_post.user_id != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    
#     post = new_post.model_copy().model_dump()
#     categories = post.pop('categories', None)
#     return posts.update_post(post_id,  posts.schemas.PatchPost(**post), categories)