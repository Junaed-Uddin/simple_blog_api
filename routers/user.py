from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
import schemas, models
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from oauth2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(username = request.username, email = request.email,
                           password = Hash.get_password_hash(request.password_hash))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

   
   
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def show_all(db: Session = Depends(get_db), 
             current_user: schemas.UserCreate = Depends(get_current_user)):
    return db.query(models.User).all()



@router.get('/me', response_model = schemas.UserOut)
def user_me(current_user: schemas.UserCreate = Depends(get_current_user)):
    return current_user



@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def single_show(id: int, db: Session = Depends(get_db), 
                current_user: schemas.UserCreate = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'the user {id} is not available')
    return user


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def user_update(id: int, request: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: schemas.UserCreate = Depends(get_current_user)):
    user = db.get(models.User, id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'the user with id {id} is not exist')

    data = request.model_dump(exclude_unset=True)
    
    for i, j in data.items():
        setattr(user, i, j)
        
    db.commit()
    db.refresh(user)
    return user



@router.delete('/{id}')
def user_delete(id: int, db: Session = Depends(get_db), 
                current_user: schemas.UserCreate = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'the id {id} is not available')
    db.commit()
    return {'message': f'the user with id {id} is successfully deleted'}



