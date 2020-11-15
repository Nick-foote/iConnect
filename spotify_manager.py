from credentials.spotify_cred import SpotifyAuth


class SpotifyManager:
    """Interaction with Spotify API"""

    def __init__(self, username):
        self._username = username

    def user_query(self):
        """Checks to see if the Spotify Username Exists"""
        SpotifyAuth.user_playlists(self._username)
        print(f"SUCCESS: Spotify Username '{self._username}' Exists")

    def playlist_retrieval(self):
        """Retrieves the most recent user playlists values to open in the Spotify App
        """
        data = SpotifyAuth.user_playlists(self._username)
        playlist_name = data['items'][0]['name']
        _, _, playlist_uri = data['items'][0]['uri'].split(":")

        return playlist_name, playlist_uri


# example playlist string = "spotify:playlist:3OOQfwgFyfwwglK3bv6HOM"