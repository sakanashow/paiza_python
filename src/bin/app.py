from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

# プロジェクトのルートディレクトリを定義
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    details = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='未着手')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "ログイン失敗"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    events = []
    for task in tasks:
        events.append({
            'id': task.id,
            'title': task.title,
            'start': task.deadline.strftime('%Y-%m-%d'),
            'details': task.details
        })
    return jsonify(events)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            'id': task.id,
            'title': task.title,
            'deadline': task.deadline.strftime('%Y-%m-%d'),
            'details': task.details,
            'status': task.status
        })
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def manage_tasks():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%d').date(),
        details=data['details'],
        status=data['status'],
        user_id=session['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.id)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.deadline = datetime.strptime(data.get('deadline', task.deadline.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    task.details = data.get('details', task.details)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'id': task.id})

@app.route('/tasks/<int:task_id>/deadline', methods=['PUT'])
def update_task_deadline(task_id):
    task = Task.query.get(task_id)
    data = request.get_json()
    task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
    db.session.commit()
    return jsonify({'id': task.id})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@app.route('/completed_tasks')
def completed_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id, status='完了').all()
    return render_template('completed_tasks.html', tasks=tasks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
