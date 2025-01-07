from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(64)
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = "https://spotify-exploration-1j6strk9o-ragingazians-projects.vercel.app/callback"
    SPOTIPY_SCOPE = '''user-top-read user-library-read 
    playlist-read-private 
    user-read-playback-state 
    user-modify-playback-state
    user-read-currently-playing'''