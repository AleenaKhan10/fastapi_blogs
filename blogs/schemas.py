from pydantic import BaseModel




class Blog(BaseModel):
    title: str
    description: str

    class Config():
        orm_mode = True 
    

class User(BaseModel):
    name: str
    email : str
    password : str
    
    
class ShowUser(BaseModel):
    name: str
    email : str
    class Config():
        orm_model = True
        
        

class ShowBlog(Blog):
    creator: ShowUser
    id : int
    class Config():
        orm_mode = True 
        
        

class Login(BaseModel):
    username : str
    password : str