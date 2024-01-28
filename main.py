from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return 'hello'


@app.get('/blogs')
def get_blogs():
    return 'here is the list of blogs'


@app.get('/blog/{id}')
def get_blog_id(id: int):
    return f'This is the blog with id {id}'


@app.get('/blog/unpublished')
def get_unpublished_blogs():
    return ('unpublished blogs')