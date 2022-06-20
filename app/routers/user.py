from fastapi import Response, HTTPException, Depends, status, APIRouter
from typing import List
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db

router = APIRouter(
    prefix = "/users",
    tags=["User"]
)

@router.get('/', response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Post with id of {id} not found."
                           )
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete('/{id}', response_model=schemas.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_query = db.query(models.User).filter(models.User.id == id)
    if delete_query.first() is None:
        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Post with id of {id} not found."
                           )
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put ('/{id}', response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    update_query = db.query(models.User).filter(models.User.id == id)
    if update_query.first() is None:
        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Post with id of {id} not found."
                           )
    new_user = user.dict()
    # hashes the new password
    new_user['password'] = utils.hash(new_user['password'])                       
    update_query.update(new_user, synchronize_session=False)
    db.commit()
    return update_query.first()