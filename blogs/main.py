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


@app.put('/blog/{id}', status_code= status.HTTP_200_OK)
def update_blog(id, request : schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        blog.update(request)
        db.commit()
        db.refresh(blog)
        return blog
    
    
@app.put('/blog/{id}', status_code= status.HTTP_200_OK)
def delete_blog(id, request : schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not found")
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        db.refresh(blog)
        return blog