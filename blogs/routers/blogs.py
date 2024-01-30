from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models
from database.database import get_db
from sqlalchemy.orm import Session



router = APIRouter(
    prefix='/blog',
    tags=['blog']
)



@router.post('/create', response_model= schemas.ShowBlog)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(title = request.title, description = request.description, user_id = 3)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get('/all', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{id}', status_code= status.HTTP_201_CREATED)
def get_blog_from_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with this id {id} is not found')
    return blog


@router.put('/update/{id}', status_code= status.HTTP_200_OK)
def update_blog(id, request : schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        blog.title = request.title
        blog.description = request.description
        db.commit()
        db.refresh(blog)
        return blog
    
    
@router.delete('/delete/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        db.delete(blog)
        db.commit()
        return blog
