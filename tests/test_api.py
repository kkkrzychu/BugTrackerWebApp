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