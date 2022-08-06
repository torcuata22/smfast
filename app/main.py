from ast import Str
from typing import Optional #to make a field optional in our class
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel  
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True #this is an optional field and I'm giving it a default value
    #rating:Optional[int]=None #this is fully optional and, if not provided, will default to null 

while True: 
    try:
        conn=psycopg2.connect(host='localhost', database='smfast', user='postgres', password='admin9325505', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error:", error)
        time.sleep(2)

my_posts=[{'title': 'title of post1', 'content': 'content of post1', 'id':1},{'title': 'favorite foods', 'content': 'I like pasta', 'id':2}] 

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """) 
    posts =cursor.fetchall() 
    print(posts)
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    #this is the code to work from database:
    cursor.execute("""INSERT INTO posts (title, content, published)VALUES(%s,%s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit() #commits to DB
    return {"data":new_post}
    #these lines were for working with hard coded data
    # post_dict=post.dict() #pydantic allows me to convert ot dictionary
    # post_dict['id']=randrange(0,100000)
    # my_posts.append(post_dict)
      

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post=cursor.fetchone()
    if not post:
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id:{id} was not found"} Replaced by:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"post_detail":post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} doesn't exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) #to make sure we are not sending data back and get an error


@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, str(id)) )
    updated_post=cursor.fetchone()
    conn.commit()
    
   
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} doesn't exist")
    
    return {'data':updated_post}