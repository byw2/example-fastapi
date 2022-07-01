from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from app.database import get_db
import app.models as models
import app.schemas as schemas
import app.utils as utils
import app.oauth2 as oauth2

# object containing all routes for login 
router = APIRouter(
    prefix = "/login",
    tags = ["Authentication"]
)

# user_credentials returns a dictionary with username and password
@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # check that user exists
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid credentials."
        )
    # check that password is correct
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials."
        )
    
    # create JWT token if credentials are valid
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {'access_token': access_token, "token_type": "bearer"}