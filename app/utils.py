# stores utility functions
from passlib.context import CryptContext

# passlib context is used to hash and verify passwords
# telling passlib what is default hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)