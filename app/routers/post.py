from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import models, schemas,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List,Optional


router=APIRouter(prefix="/posts",
                 tags=['Posts']
                 )


@router.get("/",response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db),limit:int = 30,search:Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id , isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    print(results)
    #print(posts)

    result_list = []

    for post, vote_count in results:
        post_dict = {"post": post, "votes": vote_count}
        result_list.append(post_dict)

    return result_list
   


#@router.get("/my",response_model=List[schemas.PostResponse])
#def get_my_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    #print(posts)

    #return posts


# Inserting data into database via alchemy
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    try:
        # new_posts = models.Post(title=post.title, content=post.content, published=post.published)
       
        new_posts = models.Post(owner_id=current_user.id,**post.dict())
        db.add(new_posts)
        db.commit()
        db.refresh(new_posts)
        return new_posts

    except Exception as error:
        db.rollback()
        return {"error": error}


# Using sqlalchemy to retrieve one post from the database
# @app.get("/posts/{id}", response_model=Post)


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,) )
    # post = cursor.fetchone()
   
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id , isouter = True).group_by(models.Post.id).filter(models.Post.id == id) 
    post, vote_count = post_query.first()
  
    print(post)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )
    # if post.owner_id != current_user.id:
    #             raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail=f"Cannot access another user's post",
    #         )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return{ "Error": f"Post not with {id} was not found"}
    # return {"title": post.title, "content": post.content, "published": post.published , "id": post.id}
    return {"post": post, "votes": vote_count}


"""


def get_db():
    # Connect to the PostgreSQL database
    db = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password=12345,
        cursor_factory=RealDictCursor
    )
    
    # Create a cursor object for database interaction
    cursor = db.cursor()

    try:
        # Yield the cursor to the dependent function
        yield cursor
    finally:
        # Cleanup: close the cursor and the database connection
        cursor.close()
        db.close()
"""


@router.delete("/{id}")
def del_post(
    id: int,
    db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)
):
    # cursor: RealDictCursor = Depends(get_db):
    try:
        # Execute DELETE query
        # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING id", (id,))
        # deleted_id = cursor.fetchone()
        # Check if the post with the given ID exists
        deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
        if not deleted_post:
            return {"message": f"Post with id {id} not found or already deleted"}

        # Check if the current user is the owner of the post
        if deleted_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cannot delete another user's post",
            )

        # Delete the post
        db.delete(deleted_post)
        db.commit()

        return {
            "success": f"Post with id {deleted_post.id} has been successfully deleted"
        }
    except Exception as error:
        # Rollback the transaction in case of an error
        db.rollback()
        # Print the error for debugging
        print("Error:", error)
        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


def find_post_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.Post).filter(models.Post.id == id).first()


# cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
# post = cursor.fetchone()
# return post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post_route(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    try:
        new_post = find_post_by_id(id, db=db)

        # Check if new post has a value
        if new_post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} not found",
            )
        
        if new_post.owner_id != current_user.id:
                    raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cannot update another user's post",
            )


        new_post.title = post.title
        new_post.content = post.content
        new_post.published = post.published

        # commit update to database
        db.commit()

        #Refresh the state of the object in the session
        db.refresh(new_post)

        #return new_post
        return new_post

    except Exception as error:
        # Rollback the transaction in case of an error
        db.rollback()
        # Print the error for debugging
        print("Error:", error)
        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (title, content, published, id,))
    # updated_post = cursor.fetchone()
    # db.commit()
    # return{"updated_post":new_post}
