from flask import Blueprint
main = Blueprint('main', __name__)
from .errors import *
from .views import *

