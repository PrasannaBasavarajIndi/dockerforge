import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'DockerForge' in response.data or b'Task' in response.data

def test_add_task(client):
    response = client.post('/add', data={'title': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_delete_task(client):
    # Add a task to ensure there's something to delete
    client.post('/add', data={'title': 'Delete Me Task'}, follow_redirects=True)
    
    # Get the homepage to find the ID (or just delete ID 1 since it's the only one in testing context usually)
    # Since it's a global counter in app, the ID could be anything. 
    # But wait, how do we get the ID? We can just delete the task by submitting the delete endpoint.
    # To keep the test simple without scraping HTML, we can just access app.tasks
    import app as myapp
    task_id_to_delete = myapp.tasks[-1]['id']
    
    # Delete the task
    response = client.post(f'/delete/{task_id_to_delete}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Delete Me Task' not in response.data
