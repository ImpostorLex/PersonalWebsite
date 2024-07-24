# The init.py file make this importing of bp possible.
from app.main import bp
from flask import render_template
from flask_login import current_user


@bp.route('/')
def index():
    
    is_authenticated =  current_user.is_authenticated
    return render_template('index.html', is_authenticated=is_authenticated)
