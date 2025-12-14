import pytest
import sys
import os

# Add the backend directory to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import Conference, ConferenceStatus, ConferenceLevel
from datetime import datetime

@pytest.fixture
def run_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(run_app):
    return run_app.test_client()

@pytest.fixture
def runner(run_app):
    return run_app.test_cli_runner()

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello from Flask backend!"}

def test_get_conferences_empty(client):
    response = client.get('/api/conferences')
    assert response.status_code == 200
    assert response.json == []

def test_create_conference(client):
    data = {
        "title": "Test Conf",
        "status": "Idées",
        "assignee": "User A",
        "date": datetime(2025, 12, 25, 10, 0, 0).isoformat(),
        "link_doc": "http://doc.com",
        "address": "Paris",
        "level": "expert"
    }
    response = client.post('/api/conferences', json=data)
    assert response.status_code == 201
    assert response.json['title'] == "Test Conf"
    assert response.json['status'] == "Idées"
    assert response.json['level'] == "expert"

def test_create_conference_minimal(client):
    data = {
        "title": "Minimal Conf"
    }
    response = client.post('/api/conferences', json=data)
    assert response.status_code == 201
    assert response.json['title'] == "Minimal Conf"
    assert response.json['status'] == "Idées" # Default
    assert response.json['level'] == "easy" # Default

def test_create_conference_invalid_status(client):
    data = {
        "title": "Invalid Conf",
        "status": "InvalidStatus"
    }
    response = client.post('/api/conferences', json=data)
    assert response.status_code == 400
    assert "not a valid ConferenceStatus" in response.json['error']

def test_create_conference_invalid_level(client):
    data = {
        "title": "Invalid Level",
        "level": "mega-hard"
    }
    response = client.post('/api/conferences', json=data)
    assert response.status_code == 400
    assert "not a valid ConferenceLevel" in response.json['error']

def test_create_conference_missing_title(client):
    data = {"status": "Idées"} # Missing title
    response = client.post('/api/conferences', json=data)
    assert response.status_code == 400
    assert "Missing field: 'title'" in response.json['error']

def test_update_conference(client):
    # Create first
    data = {"title": "Update Me"}
    create_res = client.post('/api/conferences', json=data)
    conf_id = create_res.json['id']

    # Update
    update_data = {
        "title": "Updated",
        "status": "Terminé",
        "level": "mid"
    }
    response = client.put(f'/api/conferences/{conf_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['title'] == "Updated"
    assert response.json['status'] == "Terminé"
    assert response.json['level'] == "mid"

def test_update_all_fields(client):
    c = Conference(title="Orig", status=ConferenceStatus.IDEES)
    db.session.add(c)
    db.session.commit()
    
    update_data = {
        "title": "New Title",
        "status": "Contacté",
        "assignee": "New Assignee",
        "date": datetime(2025, 2, 2).isoformat(),
        "link_doc": "http://new.doc",
        "address": "New Addr",
        "level": "expert"
    }
    response = client.put(f'/api/conferences/{c.id}', json=update_data)
    assert response.status_code == 200
    d = response.json
    assert d['assignee'] == "New Assignee"
    assert d['link_doc'] == "http://new.doc"
    assert d['address'] == "New Addr"


def test_update_conference_invalid_id(client):
    response = client.put('/api/conferences/999', json={"title": "Nope"})
    assert response.status_code == 404

def test_update_conference_invalid_data(client):
    # Create first
    data = {"title": "Update Me Fail"}
    create_res = client.post('/api/conferences', json=data)
    conf_id = create_res.json['id']

    # Update
    response = client.put(f'/api/conferences/{conf_id}', json={"status": "BadStatus"})
    assert response.status_code == 400

def test_delete_conference(client):
    # Create first
    data = {"title": "Delete Me"}
    create_res = client.post('/api/conferences', json=data)
    conf_id = create_res.json['id']

    # Delete
    response = client.delete(f'/api/conferences/{conf_id}')
    assert response.status_code == 204

    # Verify gone
    get_res = client.get('/api/conferences')
    assert len(get_res.json) == 0

def test_delete_conference_invalid_id(client):
    response = client.delete('/api/conferences/999')
    assert response.status_code == 404

def test_conference_model_methods():
    c = Conference(
        title="Test", 
        date=datetime(2025, 1, 1),
        status=ConferenceStatus.IDEES,
        level=ConferenceLevel.EASY
    )
    d = c.to_dict()
    assert d['title'] == "Test"
    assert d['date'] == "2025-01-01T00:00:00"
