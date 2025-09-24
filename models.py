from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    create_at = Column(DateTime(timezone=True), server_default = func.now(), nullable=False)
    
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key =True, index= True)
    title = Column(String)
    body = Column(String)
    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship("User", back_populates="posts", lazy="selectin")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan", lazy="selectin")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan", lazy="selectin")
    
    
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key = True, index = True)
    body = Column(String)
    create_at = Column(DateTime(timezone=True), server_default = func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= 'CASCADE'), nullable=False)
    
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    
    

class Like(Base):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key = True, index = True)
    like = Column(Boolean)
    author_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=False)
    create_at = Column(DateTime(timezone=True), server_default = func.now(), nullable=False)
    
    user = relationship("User", back_populates="likes")    
    post = relationship("Post", back_populates="likes")    