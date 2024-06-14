from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import users, auth, posts, comments, likes, categories

# load environment variables
load_dotenv()

# create FastAPI instance
app = FastAPI()

# root route
@app.get("/")
def read_root():
    return {"message": "Running"}

#  register routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(categories.router)
app.include_router(comments.router)
app.include_router(likes.router)



