from typing import List
from fastapi import status, Response, HTTPException, Depends, APIRouter
from ..import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
     prefix="/posts",
     tags=["posts"]
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts


@router.post("/",  status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int, db:Session=Depends(get_db)):
    #cursor.execute("""select * from posts where id=%s""", (str(id)))
    #test_post=cursor.fetchone()
    test_post=db.query(models.Post).filter(models.Post.id==id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id : {id} is not found')
    return test_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session= Depends(get_db)):
    #cursor.execute("""delete from posts where id = %s returning *""",str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    deleted_post=db.query(models.Post).filter(models.Post.id==id).first()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id :{id} not found')
    db.delete(deleted_post, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db)):
        #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *"""),
        #( post.title, post.content, post.published, str(id))
        #updated_post=cursor.fetchone()
        #conn.commit()
        ''' index=find_index_post(id) '''
        post_query=db.query(models.Post).filter(models.Post.id==id)
        updated_post=post_query.first()
        if updated_post==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id : {id} not found')
        post_query.update(post.dict(), 
                    synchronize_session=False)
        db.commit()
        '''post_dict=post.dict()
        post_dict['id']=id 
        my_posts[index]=post_dict '''
        return updated_post