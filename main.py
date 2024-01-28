from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return 'hello'


@app.get('/blogs')
def get_blogs():
    return 'here is the list of blogs'