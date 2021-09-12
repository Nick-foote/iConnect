import time
import geocoder
# from functools import wraps

from spotify_manager import SpotifyManager
import database

USER_MENU = """
Please enter your Spotify username to login
Username: """


class User:
    """Used to create methods for user to interact with Spotify and the database.
    """
    def __init__(self):
        self.username = None
        self.user_id = None
        self.spotify = None
        self.login_id = None

    # @login
    def set_username(self):
        """User to enter their spotify username, which is then used as their login username in this program.
        If the user has not logged into the program before it will ask for age & gender and create a new user + id.
        The app does require the user to already have a Spotify account for use.
        """
        while True:
            self.username = input(USER_MENU)

            try:
                self.spotify = SpotifyManager(self.username)        # *FAILING HERE*
                self.spotify.user_query()
                break
            except:
                print("ERROR: Spotify Username does not exist. Please enter a valid Spotify username.")
                continue

        try:
            self.user_id = database.get_user_id(self.username)[0]
            print(f"Previous User Login details retrieved from iConnect.\nID: {self.user_id} - '{self.username}'")

        except:
            self.add_user()
            print(f"\nSetting up New User.  id: {self.user_id} - '{self.username}'")

        self.login()
        return self.username, self.user_id, self.login_id

    def add_user(self):
        """Adds user information to the database, returning the newly created user_id
        """
        while True:
            age_input = input("Please enter your age: ")

            try:
                age = int(age_input)
                break
            except ValueError:
                print("INVALID AGE. Please enter a number.")

        while True:
            gender_input = input("Please enter your gender (m/f): ")

            if gender_input == 'm' or gender_input == 'M':
                gender = 1
                break
            elif gender_input == 'f' or gender_input == 'F':
                gender = 2
                break
            else:
                print("INVALID ENTRY.")

        self.user_id = database.create_user(self.username, age, gender)
        print("User ID: ", self.user_id)

    def login(self):
        """Logs a timestamp for the user to track the latest location and Spotify playlist
        """
        login_timestamp = time.time()
        self.login_id = database.add_login(self.user_id, login_timestamp)[0]

        # @wraps(orig_func)
        # def wrapper(*args, **kwargs):
        #     return orig_func(*args, **kwargs)
        #
        # return wrapper

    def locate(self):
        """From the user's IP the program locates the Lat & Long coordinates, as well as town/area and country.
        area and county could be used as initial filters to locate closest users for when there are too many to
        compare relative distance quickly
        """
        try:
            user_geo = geocoder.ip('me')
            user_latitude, user_longitude = user_geo.latlng[0], user_geo.latlng[1]
            area, county, country = user_geo.address.split(", ")

            database.add_location(self.user_id, self.login_id, user_latitude, user_longitude, area, county, country)

            user_coords = [user_latitude, user_longitude]
            return user_coords

        except Exception as e:
            print("ERROR: Unable to locate User Location!")
            print(e)