from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash:
    
    def bcrypt(password: str):
        hashed_password = pwd_context.hash(password)
        return hashed_password
    
    
    def verify(password, hashed_password):
        return pwd_context.verify(password, hashed_password)
    