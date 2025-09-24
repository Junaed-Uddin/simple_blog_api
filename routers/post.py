from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models
from database import get_db
from oauth2 import get_current_user
from typing import List



router = APIRouter(
    prefix='/post',
    tags=['Post']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(request: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user) ):
    new_post = models.Post(title = request.title, body = request.body, author_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.PostWithDetails])
def all_user_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Post).all()


@router.get('/mine', status_code=status.HTTP_200_OK, response_model=List[schemas.PostWithDetails])
def single_user_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Post).filter(models.Post.author_id == current_user.id).all()


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostWithDetails)
def single_show(id: int, db: Session = Depends(get_db), currentUser: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'the post with the id: {id} is not found')
    return post


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def post_update(id: int, request: schemas.PostCreate, db: Session = Depends(get_db), currentUser: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).update(request.model_dump(exclude_unset=True), 
                                                                     synchronize_session=False)
    if not post:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
                            detail= f'the post with id:{id} is not found')
    
    db.commit()
    return post



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def post_delete(id: int, db: Session = Depends(get_db), currentUser: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'the post with id: {id} is not found')
    db.commit()
    return {'message': 'the post is successfully deleted'}
