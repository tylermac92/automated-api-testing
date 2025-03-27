import pytest
import json
from app import app, items

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Reset the in-memory items list for each test run
    original_items = items.copy()
    with app.test_client() as client:
        yield client
    # Restore the original state after tests if needed
    items.clear()
    items.extend(original_items)

def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Expect initial items to be present
    assert len(data) >= 2

def test_get_single_item_success(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1

def test_get_single_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404

def test_create_item(client):
    new_item = {"name": "Item Three", "description": "The third item"}
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == new_item["name"]
    assert "id" in data

def test_update_item(client):
    update_data = {"name": "Updated Item One", "description": "Updated description"}
    response = client.put("/items/1", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == update_data["name"]

def test_delete_item(client):
    response = client.delete("/items/1")
    assert response.status_code == 200
    # Verify item is removed
    follow_up = client.get("/items/1")
    assert follow_up.status_code == 404