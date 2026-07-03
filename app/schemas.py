from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(Post):
    pass

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class ResponsePost(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True

class PostWithVotes(BaseModel):
    Post: ResponsePost
    votes: int
    
    class Config:
        from_attributes = True

class User(BaseModel):
    email: EmailStr
    password: str

class UserCreate(User):
    pass


    
    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]