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

def test_get_bugs():

    response = client.get("/bugs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

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
