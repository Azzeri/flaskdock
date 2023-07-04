from flask import session
from app.database import get_db_instance, User

db = get_db_instance()


def login(request):
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['username'] = username
        return True
    else:
        return False


def register(request):
    username = request.form['username']
    password = request.form['password']
    interests = get_form_interests(request.form)

    if User.query.filter_by(username=username).first():
        return False

    new_user = User(username=username, interests=interests)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    session['username'] = username

    return True


def logout():
    session.pop('username', None)


def get_form_interests(form):
    interests = ''
    for input in form:
        if input.startswith('i_'):
            interests += form[input] + '|'
    interests = interests[:-1]

    return interests
