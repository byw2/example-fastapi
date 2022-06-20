from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# definition of schema via pydantic module
# contract between client and API

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

# Request Schemas
class PostCreate(PostBase):
    pass

class UserCreate(UserBase):
    pass  

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# user sends token in header back to API
class Token(BaseModel):
    access_token: str
    token_type: str

# user sends data for token creation
class TokenData(BaseModel):
    id: Optional[str] = None

# Response Schemas
class User(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True

# schema for response of user creation and update
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # tell the Pydantic model to read the data even if it is not a dict, 
    # but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# schema for body of vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)