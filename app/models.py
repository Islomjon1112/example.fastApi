from sqlmodel import SQLModel, Field, Relationship, create_engine, Column, TIMESTAMP, text, ForeignKey, Integer
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import relationship



# Post model
class Post(SQLModel, table=True):

    __tablename__ = "posts"

    #id: int = Field(nullable=False, primary_key=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    created_datetime: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")))
    #updated_datetime: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP")))
    
    # create new column like foreign-key to connect with user table
    owner_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))

    owner: list["User"] = Relationship(back_populates="user")
    
# Create new User table
class User(SQLModel, table=True):

    __tablename__ = "users"

    id: int = Field(nullable=False, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_datetime: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"),))
    phone_number: str 

    user: Post|None = Relationship(back_populates="owner")


# Create new votes table
class Vote(SQLModel, table=True):
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True))
    post_id: int = Field(sa_column=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True))