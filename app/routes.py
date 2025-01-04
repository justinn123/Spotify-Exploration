from flask import redirect, request, session, url_for, render_template, current_app as app
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=app.config['SPOTIPY_CLIENT_ID'],
    client_secret=app.config['SPOTIPY_CLIENT_SECRET'],
    redirect_uri=app.config['SPOTIPY_REDIRECT_URI'],
    scope=app.config['SPOTIPY_SCOPE'],
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

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
    return redirect(url_for('get_playlists'))

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
    return render_template('index.html', top_songs=top_songs)

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
    return render_template('playlists.html', playlists=playlists)