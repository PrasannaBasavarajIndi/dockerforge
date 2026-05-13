import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Task' in response.data

def test_add_task(client):
    # Ensure starting clean or knowing state
    initial_count = len(tasks)
    response = client.post('/add', data={'title': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert len(tasks) == initial_count + 1
    assert any(t['title'] == 'Test Task' for t in tasks)

def test_delete_task(client):
    # Add a task to ensure there's something to delete
    client.post('/add', data={'title': 'Delete Me'})
    task_id_to_delete = tasks[-1]['id']
    
    # Delete the task
    response = client.post(f'/delete/{task_id_to_delete}', follow_redirects=True)
    assert response.status_code == 200
    assert not any(t['id'] == task_id_to_delete for t in tasks)
