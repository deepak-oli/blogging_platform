from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)

    posts = relationship("Post", secondary='post_categories', back_populates="categories")

class PostCategory(Base):
    __tablename__ = "post_categories"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
