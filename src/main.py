import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ba84285e9f8e46fba2207ec5dac8adac",
                                                           client_secret="e0328980b88b48d582ab1ea39e15aac1",
                                                           redirect_uri="http://localhost:3000",
                                                           scope = "user-library-read"))

playlists = sp.user_playlists('qmf0k6enaxlvtpossw58c6ql5') # Raging_Azian's playlists
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s" % (i + 1 + playlists['offset'], playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None