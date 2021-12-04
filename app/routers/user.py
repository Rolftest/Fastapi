
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import my_engin, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.User)
def user_creat(user: schemas.UserCreat, db: Session = Depends(get_db)):
    # hash the user.password
    user.password = utils.hash_me(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID: {id} does not exist")
    return user