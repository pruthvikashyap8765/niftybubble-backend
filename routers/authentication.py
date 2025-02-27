from fastapi import APIRouter, Depends, HTTPException, status
import schemas, database, models
from sqlalchemy.orm import Session
from hashing import Hash
from token_utils import create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm





router = APIRouter(
    tags= ['Authentication']
)



@router.post('/login')

def login(request : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): #To use the authorizer we need to use OAuth2PasswordRequestForm for request
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Invalid Credentials')
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Incorrect Password')
    



    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}
        , expires_delta=access_token_expires 
    )
    return schemas.Token(access_token=access_token, token_type="bearer", user_id = user.id)

