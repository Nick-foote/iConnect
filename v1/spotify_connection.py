import database
from scipy import spatial
import numpy as np
import webbrowser
from geopy import distance

from spotify_manager import SpotifyManager


class SpotifyConnection:
    """Gathers user's public Spotify playlists with the Spotify API"""

    def __init__(self, user):
        self.closest_user = None
        self.user_coords = None

        sp = SpotifyManager(user.username)
        playlist_name, playlist_uri = sp.playlist_retrieval()

        try:
            database.add_playlists(user.user_id, user.login_id, playlist_name, playlist_uri)
            print(f"Playlist {playlist_name!r} added to database")
        except:
            print(f"Playlist {playlist_name!r} already exists in database")

    def nearest_user(self, user_coords):
        """Locates the closest other user's Lat/Long coordinates to the user's current location, filtering
        through the array of coordinates with Scipy Spatial.
        """
        coords_list = []
        self.user_coords = user_coords

        user_rows = database.retrieve_user_locations()
        for _, lat, long, _ in user_rows:
            coords_list.append([lat, long])

        coords_array = np.array(coords_list)
        closest_2_coords = coords_array[spatial.KDTree(coords_array).query(self.user_coords, k=2)[1]]

        self.closest_coords = closest_2_coords[1]       # ignores the user's result of being the closest location to themself.
        print("\nClosest coord: ", self.closest_coords)

        for name, lat, long, _ in user_rows:
            if self.closest_coords[0] == lat and self.closest_coords[1] == long:
                self.closest_user = name

        print(f"Closest Spotify User: {self.closest_user}")
        self.open_playlists()


    def open_playlists(self):
        """Returns the closest user's latest public playlist name, playlist URI
         and the time the playlist was added.
         Finally will ask user in a pop-up web browser if ok to open in the Spotify app, otherwise will play the
         playlist in the browser.
         """
        login_timestamp, closest_playlist_name, closest_playlist_uri = database.retrieve_user_playlist(self.closest_user)
        distance_from_user = distance.distance(self.closest_coords, self.user_coords).miles

        print(f"""
    Successfull application Opening playlist {closest_playlist_name!r}
    Added by your neighbour Spotify User {self.closest_user!r}, {distance_from_user:,.2f} miles from your location.
    """)

        webbrowser.open(f"spotify:playlist:{closest_playlist_uri}")
