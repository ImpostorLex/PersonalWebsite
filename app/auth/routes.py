from app.auth import bp
from flask import render_template, redirect, url_for, flash, request, current_app, request
from app.extensions import db, ic, current_user, login_user, logout_user
from app.models.auth import Admin
import hashlib
import logging

def hash_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()


@bp.route('/secret_login', methods=['POST', 'GET'])
def login():

    form = ""

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        hashed_pass = hash_sha256(password)
        
        is_user_exists = Admin.query.filter_by(username=username, password=hashed_pass).first()
        
        if not is_user_exists:
            
            flash("User not found please try again!")
            # Get the client's IP address
            client_ip = request.remote_addr
            current_app.logger.info(f"ip_addr: {client_ip}, msg: Login Attempt Failed, Username: {username}")

        else:
            login_user(is_user_exists)
            current_app.logger.info(f"ip_addr {client_ip}, msg: Login Attempt Succesful, Username: {username}")
            return redirect(url_for('main.index'))


    return render_template('auth/login.html', form=form)


@bp.route('/logout', methods=['POST', 'GET'])
def logout():

    logout_user()
    return redirect(url_for('main.index'))