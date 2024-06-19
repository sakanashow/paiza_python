from app import db, User, app

def create_user(email, password):
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_user('test@example.com', 'password')
        print("User created: test@example.com / password")
