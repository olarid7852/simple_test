import os
import pytest
from fastapi.testclient import TestClient
from shutil import copyfile

os.environ['ENV'] = 'test'

from config import get_current_config
from main import app

print(os.environ)

client = TestClient(app)


@pytest.fixture(autouse=True)
def create_temp_db():
    try:
        os.remove(get_current_config().DATABASE_NAME)
    except:
        pass
    try:
        copyfile('db/test.db', get_current_config().DATABASE_NAME)
    except:
        pass
    yield
    try:
        os.remove(get_current_config().DATABASE_NAME)
    except:
        pass


def test_get_player_correct_id():
    response = client.get("/player/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "age": 25,
        "name": "Patrick Mahomes",
        "team_id": 1
    }


def test_get_player_wrong_id():
    response = client.get("/player/100")
    assert response.status_code == 404


def test_delete_player_correct_id():
    response = client.delete("/player/100")
    assert response.status_code == 404


def test_delete_player_wrong_id():
    response = client.delete("/player/5")
    assert response.status_code == 204

    response = client.get("/player/5")
    assert response.status_code == 404


def test_update_player_wrong_id():
    response = client.put("/player/100", json={
        'age': 20,
        'name': 'new name',
        'team_id': 1
    })
    assert response.status_code == 404


def test_update_player_correct_id():
    response = client.put("/player/10", json={
        'age': 20,
        'name': 'new name',
        'team_id': 1
    })
    assert response.status_code == 200

    response = client.get("/player/10")
    assert response.status_code == 200
    assert response.json() == {
        "id": 10,
        "age": 20,
        "name": "new name",
        "team_id": 1
    }


def test_update_player_invalid_data_id():
    # Name too short
    response = client.put("/player/10", json={
        'age': 20,
        'name': 'new',
        'team_id': 1
    })
    assert response.status_code == 422

    # Age too low
    response = client.put("/player/10", json={
        'age': 0,
        'name': 'new',
        'team_id': 1
    })
    assert response.status_code == 422