from fastapi import FastAPI, HTTPException, status
from .models import BugCreate, BugResponse, BugUpdate
from . import database

app = FastAPI()
database.init_db()

@app.get("/bugs", response_model = list[BugResponse])
def get_bugs():
    return database.get_bugs()

@app.get("/bugs/{id}", response_model = BugResponse)
def get_bug(id: int):
    
    bug = database.get_bug(id)

    if bug is None: 
        raise HTTPException(status_code=404, detail="Item not found")

    return bug
    
@app.post("/bugs", response_model = BugResponse, status_code=status.HTTP_201_CREATED)
def create_bug(bug: BugCreate):  

    return database.create_bug(bug.title, bug.description, bug.priority)

@app.patch("/bugs/{id}", response_model = BugResponse)
def update_bug(id: int, bug: BugUpdate):

    updated_bug = database.update_bug(id, bug.title, bug.description, bug.priority, bug.status)

    if updated_bug is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_bug

@app.delete("/bugs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bug(id: int):


    is_bug_deleted = database.delete_bug(id)

    if is_bug_deleted is False:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return
