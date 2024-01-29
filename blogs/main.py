from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog/create')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(title = request.title, description = request.description)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@app.get('/blog/all')
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
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        blog.update(request)
        db.commit()
        db.refresh(blog)
        return blog
    
    
@app.delete('/blog/delete/{id}', status_code= status.HTTP_200_OK)
def delete_blog(id, request : schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        db.refresh(blog)
        return blog
    

@app.post('/user/create', status_code=status.HTTP_201_CREATED)    
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    user = models.User(name = request.name, email = request.email, password = request.password)
    db.add(user)
    db.commit()
    db.refresh(user)   
    return user 


@app.get('/user/all', status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.user).all()
    return users


@app.get('/user/{id}')
def get_user_from_id(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    return user


@app.delete('user/delete/{id}')
def delete_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    user.delete(synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user


@app.delete('user/put/{id}')
def delete_user(id, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not found')
    user.update(request)
    db.commit()
    db.refresh(user)
    return user