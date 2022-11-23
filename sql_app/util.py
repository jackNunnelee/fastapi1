from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(orig_pword, hashed_pword):
    return pwd_context.verify(orig_pword, hashed_pword)