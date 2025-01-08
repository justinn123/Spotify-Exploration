from flask import Flask
from flask_socketio import SocketIO
from config import Config

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from . import routes

    socketio.init_app(app)
    return app