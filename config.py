import os
from credentials import client_id, client_secret

class Config:
    SECRET_KEY = os.urandom(64)
    SPOTIPY_CLIENT_ID = client_id
    SPOTIPY_CLIENT_SECRET = client_secret
    SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"
    SPOTIPY_SCOPE = '''user-top-read user-library-read 
    playlist-read-private 
    user-read-playback-state 
    user-modify-playback-state
    user-read-currently-playing'''