from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# -- Spotify API info below --
client_id = "####"      
client_secret = "####"


redirect_uri = 'http://localhost:7777/callback'
scope = 'user-library-read'

SpotifyAuth = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))
