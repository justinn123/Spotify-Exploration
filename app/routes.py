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
    return redirect(url_for('index'))

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return redirect(url_for('error_page'))
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('index'))

@app.route('/error_page')
def error_page():
    return render_template('error.html')

@app.route('/home')
def index():
    current_playing = sp.current_user_playing_track()
    if current_playing is None or current_playing.get('item') is None:
        current_playing = {
            'item': {
                'name': 'No song currently playing',
                'album': {'images': [{'url': 'https://cdn.chatfai.com/public_characters/D2ubMNsMyaZHvfQEwcz4uuOir2P2/f65ad656-1a0b-4006-b250-80a2dee62270ab67616d0000b2733aecad4bb7cbd784f92d2f9a.jpeg'}]},
                'artists': [{'name': 'No artist'}]
            }
        }
    return render_template('index.html', username=sp.current_user()['display_name'], 
                           current_playing=current_playing)

@app.route('/TopSongs')
def get_top_songs():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    top_songs = sp.current_user_top_tracks()
    return render_template('top_songs.html', top_songs=top_songs)

@app.route('/Playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
    current_playing = sp.current_user_playing_track()
    return render_template('playlists.html', playlists=playlists, 
                           current_user = sp.current_user())