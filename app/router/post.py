from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_session

# declare router
router = APIRouter(
    prefix="/createposts",
    tags= ["Posts"]
)


# API routes for CRUD operations (you can adapt your existing logic here)
@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):

    #posts = db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all() # Use SQLModel to query the database

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    # response = [
    #     {**post.__dict__, "votes": votes} for post, votes in result
    # ]

    return posts


# Create post with SQLAlchemy/SQLModel
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    print(current_user.email)
    post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# Fetch single post
@router.get("/{id}", response_model=schemas.PostOut)
def get_one_post(id: int, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found!")
    return post


# Delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    #delete_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    #update_post = cursor.fetchone()
    #conn.commit()
    db_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post

