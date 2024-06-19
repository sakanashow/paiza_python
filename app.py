from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Task:
    def __init__(self, title, deadline, details, status="未着手"):
        self.title = title
        self.deadline = deadline
        self.details = details
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "details": self.details,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data["deadline"],
            data["details"],
            data.get("status", "未着手")
        )

tasks = []
users = {"test@example.com": "password"}  # サンプルユーザー

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', tasks=[task.to_dict() for task in tasks])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('index'))
        else:
            return "ログイン失敗"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/task_form')
@app.route('/task_form/<int:index>')
def task_form(index=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    task = tasks[index] if index is not None else None
    return render_template('task_form.html', task=task, index=index)

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        data = request.get_json()
        task = Task.from_dict(data)
        tasks.append(task)
        save_tasks()
        return jsonify(task.to_dict())
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:index>', methods=['PUT', 'DELETE'])
def update_task(index):
    if request.method == 'PUT':
        data = request.get_json()
        task = Task.from_dict(data)
        tasks[index] = task
        save_tasks()
        return jsonify(task.to_dict())
    elif request.method == 'DELETE':
        tasks.pop(index)
        save_tasks()
        return '', 204

@app.route('/save_task', methods=['POST'])
def save_task():
    data = request.form
    task_data = {
        'title': data['title'],
        'deadline': data['deadline'],
        'details': data['details'],
        'status': data['status']
    }
    if 'index' in data and data['index']:
        index = int(data['index'])
        tasks[index] = Task.from_dict(task_data)
    else:
        tasks.append(Task.from_dict(task_data))
    save_tasks()
    return redirect(url_for('index'))

def save_tasks():
    with open('tasks.json', 'w') as file:
        json.dump([task.to_dict() for task in tasks], file)

def load_tasks():
    global tasks
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            tasks_data = json.load(file)
            tasks = [Task.from_dict(task_data) for task_data in tasks_data]

if __name__ == '__main__':
    load_tasks()
    app.run(debug=True)
