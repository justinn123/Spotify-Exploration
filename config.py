import os

class Config:
    SECRET_KEY = os.urandom(64)
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"
    SPOTIPY_SCOPE = 'user-top-read user-library-read playlist-read-private'