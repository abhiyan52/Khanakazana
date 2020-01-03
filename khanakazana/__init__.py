''' 
Name: __init__.py 
Description: Main File of the flask app which configures the application and registers all blueprints
author: abhiyan timilsina
'''

from datetime import timedelta, datetime
import os
import time
from flask import Flask, request, session, flash, g
from khanakazana.api.functions.Database import Database
from flask_login import LoginManager, login_required, login_user
from khanakazana.api.functions.Models import Users
from khanakazana.api.routes import api_blueprint
from khanakazana.auth.routes import auth_blueprint
from khanakazana.views.controller import views_blueprint
from flask_uploads import UploadSet, configure_uploads, DATA

app = Flask(__name__, static_folder='./views/static')
app.config['SECRET_KEY'] = os.urandom(26)
login_manager = LoginManager()
login_manager.init_app(app)
files = UploadSet('csvfiles', DATA)
app.config['UPLOADED_CSVFILES_DEST'] = 'static/files'
configure_uploads(app, files)
app.files = files


@login_manager.user_loader
def load_user(user_id):
    d = Database()
    user = d.session.query(Users).get(user_id)
    return user


@app.before_request
def logger():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    g.user = 'anno'
    g.user_type = None
    if 'username' in session:
        g.user = session['username']
        g.user_type = session['user_type']
    print(f'''[{request.method}]Request made at time {datetime.now()} for url {request.url}''')

# Registering blueprints
app.register_blueprint(api.routes.api_blueprint, url_prefix='/api/v1')     
app.register_blueprint(auth.routes.auth_blueprint, url_prefix='/auth')
app.register_blueprint(views.controller.views_blueprint, url_prefix='/')


    
