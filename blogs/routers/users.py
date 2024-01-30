from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, hashing, models
from database.database import get_db
from sqlalchemy.orm import Session



router = APIRouter(
    prefix='/user',
    tags=['User']
)



    

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)    
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    user = models.User(name = request.name, email = request.email, password = hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)   
    return user 


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user_from_id(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    return user


@router.delete('/delete/{id}')
def delete_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    db.delete(user)
    db.commit()  
    return user


@router.put('/update/{id}', status_code= status.HTTP_200_OK)
def update_blog(id, request : schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} is not found")
    else:
        user.name = request.name
        user.email = request.email
        user.password = request.password
        db.commit()
        db.refresh(user)
        return user