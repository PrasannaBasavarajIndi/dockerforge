import pytest
import json
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add_task(client):
    response = client.post('/api/tasks', json={'title': 'Test API Task'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test API Task'
    assert 'id' in data


def test_get_tasks(client):
    client.post('/api/tasks', json={'title': 'Test API Task 1'})
    client.post('/api/tasks', json={'title': 'Test API Task 2'})

    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] == 'Test API Task 1'


def test_delete_task(client):
    res = client.post('/api/tasks', json={'title': 'Delete Me Task'})
    task_id = json.loads(res.data)['id']

    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200

    response_get = client.get('/api/tasks')
    data = json.loads(response_get.data)
    assert len(data) == 0
