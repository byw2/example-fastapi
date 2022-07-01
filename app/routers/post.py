from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user
from app.database import get_db
import app.schemas as schemas
import app.models as models
import app.oauth2 as oauth2


router = APIRouter(
    prefix = "/posts",
    tags=["Post"]
)

# get all posts
# use database object (session) to query all posts
# ORM will convert the Python into SQL under the hood at 
# fetch all posts
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, 
              skip: int = 0,
              search: Optional[str] = ""):
    # query = """SELECT * FROM posts;"""
    # cur.execute(query)
    # posts = [dict(post) for post in cur.fetchall()]
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
                 join(models.Vote, 
                      models.Post.owner_id == models.Vote.post_id,
                      isouter=True).\
                 group_by(models.Post.id).\
                 filter(models.Post.title.contains(search)).\
                 limit(limit).\
                 offset(skip).\
                 all()
    print(results)
    return results

# gets a post with given id
# note: id has to be validated as an integer
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, 
             db: Session = Depends(get_db),
             limit: int = 10, 
             skip: int = 0,
             search: Optional[str] = ""):
    # query = """SELECT * FROM posts WHERE id = %s;"""
    # cur.execute(query, (str(id)))
    # post = cur.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
                                join(models.Vote, 
                                     models.Post.owner_id == models.Vote.post_id,
                                     isouter=True).\
                                group_by(models.Post.id).\
                                filter(models.Post.title.contains(search)).\
                                limit(limit).\
                                offset(skip).\
                                first()
    if post is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Post with id of {id} not found."
        )
    return post

# creates new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db),
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # query = """INSERT INTO posts (title, content, published) 
    #         VALUES (%s, %s, %s) RETURNING *;"""
    # cur.execute(query, (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()

    # spreads out all attributes in dictionary from post pydantic model
    new_post = models.Post(**post.dict(), owner_id = current_user.id)
    db.add(new_post) 
    db.commit()
    # conn.commit()
    # immediately reload attributes on new_post
    db.refresh(new_post) 
    return new_post

# delete post with given id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, 
                 db: Session = Depends(get_db),
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # index, _ = find_post(id)
    # query = """DELETE FROM posts WHERE id = %s RETURNING *;"""
    # cur.execute(query, (str(id),))
    # deleted_post = cur.fetchone()
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    if delete_query.first() is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Post with id of {id} not found."
        )
    print(current_user.id)
    print(delete_query.first().owner_id)
    # check to make sure current user created this post
    if current_user.id != delete_query.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to perform requested action."
        )
    # matching objects within the Session will be marked as deleted and expunged
    # deleted_post contains WHERE command in SQL
    delete_query.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# update post with given id
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, 
                post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # query = """UPDATE posts SET title = %s, content = %s,
    #         published = %s WHERE id = %s RETURNING *;"""
    # cur.execute(query, (post.title, post.content, post.published, str(id)))
    # updated_post = cur.fetchone()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    if update_query.first() is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Post with id of {id} not found."
        )
    # check to make sure current user created this post
    if current_user.id != update_query.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to perform requested action."
        )
    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return update_query.first()

# gets latest post - order matters!
# @router.get("/latest")
# def get_latest_post():
#     query = """SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;"""
#     cur.execute(query)
#     latest_post = cur.fetchone()
#     return latest_post