from ast import Str
from typing import Optional #to make a field optional in our class
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel  

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True #this is an optional field and I'm giving it a default value
    rating:Optional[int]=None #this is fully optional and, if not provided, will default to null 

my_posts=[{'title': 'title of post1', 'content': 'content of post1', 'id':'1'},{'title': 'favorite foods', 'content': 'I like pasta', 'id':'2'}] 

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/posts")
def createposts(post:Post):
    print(post.rating) 
    print(post.dict())
    return {"data":post} #I can do this because pydantic allows me to convert ot dictionary
    