from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import users, auth, posts, comments, likes, categories

from app.config.database import create_tables

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Running"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(categories.router)
app.include_router(comments.router)
app.include_router(likes.router)

create_tables()



