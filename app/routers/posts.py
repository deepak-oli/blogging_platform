from fastapi import APIRouter, Depends, HTTPException,status

from app.services import posts
from app.services.auth import Auth


router = APIRouter(dependencies=[Depends(Auth())])

@router.get("/posts/", tags=["posts"])
def read_posts():
    return posts.get_posts()

@router.post("/posts/", tags=["posts"])
def create_post(post: posts.schemas.PostBase, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']

    return posts.create_post(user_id, post)


@router.get("/posts/{post_id}", tags=["posts"])
def read_post(post_id: int):
    db_post =  posts.get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return db_post

@router.put("/posts/{post_id}", tags=["posts"])
def update_post(post_id: int, new_post: posts.schemas.PostBase, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_post  = posts.get_post(post_id)

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return posts.update_post(post_id, new_post)

@router.delete("/posts/{post_id}", tags=["posts"])
def delete_post(post_id: int, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_post = posts.get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return posts.delete_post(post_id)


@router.patch("/posts/{post_id}", tags=["posts"])
def patch_post(post_id: int, new_post: posts.schemas.PatchPost, dependencies=Depends(Auth())):
    user_id = dependencies['user_id']
    db_post  = posts.get_post(post_id)

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if db_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return posts.update_post(post_id, new_post)