from fastapi import APIRouter, Depends, status
import schemas
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from repository import user
from oauth2 import get_current_user







router = APIRouter(
    prefix = '/user',
    tags=['Users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    return user.create_user(db, request)
    



@router.get('/', response_model=List[schemas.ShowUser]) 
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.all(db)


@router.post('/favorites', response_model=List[str])
def fav( request: schemas.FavCompanies, current_user: schemas.User = Depends(get_current_user), db:Session = Depends(get_db),): 
    return user.add_fav(db, request)


@router.get('/favorites/{id}', response_model=List[str])
def get_favs(id, db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)   ):
    return user.get_favs(db,id)



@router.delete('/favorites', status_code=status.HTTP_204_NO_CONTENT) 
def destroy(request : schemas.FavCompanies, db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.destroy(db,request)