from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
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
    
    user_id = session['user_id']
    user = db.session.get(User, user_id)  # 修正箇所
    
    return render_template('index.html', user=user)


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
            flash('ログイン失敗', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/task_form')
@app.route('/task_form/<int:task_id>')
def task_form(task_id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = db.session.get(Task, task_id) if task_id else None  # 修正箇所
    return render_template('task_form.html', task=task)

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
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
    else:
        user_id = session['user_id']
        tasks = Task.query.filter_by(user_id=user_id).filter(Task.status != '完了').all()
        return jsonify([{
            'id': task.id,
            'title': task.title,
            'deadline': task.deadline.strftime('%Y-%m-%d'),
            'details': task.details,
            'status': task.status
        } for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def task_detail(task_id):
    task = db.session.get(Task, task_id)  # 修正箇所
    if request.method == 'GET':
        return jsonify({
            'id': task.id,
            'title': task.title,
            'deadline': task.deadline.strftime('%Y-%m-%d'),
            'details': task.details,
            'status': task.status
        })
    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
        task.details = data['details']
        task.status = data['status']
        db.session.commit()
        return jsonify(task.id)
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return '', 204

@app.route('/tasks/<int:task_id>/deadline', methods=['PUT'])
def update_task_deadline(task_id):
    task = db.session.get(Task, task_id)  # 修正箇所
    data = request.get_json()
    task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
    db.session.commit()
    return jsonify(task.id)

@app.route('/completed_tasks')
def completed_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id, status='完了').all()
    return render_template('completed_tasks.html', tasks=tasks)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に登録されています', 'danger')
            return redirect(url_for('register'))
        new_user = User(email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        flash('新規登録が完了しました。ログインしてください', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
