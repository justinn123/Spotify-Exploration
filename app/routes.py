from flask import redirect, request, session, url_for, render_template, current_app as app
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import Config

def get_spotify_oauth():
    cache_handler = FlaskSessionCacheHandler(session)
    return SpotifyOAuth(
        client_id=Config.SPOTIPY_CLIENT_ID,
        client_secret=Config.SPOTIPY_CLIENT_SECRET,
        redirect_uri=Config.SPOTIPY_REDIRECT_URI,
        scope=Config.SPOTIPY_SCOPE,
        cache_handler=cache_handler,
        show_dialog=True
    )

# def get_spotify_client():
#     token_info = session.get('token_info', None)
#     if not token_info:
#         return None
#     sp_oauth = get_spotify_oauth()
#     if sp_oauth.is_token_expired(token_info):
#         token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
#         session['token_info'] = token_info
#     return Spotify(auth=token_info['access_token'])

# @app.route('/')
# def home():
#     if not session.get('token_info'):
#         sp_oauth = get_spotify_oauth()
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
#     return redirect(url_for('index'))

# @app.route('/callback')
# def callback():
#     error = request.args.get('error')
#     if error:
#         app.logger.error(f"OAuth Error: {error}")
#         return redirect(url_for('error_page'))

#     code = request.args.get('code')
#     if not code:
#         return redirect(url_for('error_page'))

#     try:
#         sp_oauth = get_spotify_oauth()
#         token_info = sp_oauth.get_access_token(code)
#         session['token_info'] = token_info
#         print("TOKEN INFO:", token_info)
#         return redirect(url_for('index'))
#     except Exception as e:
#         app.logger.error(f"Error during token exchange: {str(e)}")
#         return redirect(url_for('error_page'))

def get_spotify_client():
    refresh_token = Config.STATIC_REFRESH_TOKEN
    try:
        sp_oauth = get_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(refresh_token)

        # Use the freshly generated access token
        return Spotify(auth=token_info['access_token'])

    except Exception as e:
        app.logger.error(f"Error getting Spotify client: {e}")
        return None


@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/callback')
def callback():
    return redirect(url_for('index'))

@app.route('/error_page')
def error_page():
    return render_template('error.html')

@app.route('/home')
def index():
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('error_page'))
    current_playing = sp.current_user_playing_track()
    if current_playing is None or current_playing.get('item') is None or current_playing['item'].get('is_local'):
        current_playing = {
            'item': {
                'name': 'No song currently playing',
                'album': {'images': [{'url': sp.current_user()['images'][0]['url']}]},
                'artists': [{'name': 'No artist'}]
            }
        }
    return render_template('index.html', username=sp.current_user()['display_name'], 
                           current_playing=current_playing)

@app.route('/TopSongs')
def get_top_songs():
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('home'))
    top_songs = sp.current_user_top_tracks(time_range='short_term', limit=10)
    return render_template('top_songs.html', top_songs=top_songs)

@app.route('/Playlists')
def get_playlists():
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('home'))
    playlists = sp.current_user_playlists()
    return render_template('playlists.html', playlists=playlists, 
                           current_user=sp.current_user())