from flask import Blueprint, render_template
from config import Config

default = Blueprint('cast', __name__, static_folder=Config.STATIC_FOLDER, static_url_path='')
from . import routes