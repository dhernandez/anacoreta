from flask import Blueprint

bp = Blueprint('update', __name__)

from . import routes
