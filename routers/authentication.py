from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
import JWT


router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post('/', status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'the user is not exist')
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= 'Password is not correct')
        
    access_token = JWT.create_access_token(data={"sub": user.email})
    refresh_token = JWT.create_refresh_token(data={"sub": user.email})
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,           
        samesite="lax",         
        max_age=JWT.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/",               
    )
    
    return schemas.Token(access_token=access_token, token_type="bearer")




