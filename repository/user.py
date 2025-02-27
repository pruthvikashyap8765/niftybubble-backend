from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from hashing import Hash
from models import User, Favorites




def create_user(db : Session, request : schemas.User ):

    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(status_code=400,detail="Username already exists.")
    

    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400,detail="Email already exists.")
    

    existing_phone = db.query(User).filter(User.phone == request.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400,detail="Phone already exists.")


    new_user = models.User(username = request.username, email = request.email, phone = request.phone ,password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def all(db : Session):
    user = db.query(models.User).all() 
    return user



def add_fav(db : Session,  request : schemas.FavCompanies):
    
    data_existing = db.query(Favorites).filter((Favorites.user_id == request.user_id) & (Favorites.company == request.company)).first()

    if data_existing:
        raise HTTPException(status_code=400, detail= f"{request.company} has already been added to your Favorites")

    new_fav = models.Favorites(company = request.company, user_id = request.user_id)
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)

    favs = db.query(Favorites.company).filter(Favorites.user_id == request.user_id).all()
    favs = [comp[0] for comp in favs]
    return favs




def get_favs(db : Session, id):
    favs = db.query(Favorites.company).filter(Favorites.user_id == id).all()
    favs = [comp[0] for comp in favs]
    return favs








def destroy(db : Session, request: schemas.FavCompanies):
    comp = db.query(Favorites).filter(Favorites.company == request.company and Favorites.user_id == request.user_id)
    
    if not comp.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{comp} is not added")
    
    comp.delete(synchronize_session=False) 
    db.commit() 
    return 'done'




