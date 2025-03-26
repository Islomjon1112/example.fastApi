from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg
from typing import Optional
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, Field, create_engine

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:malika1802@localhost/fastApi"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create tables using SQLModel
SQLModel.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(default=None)
    published: bool = Field(default=True)

while True:
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname="fastApi",
            user="postgres",
            password="malika1802"
        )
        cursor = conn.cursor()
        print("Database connection was succesfull ")
        break

    except psycopg.OperationalError as error:
        print("connection to database was failed")
        print("Error: ", error)
        time.sleep(2)


# Create a schema
class Post(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = True 


#This is an array with some dictionary 
my_post = [{"title": "Today it is snowing", "content": "And also it is windy", "id": 1},
           {"title": "Tomorrow it will be snow", "content": "And there is no sun", "id": 2}]


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_session)):
    return {"status": "success"}

# Just get post
@app.get("/createposts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"message": posts}

# Just create post with using Post method
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# Just get one individual post with using Get method
@app.get("/createposts/{id}")
def get_one_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"this id {id} was not found!")
    return {"post_detail": test_post}

# # Delete some post
@app.delete("/createposts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"this is id {id} does not exit!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update new data into post
@app.put("/createposts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"this is id {id} does not exit!")
    
    return {"data": update_post}