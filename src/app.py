import os

from flask import Flask, redirect, request, session, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

from credentials import client_id, client_secret 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

redirect_uri = "http://localhost:8000/callback"
scope = 'user-top-read'

cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager = sp_oauth)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_top_songs'))

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return redirect(url_for('error_page'))
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_top_songs'))

@app.route('/error_page')
def error_page():
    html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Error</title></head><body><h1>There was an error</h1></body></html>'
    return html

@app.route('/get_top_songs')
def get_top_songs():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    top_songs = sp.current_user_top_tracks()
    html_content = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Top Songs</title></head><body>'
    html_content += '<h1>Your Top Songs</h1><ul>'
    
    for item in top_songs['items']:
        html_content += f'<li>{item["name"]} by {item["artists"][0]["name"]}</li>'
    
    html_content += '</ul></body></html>'
    
    return html_content

if __name__ == '__main__':
    app.run(port = 8000, debug=True)




