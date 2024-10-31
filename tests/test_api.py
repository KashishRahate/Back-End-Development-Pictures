import pytest
import json
from flask import Flask
from app import app  # Adjust based on where your Flask app is located

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "OK"}

def test_count(client):
    response = client.get('/count')
    assert response.status_code == 200
    assert "length" in response.json

def test_data_contains_10_pictures(client):
    response = client.get('/count')
    assert response.json["length"] == 10  # Assuming you have 10 pictures

def test_get_picture(client):
    response = client.get('/picture/1')
    assert response.status_code == 200
    assert "id" in response.json

def test_get_pictures_check_content_type_equals_json(client):
    response = client.get('/picture')
    assert response.content_type == "application/json"

def test_get_picture_by_id(client):
    response = client.get('/picture/1')
    assert response.status_code == 200

def test_pictures_json_is_not_empty(client):
    response = client.get('/picture')
    assert len(response.json) > 0

def test_post_picture(client):
    picture_data = {
        "id": 200,
        "pic_url": "http://dummyimage.com/230x100.png/dddddd/000000",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "11/2/2030"
    }
    response = client.post('/picture', json=picture_data)
    assert response.status_code == 201
    print(f"tests/test_api.py::test_post_picture {response.json} PASSED")

def test_post_picture_duplicate(client):
    picture_data = {
        "id": 200,
        "pic_url": "http://dummyimage.com/230x100.png/dddddd/000000",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "11/2/2030"
    }
    response = client.post('/picture', json=picture_data)
    assert response.status_code == 302
    print(f"tests/test_api.py::test_post_picture_duplicate {response.json} PASSED")
