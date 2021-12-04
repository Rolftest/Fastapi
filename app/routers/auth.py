from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import my_engin, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login", tags=['Authentification'])

@router.post("/", status_code=HTTP_202_ACCEPTED, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"infvalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"infvalid Password Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}