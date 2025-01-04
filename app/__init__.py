import os
from flask import Flask
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from credentials import client_id, client_secret

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(64)
    app.config['SPOTIPY_CLIENT_ID'] = client_id
    app.config['SPOTIPY_CLIENT_SECRET'] = client_secret
    app.config['SPOTIPY_REDIRECT_URI'] = "http://localhost:5000/callback"
    app.config['SPOTIPY_SCOPE'] = 'user-top-read user-library-read playlist-read-private'

    with app.app_context():
        from . import routes

    return app