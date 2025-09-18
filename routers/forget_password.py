from fastapi import APIRouter, status, BackgroundTasks, Depends, HTTPException
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from JWT import create_password_reset_token
import jwt 
from JWT import ALGORITHM, SECRET_KEY
from jwt.exceptions import InvalidTokenError
from hashing import Hash
from jwt import ExpiredSignatureError



router = APIRouter(
    tags=['Password Reset']
)


def send_reset_email_dev(email:str, link: str):
    print(f"password reset link for {email}: {link}")
    

@router.post('/forgot_password', status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
def forget_password(request: schemas.ForgetPasswordIn, 
                    background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    email = request.email.strip().lower()
    message = 'Your email is not exist'
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
         return {"message": message}
    
    token = create_password_reset_token(email = email)
    
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    
    background_tasks.add_task(send_reset_email_dev, email, reset_link)
    
    return {"message": 'reset link has been sent'}


@router.post('/password_reset', status_code=status.HTTP_201_CREATED, response_model=schemas.Message)
def reset_password(request: schemas.ResetPasswordIn, db: Session = Depends(get_db)):
    
    try:
        claims = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        if claims.get("scope") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid reset token")
        email = claims.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid reset token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid reset token")


    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        return {"message": "Password has been reset if the account exists."}
    
    user.password = Hash.get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "Password reset successfully"}

    


    
    
    
    