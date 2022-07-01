from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
import app.schemas as schemas
import app.models as models
from app.config import settings as env

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
# SECRET KEY - only known by us
# Algorithm
# Expiration time of token

SECRET_KEY = env.secret_key
ALGORITHM = env.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = env.access_token_expire_minutes

# data contains payload and header
# do not want to modify
def create_access_token(data: dict):
    to_encode = data.copy() # create a copy of the data to prevent modifying it
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) # create expiration time
    to_encode.update({"exp": expire}) # add exp property to to_encode
    # encoded jwt token
    encoded_jwt = jwt.encode(claims = to_encode,
                             key = SECRET_KEY,
                             algorithm = ALGORITHM)
    return encoded_jwt

# verify that payload conforms to TokenData schema (has correct fields)
def verify_access_token(token: str, credentials_exception):
    try:
        # uses key and algorithm to decode token into payload
        # will raise JWT error if signature is invalid in any way
        # (i.e., check is hs(header+payload+secret) == signature)
        payload = jwt.decode(token = token,
                             key = SECRET_KEY,
                             algorithms = [ALGORITHM])
        id: str = payload.get("user_id")

        # if there was no string called id
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
# oauth2 dependency links this
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    # verify that token is correct
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = f"Could not validate credentials.",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "User not found.")

    return user