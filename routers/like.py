from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from oauth2 import get_current_user
import schemas, models


router = APIRouter(
    prefix='/like',
    tags=['Like']
)

@router.post('/{id}', status_code= status.HTTP_200_OK, response_model=schemas.LikeOut)
def post_like(id: int, request: schemas.LikeIn, db: Session = Depends(get_db),
              currentUser: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'the post with {id} is not found')
    
    like = models.Like(like = request.like, author_id = currentUser.id, post_id = id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.LikeOut])
def show_all(db: Session = Depends(get_db), currentUser: models.User = Depends(get_current_user)):
    return db.query(models.Like).all()
    


@router.get('/mine', status_code=status.HTTP_200_OK, response_model=List[schemas.LikeOut])
def my_like(db: Session = Depends(get_db), 
            currentUser: models.User = Depends(get_current_user)):
    return db.query(models.Like).filter(models.Like.author_id == currentUser.id).all()



@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LikeOut)
def single_like(id: int, db: Session = Depends(get_db), 
                currentUser: models.User = Depends(get_current_user)):
    
    like = db.query(models.Like).filter(models.Like.id == id).first()

    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'like with {id} is not found')
        
    return like


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def unlike_post(id: int, db: Session = Depends(get_db),
                currentUser: models.User = Depends(get_current_user)):
    like = db.query(models.Like).filter(models.Like.id == id).first()
    
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'the post with {id} is not found')
    
    owner = db.query(models.Like).filter(models.Like.author_id == currentUser.id).first()

    if like.author_id != owner.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f'not valid of this {id} user')
    
    db.query(models.Like).filter(models.Like.id == id).delete(synchronize_session=False)
    db.commit()
    return {'message': f'successfully deleted with the id: {id}'}

