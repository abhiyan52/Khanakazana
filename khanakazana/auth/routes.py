from flask import Blueprint, request, jsonify, session, g, redirect, flash
from khanakazana.api.functions.Models import Users
from khanakazana.api.functions.Database import Database
import hashlib
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.before_request
def generate_datbase():
    if 'db_session' not in g:
        g.session = Database().session


@auth_blueprint.route('/login', methods=['POST'])
def validate_user():
    g.session.commit()
    username = request.form.get('username')
    password = request.form.get('password')
    db_password = None
    user_type = 0
    user = g.session.query(Users).filter(Users.username == username).first()
    if user is not None:
        db_password = user.password

    if db_password is not None and hashlib.sha256(password.encode('utf-8')).hexdigest() == db_password:
        session['username'] = user.username
        session['user_type'] = user.user_type
        login_user(user, remember=True)
        return jsonify({'status': 'sucessful', 'type': user_type})
    else:
        return jsonify({'status': 'unsucessful'})


@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    g.session.commit()
    email = request.form.get('email')
    username = request.form.get('username')
    password = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest() 
    contact_no = request.form.get('contact')
    address = request.form.get('address')
    name = request.form.get('name')
    user_type = 0
    user = Users(username, password, email, name, address, contact_no)
    try:
        g.session.add(user)
        g.session.commit()
        return user.username
    except:
        return 'hello'


@auth_blueprint.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    g.session.commit()
    user = g.session.query(Users).filter(Users.username == session['username']).first()
    login_user(user)
    session.clear()
    if request.method == 'POST':
        return jsonify({'status': 200, 'message': 'Logout Successful'})
    flash({'type': 'fail', 'message': 'You are now logged out'})
    return redirect('/')


def validate_unique_username(username):
    d = Database()
    if d.session.query(Users).filter(Users.username == username).first() is not None:
        return False
    else:
        return True


