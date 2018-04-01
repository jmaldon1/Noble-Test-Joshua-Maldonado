import os
from flask import Flask
from config import config
import eventlet
eventlet.monkey_patch()
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

bootstrap = Bootstrap()
#db = SQLAlchemy()

app = Flask(__name__)

#socketio
socketio = SocketIO(app)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "orderbooks.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
socketio = SocketIO(app)

from app.models import models

def create_app(config_name):
	app.config.from_object(config[config_name])

	# Register our blueprints
	from .default import default as default_blueprint
	app.register_blueprint(default_blueprint)

	app.config['SECRET_KEY'] = 'noble test secret'

	# Initialize any extensions we are using
	bootstrap.init_app(app)
	# db.init_app(app)
	# print(db)



	return app