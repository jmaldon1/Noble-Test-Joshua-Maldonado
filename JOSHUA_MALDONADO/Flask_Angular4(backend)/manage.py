import os
from app import create_app
from flask.ext.script import Manager
from flask_sqlalchemy import SQLAlchemy
from app import socketio

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
	socketio.run(app)