from pydantic import BaseModel




class Blog(BaseModel):
    title: str
    description: str
    

class User(BaseModel):
    name: str
    email : str
    password : str