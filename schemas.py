from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    

class UserUpdate(BaseModel):
    username: str
    password_hash: str
    

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    create_at: datetime
    
    model_config = {"from_attributes": True}

    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    
    
class ForgetPasswordIn(BaseModel):
    email: EmailStr
    

class ResetPasswordIn(BaseModel):
    token: str
    new_password: str
    

class Message(BaseModel):
    message: str
    
    model_config = {"from_attributes": True}


# POST 
class PostCreate(BaseModel):
    title: str
    body: str
    

class PostOut(BaseModel):
    id: int
    title: str
    body: str
    create_at: datetime
    author_id: int

    model_config =  {"from_attributes": True}
    

# Comment 
class CommentCreate(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: int
    body: str
    create_at: datetime
    author_id: int
    post_id: int
    
    model_config = {"from_attributes": True}
