from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    create_at = Column(DateTime(timezone=True), server_default = func.now(), nullable=False)
    


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key =True, index= True)
    title = Column(String)
    body = Column(String)
    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key = True, index = True)
    body = Column(String)
    create_at = Column(DateTime(timezone=True), server_default = func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= 'CASCADE'), nullable=False)
    
    

    