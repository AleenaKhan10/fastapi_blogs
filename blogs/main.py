from fastapi import FastAPI, Depends
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
    return(f'blogs created successfull with title as {request.title}')
    