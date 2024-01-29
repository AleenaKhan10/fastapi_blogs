from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models, hashing
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import delete



models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog/create', response_model= schemas.ShowBlog)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(title = request.title, description = request.description, user_id = 3)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@app.get('/blog/all', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code= status.HTTP_201_CREATED)
def get_blog_from_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with this id {id} is not found')
    return blog


@app.put('/blog/update/{id}', status_code= status.HTTP_200_OK)
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
    
    
@app.delete('/blog/delete/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        db.delete(blog)
        db.commit()
        return blog
    

@app.post('/user/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)    
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    user = models.User(name = request.name, email = request.email, password = hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)   
    return user 


@app.get('/user/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', response_model=schemas.ShowUser)
def get_user_from_id(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    return user


@app.delete('/user/delete/{id}')
def delete_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    db.delete(user)
    db.commit()  
    return user


@app.put('/user/update/{id}', status_code= status.HTTP_200_OK)
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