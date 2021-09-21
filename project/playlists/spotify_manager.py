import logging
from django.conf import settings
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from playlists.models import Playlist


SOCIAL_AUTH_SPOTIFY_KEY = settings.SOCIAL_AUTH_SPOTIFY_KEY
SOCIAL_AUTH_SPOTIFY_SECRET = settings.SOCIAL_AUTH_SPOTIFY_SECRET
SPOTIFY_REDIRECT_URI = settings.SOCIAL_REDIRECT_URL
SOCIAL_AUTH_SPOTIFY_SCOPE = settings.SOCIAL_AUTH_SPOTIFY_SCOPE


logger = logging.getLogger(__name__) 


class SpotifyManager:
    """Interaction with Spotify API"""

    def __init__(self, user):
        self.user = user
        self.SpotifyAuth = Spotify(auth_manager=SpotifyOAuth(
            client_id=SOCIAL_AUTH_SPOTIFY_KEY,
            client_secret=SOCIAL_AUTH_SPOTIFY_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SOCIAL_AUTH_SPOTIFY_SCOPE)
            )

    def user_query(self):
        """Checks to see if the Spotify Username Exists"""
        try:
            self.SpotifyAuth.user_playlists(self.username)
            return True
        except:
            logger.error(f"User {self.username!r} not found on Spotify")
            return False

    def playlist_retrieval(self):
        """Retrieves the most recent user playlists values to open in the Spotify App.
        Example playlist string = "spotify:playlist:3OOQfwgFyfwwglK3bv6HOM"
        """
        data = self.SpotifyAuth.user_playlists(self._username)
        playlist_name = data['items'][0]['name']
        _, _, playlist_uri = data['items'][0]['uri'].split(":")

        return playlist_name, playlist_uri


    def upload_playlist(self, location=None):
        playlist_name, playlist_uri = self.playlist_retrieval()

        # only wanting each user's playlist uploaded once
        try:
            Playlist.objects.get_or_create(
                user=self.user,
                name = playlist_name,
                spotify_uri = playlist_uri,
                location=location,
            )
        except ValueError:
            logger.error(f"Playlist Creation Failed - User {self.user.username!r}")

        return