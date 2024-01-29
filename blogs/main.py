from fastapi import FastAPI
from .schemas import Blog



app = FastAPI()



@app.post('/blog/create')
def create_blog(request: Blog):
    return(f'blogs created successfull with title as {request.title}')
    