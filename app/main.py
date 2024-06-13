from fastapi import FastAPI

from app.routers import users, auth

from app.config.database import create_tables

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

create_tables()


@app.get("/")
def read_root():
    return {"message": "Running"}
