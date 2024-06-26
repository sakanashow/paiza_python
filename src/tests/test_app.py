import pytest
from app import app, db, User, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_register(client):
    response = client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200

def test_login(client):
    client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200

def test_add_task(client):
    # Register and login a new user
    client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Add a new task
    task_data = {
        'title': 'Test Task',
        'deadline': '2023-06-20',
        'details': 'Test details',
        'status': '未着手'
    }
    response = client.post('/tasks', json=task_data)
    assert response.status_code == 200

def test_edit_task(client):
    # Register and login a new user
    client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Add a new task
    task_data = {
        'title': 'Test Task',
        'deadline': '2023-06-20',
        'details': 'Test details',
        'status': '未着手'
    }
    response = client.post('/tasks', json=task_data)
    task_id = response.get_json()

    # Edit the task
    updated_task_data = {
        'title': 'Updated Task',
        'deadline': '2023-06-21',
        'details': 'Updated details',
        'status': '進行中'
    }
    response = client.put(f'/tasks/{task_id}', json=updated_task_data)
    assert response.status_code == 200

def test_delete_task(client):
    # Register and login a new user
    client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Add a new task
    task_data = {
        'title': 'Test Task',
        'deadline': '2023-06-20',
        'details': 'Test details',
        'status': '未着手'
    }
    response = client.post('/tasks', json=task_data)
    task_id = response.get_json()

    # Delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204

def test_task_list(client):
    # Register and login a new user
    client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Add a new task
    task_data = {
        'title': 'Test Task',
        'deadline': '2023-06-20',
        'details': 'Test details',
        'status': '未着手'
    }
    client.post('/tasks', json=task_data)

    # Fetch the task list
    response = client.get('/tasks')
    assert response.status_code == 200
