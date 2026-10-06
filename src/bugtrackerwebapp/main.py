from fastapi import FastAPI, HTTPException, status
from .models import BugCreate, BugResponse, BugUpdate
from datetime import datetime
from . import database

app = FastAPI()

bugs = [
    {
    "id": 1,
    "title": "Login nie działa",
    "description": "Przykładowy opis",
    "priority": "High",
    "status": "Proposed",
    "created_at": datetime.now(),
    "updated_at": datetime.now()
        }
    ]   

@app.get("/bugs", response_model = list[BugResponse])
def get_bugs():
    return database.get_bugs()

@app.get("/bugs/{id}", response_model = BugResponse)
def get_bug(id: int):
    
    for bug in bugs:
        if bug["id"] == id:
            return bug
        
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/bugs")
def create_bug(bug: BugCreate):

    now = datetime.now()

    new_bug = {
        "title": bug.title,
        "description": bug.description,
        "priority": bug.priority,
        "status": "Proposed",
        "id": get_next_id(),
        "created_at": now,
        "updated_at": now
        }

    bugs.append(new_bug)

    return new_bug

@app.patch("/bugs/{id}")
def update_bug(id: int, bug: BugUpdate):

    now = datetime.now()

    for bug_update in bugs:
        if bug_update["id"] == id:
            if bug.title is not None:
                bug_update["title"] = bug.title

            if bug.description is not None:
                bug_update["description"] = bug.description

            if bug.priority is not None:
                bug_update["priority"] = bug.priority

            bug_update["updated_at"] = now
            return bug_update
        
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/bugs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bug(id: int):

    for bug in bugs:
        if bug["id"] == id:
            bugs.remove(bug)
            return

    raise HTTPException(status_code=404, detail="Item Not Found")

def get_next_id():

    existing_ids = []

    for bug in bugs:
        existing_ids.append(bug["id"])

    if not existing_ids:
        return 1

    bug_id = max(existing_ids) + 1

    return bug_id