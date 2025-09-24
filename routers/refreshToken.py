from fastapi import APIRouter, status, HTTPException, Depends, Request, Response
from sqlalchemy.orm import Session
from database import get_db
import jwt
from JWT import SECRET_KEY, ALGORITHM, create_access_token
from jwt.exceptions import InvalidTokenError
from jwt import ExpiredSignatureError
import models, schemas


router = APIRouter(
    prefix='/refreshToken',
    tags=['Login']
)


@router.post('/', status_code= status.HTTP_200_OK)
def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
    
    refreshToken = request.cookies.get("refresh_token")
    if not refreshToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="No refresh token")
    try:
        claims = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
        if claims.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid token type")
            
        email = claims.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid refresh token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Refresh token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail= 'User not found')
    
    new_access = create_access_token({"sub": user.email})

    return schemas.Token(access_token=new_access, token_type="bearer")

