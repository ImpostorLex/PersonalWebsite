from flask import Blueprint, url_for

bp = Blueprint('posts', __name__)


from app.posts import routes


