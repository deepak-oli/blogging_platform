
from app.schemas import users as schemas
from app.models import users as models

from app.config.database import get_db

from app.utils.password_hash import get_password_hash

db = next(get_db())


def get_user(user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# def get_users(skip: int = 0, limit: int = 100):
def get_users():
    return db.query(models.User).all()
    # return db.query(models.User).offset(skip).limit(limit).all()


def create_user(user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.email = user.email
    db_user.hashed_password = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_password(user_id: int, password: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.hashed_password = get_password_hash(password)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
