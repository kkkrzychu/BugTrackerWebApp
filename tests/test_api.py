from fastapi.testclient import TestClient
from bugtrackerwebapp.main import app
import pytest
from bugtrackerwebapp import database

client = TestClient(app)

@pytest.fixture(autouse=True)
def prepare_test_db(tmp_path):

    original_db = database.DB_PATH    

    database.DB_PATH = tmp_path / "test_bugtracker.db"

    database.init_db()

    yield

    database.DB_PATH = original_db

@pytest.fixture
def sample_bug_data():

    return {
        "title": "Login error",
        "description": "Login button does not work",
        "priority": "High"
    }

@pytest.fixture
def created_bug(sample_bug_data):

    post_response = client.post("/bugs", json = sample_bug_data)

    assert post_response.status_code == 201

    return post_response.json()

def test_get_bugs():

    response = client.get("/bugs")

    assert response.status_code == 200
    assert response.json() == []

def test_get_nonexistent_bug():

    response = client.get("/bugs/9999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_create_bug():

    bug_data = {
                "title": "Login error",
                "description": "Login button does not work",
                "priority": "High" 
                }
    post_response = client.post("/bugs", json = bug_data)
    created_bug = post_response.json()    

    assert post_response.status_code == 201

    bug_id = created_bug["id"]

    assert created_bug["id"] > 0
    assert created_bug["title"] == bug_data["title"]
    assert created_bug["description"] == bug_data["description"]
    assert created_bug["priority"] == bug_data["priority"]    
    assert created_bug["status"] == "Proposed"

    get_response = client.get(f"/bugs/{bug_id}")
    fetched_bug = get_response.json()

    assert get_response.status_code == 200
    assert fetched_bug["id"] == bug_id
    assert fetched_bug["title"] == bug_data["title"]
    assert fetched_bug["description"] == bug_data["description"]
    assert fetched_bug["priority"] == bug_data["priority"]
    assert fetched_bug["status"] == "Proposed"

def test_update_bug(created_bug, sample_bug_data):       
       
       updated_priority = "Low"
       
       bug_id = created_bug["id"]

       patch_response = client.patch(f"/bugs/{bug_id}", json = {"priority": updated_priority})
       
       assert patch_response.status_code == 200
       
       updated_bug = patch_response.json() 
       
       assert updated_bug["title"] == sample_bug_data["title"]
       assert updated_bug["description"] == sample_bug_data["description"]
       assert updated_bug["priority"] == updated_priority

       get_response = client.get(f"/bugs/{bug_id}")

       assert get_response.status_code == 200

       fetched_bug = get_response.json()

       assert fetched_bug["priority"] == updated_priority
       assert fetched_bug["title"] == sample_bug_data["title"]
       assert fetched_bug["description"] == sample_bug_data["description"]

def test_delete_bug(created_bug):

    bug_id = created_bug["id"]

    first_delete_response = client.delete(f"/bugs/{bug_id}")

    assert first_delete_response.status_code == 204

    get_response = client.get(f"/bugs/{bug_id}")

    assert get_response.status_code == 404

    second_delete_response = client.delete(f"/bugs/{bug_id}")

    assert second_delete_response.status_code == 404

bug_data_title_too_short = {
                            "title": "aa",
                            "description": "Valid bug description",
                            "priority": "Low" 
                            }

bug_data_description_too_short = {
                            "title": "Valid bug title",
                            "description": "aa",
                            "priority": "Low" 
                                }

bug_data_invalid_bug_priority = {
                            "title": "Valid bug title",
                            "description": "Valid bug description",
                            "priority": "Invalid bug priority" 
                                }

@pytest.mark.parametrize("bug_data",
                        [
                            bug_data_title_too_short,
                            bug_data_description_too_short, 
                            bug_data_invalid_bug_priority
                        ],
                        ids = ["short-title", "short-description", "invalid-priority"]
                    )
def test_create_bug_invalid_data(bug_data):

    post_response = client.post("/bugs", json = bug_data)

    assert post_response.status_code == 422

    get_response = client.get("/bugs")

    assert get_response.status_code == 200
    assert get_response.json() == []

def test_update_bug_invalid_priority(created_bug, sample_bug_data):

    updated_priority = "Critical"
        
    bug_id = created_bug["id"]

    patch_response = client.patch(f"/bugs/{bug_id}", json = {"priority": updated_priority})

    assert patch_response.status_code == 422

    get_response = client.get(f"/bugs/{bug_id}")

    assert get_response.status_code == 200

    fetched_bug = get_response.json()

    assert fetched_bug["title"] == sample_bug_data["title"]
    assert fetched_bug["description"] == sample_bug_data["description"]
    assert fetched_bug["priority"] == sample_bug_data["priority"]

def test_update_nonexistent_bug():

    patch_response = client.patch("/bugs/9999999999", json = {"priority": "Low"})

    assert patch_response.status_code == 404
    assert patch_response.json() == {"detail": "Item not found"}

def test_get_multiple_bugs():

    first_bug_data = {
        "title": "First Bug Title",
        "description": "First Bug Description",
        "priority": "Low"
    }

    second_bug_data = {
        "title": "Second Bug Title",
        "description": "Second Bug Description",
        "priority": "Low"
    }

    first_post_response = client.post("/bugs", json = first_bug_data)
    second_post_response = client.post("/bugs", json = second_bug_data)

    assert first_post_response.status_code == 201
    assert second_post_response.status_code == 201

    get_response = client.get("/bugs")

    assert get_response.status_code == 200

    fetched_bugs = get_response.json()

    assert len(fetched_bugs) == 2    

    fetched_ids = []

    for bug in fetched_bugs:
        fetched_ids.append(bug["id"])

    first_id = first_post_response.json()["id"]
    second_id = second_post_response.json()["id"]

    assert first_id in fetched_ids
    assert second_id in fetched_ids