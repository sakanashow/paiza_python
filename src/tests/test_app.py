import pytest
import os
import sys

# appモジュールのインポートパスを設定
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bin')))

from app import app, db, User, Task
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_register(client):
    response = client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert '新規登録が完了しました。ログインしてください' in response.get_data(as_text=True)

def test_login(client):
    client.post('/register', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'ようこそ' in response.get_data(as_text=True)

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
    task_id = response.get_json()
    
    # Verify the task was added
    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task is not None
        assert task.title == 'Test Task'
        assert task.deadline == datetime.strptime('2023-06-20', '%Y-%m-%d').date()
        assert task.details == 'Test details'
        assert task.status == '未着手'

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
    
    # Verify the task was updated
    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task is not None
        assert task.title == 'Updated Task'
        assert task.deadline == datetime.strptime('2023-06-21', '%Y-%m-%d').date()
        assert task.details == 'Updated details'
        assert task.status == '進行中'

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
    
    # Verify the task was deleted
    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task is None
