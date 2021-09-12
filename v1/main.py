import database
from spotify_connection import SpotifyConnection
from user import User


class App:
    """Automatically logins user with their Spotify username.
    Locates user location with geopy. Stores all data in a PostGreSQL database.
    Finally locates the closest user to the current user and opens their playlist.
    """

    def __init__(self):
        database.create_tables()

    def run(self):
        user = User()
        user.username, user.user_id, user.login_id = user.set_username()

        user.coords = user.locate()

        spconn = SpotifyConnection(user)
        spconn.nearest_user(user.coords)


# -- Running App --

app = App()

if __name__ == "__main__":
    app.run()
