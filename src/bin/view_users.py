from bin.app import db, User, app

def view_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f'ID: {user.id}, Email: {user.email}, Password Hash: {user.password_hash}')

if __name__ == '__main__':
    view_users()
