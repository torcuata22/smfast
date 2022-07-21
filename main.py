from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/createposts")
def createposts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post":f"title {payLoad['title']} content: {payLoad['content']}"}
    