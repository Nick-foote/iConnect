from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

### Hard-coded in
client_id = "9f660f6108d44080b18f15b3eda4a432"
client_secret = "8221d6445e064eeebb8a2d7439f0aa58"
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-library-read'

SpotifyAuth = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))
