from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.errors import DateTimeError
from datetime import datetime

from pydantic.types import conint
from sqlalchemy.sql.sqltypes import Boolean

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreat(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True   


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: User

    class Config:
        orm_mode = True    

class Posttest(PostBase):
    published: bool
    id: int
    user_id: int
    content: str
    title: str    
    created_at: datetime

class PostVote(PostBase):
    Post: Posttest
    votes: int 

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str    

class TokenData(BaseModel):
    id: Optional[str]  

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
