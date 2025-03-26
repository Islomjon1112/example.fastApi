from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Column, TIMESTAMP, text
from pydantic.types import conint


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = True 

class PostCreate(PostBase):
    pass

# create class to provide response
class UserResponse(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    created_datetime: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")))


class PostResponse(PostBase):
    id: Optional[int] = None
    created_datetime: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")))
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    owner: UserResponse

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

# Create new schema for user table
class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None


# Create new authenticaton schema
class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None

# Create a schema for Token
class Token(BaseModel):
    access_token: str
    token_type: str

# create a schema for TokenData
class TokenData(BaseModel):
    id: Optional[int] = None

# Create new schema for vote
class Vote(BaseModel):
    post_id: int
    dir: int = conint(le=1)
