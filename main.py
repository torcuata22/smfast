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

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/createposts")
def createposts(new_post:Post):
    print(new_post.rating)
    return {"data":"new post"}
    