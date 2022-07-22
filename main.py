from ast import Str
from typing import Optional #to make a field optional in our class
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel  
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True #this is an optional field and I'm giving it a default value
    rating:Optional[int]=None #this is fully optional and, if not provided, will default to null 

my_posts=[{'title': 'title of post1', 'content': 'content of post1', 'id':1},{'title': 'favorite foods', 'content': 'I like pasta', 'id':2}] 

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post:Post):
    post_dict=post.dict() #pydantic allows me to convert ot dictionary
    post_dict['id']=randrange(0,100000)
    my_posts.append(post_dict)
    return {"data":post_dict} 

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post=find_post(id)
    if not post:
        response.status_code= status.HTTP_404_NOT_FOUND
        return {'message':f"post with id:{id} was not found"}
    return{"post_detail":post}