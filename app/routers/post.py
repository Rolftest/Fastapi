from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import my_engin, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=['Posts'])

# Read all  , response_model=List[schemas.PostVote])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
#    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#    cursor.execute("""SELECT * FROM posts """)
#    posts = cursor.fetchall()
#   LEFT outer Join    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
              models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results
    

# Read 1
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
#    post = cursor.fetchone()
    # print(current_user.email)
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return posts


# Create
@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 #   cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
 #                                                           (post.title, post.content, post.published))
 #   new_post = cursor.fetchone()
 #   conn.commit()
 #   new_post = models.Post(title=post.title, content=post.content, published=post.published)
 #   print(post.dict())
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                                     (post.title, post.content, post.published, str(id)))
    # update_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} das not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized to update Post")                            
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()



# Delete Post
@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post = query_post.first()
   
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} das not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized to Delete")
    query_post.delete(synchronize_session=False)                            
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)