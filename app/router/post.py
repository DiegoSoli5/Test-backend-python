
from sqlalchemy import func

from .. import models, schemas,oauth2
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.ResponsePost])
@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # data = cursor.fetchall()
    # data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result


# we only want the user to send the title and content of the post, so we can create a model for that


    
# def get_post_by_id(id: int):
#     for i, post in enumerate(data):
#         if post['id'] == id:
#             return i
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")


# extracting data from the request body
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # data = cursor.fetchone()
    # conn.commit()
    # return {"new_post": data}
    print(current_user.email)
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest")
def get_latest_post(db: Session = Depends(get_db), response_model=schemas.ResponsePost):
    # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    # latest_post = cursor.fetchone()
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post

# geting a single post by id
@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # data = cursor.fetchone()
    data = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    print(data)
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="post was not found")
    return data
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
        
    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"deleted_post": deleted_post}

@router.put("/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
        
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(exclude_unset=True))
    
    db.commit()
    return {"updated_post": post_query.first()}
