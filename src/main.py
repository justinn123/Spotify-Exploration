import spotipy
from spotipy.oauth2 import SpotifyOAuth


playlists = sp.user_playlists('qmf0k6enaxlvtpossw58c6ql5') # Raging_Azian's playlists
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s" % (i + 1 + playlists['offset'], playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
