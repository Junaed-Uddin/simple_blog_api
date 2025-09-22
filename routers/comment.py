from fastapi import APIRouter, status, HTTPException, Depends
import schemas, models
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user


router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)

@router.post('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def comment_create(id: int, request: schemas.CommentCreate, db: Session = Depends(get_db), 
                   currentUser: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the id: {id} is not found')
    
    new_comment = models.Comment(body = request.body, author_id = currentUser.id, 
                                 post_id = id)
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get('/', status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db), currentUser: models.User = Depends(get_current_user)):
    return db.query(models.Comment).all()


@router.get('/mine', status_code=status.HTTP_200_OK)
def my_comments(db: Session = Depends(get_db), currentUser: models.User = Depends(get_current_user)):
    mine = db.query(models.Comment).filter(models.Comment.author_id == currentUser.id).all()
    return mine


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def comment_update(id: int, request: schemas.CommentCreate, db: Session = Depends(get_db),
                   currentUser: models.User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    owner = db.query(models.Comment).filter(models.Comment.author_id == currentUser.id).first()

    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= 'Not found any comment')
    
    if owner.author_id != comment.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f'Not valid for this user')
        
    data = request.model_dump(exclude_unset=True)
    for i, j in data.items():
        setattr(comment, i, j)
        
    db.commit()
    db.refresh(comment)
    return comment


@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED)
def single_show(id: int, db: Session = Depends(get_db), 
                currentUser: models.User = Depends(get_current_user)):
    single_comment = db.query(models.Post).filter(models.Post.id == id).first()

    if not single_comment:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'comment {id} is not found')
         
    return single_comment



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(id: int, db: Session = Depends(get_db), 
                   currentUser: models.User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    
    if not comment: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'comment {id} is not found')
        
    owner = db.query(models.Comment).filter(models.Comment.author_id == currentUser.id).first()
    

    if comment.author_id != owner.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f'Not validate for this user {id}')

    db.query(models.Comment).filter(models.Comment.id == id).delete(synchronize_session=False)
    db.commit()
    return {'message': f'successfully deleted with the id: {id}'}
    
    

    
    