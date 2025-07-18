from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

import os



class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")  # "dev" fallback only for dev/testing
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    STATIC_ACCESS_TOKEN = os.getenv("STATIC_ACCESS_TOKEN") 
    STATIC_REFRESH_TOKEN = os.getenv("STATIC_REFRESH_TOKEN")
    #SPOTIPY_REDIRECT_URI = "https://spotify-exploration.vercel.app/callback"
    SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"
    SPOTIPY_SCOPE = '''user-top-read user-library-read 
    playlist-read-private 
    user-read-playback-state 
    user-modify-playback-state
    user-read-currently-playing'''
    
#pls update