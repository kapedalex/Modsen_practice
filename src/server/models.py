import sys

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel
from datetime import date
from typing import List

sys.path.append('.')
from server.config import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    created_date = Column(Date, nullable=False)
    rubrics = relationship("Rubric", secondary='post_rubrics')


class Rubric(Base):
    __tablename__ = 'rubrics'
    id = Column(Integer, primary_key=True)
    rubric = Column(String, nullable=False)


class PostRubric(Base):
    __tablename__ = 'post_rubrics'
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    rubric_id = Column(Integer, ForeignKey('rubrics.id'), primary_key=True)


class PostBase(BaseModel):
    text: str
    created_date: date


class PostCreate(PostBase):
    rubrics: List[str]


class RubricBase(BaseModel):
    rubric: str


class RubricCreate(RubricBase):
    pass
