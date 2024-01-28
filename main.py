from fastapi import FastAPI
from typing import Optional


app = FastAPI()


@app.get('/')
def index():
    return 'hello'


@app.get('/blogs')
def get_blogs(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return f'here is the list of {limit} first published blogs'
    else:
        return f'here is the list of {limit} first blogs'


@app.get('/blog/unpublished')
def get_unpublished_blogs():
    return ('unpublished blogs')


@app.get('/blog/{id}')
def get_blog_id(id: int):
    return f'This is the blog with id {id}'

