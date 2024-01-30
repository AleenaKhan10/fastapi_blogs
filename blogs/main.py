from fastapi import FastAPI
from . import models
from database.database import engine
from .routers import blogs, users, login



models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(login.router)
