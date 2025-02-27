from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import token_utils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #This is the route where the dastapi will fetch the token


def get_current_user(Token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )



    return token_utils.verify_token(Token, credentials_exception)


