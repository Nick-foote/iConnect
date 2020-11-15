import psycopg2

PG_URL = "postgres://vxkyuztm:ceAbaeB1wa_qXyTY-GY3cc9-F1eDvOok@kandula.db.elephantsql.com:5432/vxkyuztm"
connection = psycopg2.connect(PG_URL)

# -- SQL Statements --

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS users
    (id SERIAL PRIMARY KEY,
    username TEXT,
    age INTEGER,
    gender TEXT
);"""
#  Other data could be date_created, date_updated

CREATE_LOGIN_TABLE = """
    CREATE TABLE IF NOT EXISTS login
    (id SERIAL PRIMARY KEY,
    user_id INTEGER,
    login_timestamp INTEGER, 
    FOREIGN KEY (user_id) REFERENCES users (id)
);"""
# updates address to latest login or creates new entries each time??

CREATE_LOCATION_TABLE = """
    CREATE TABLE IF NOT EXISTS location
    (id SERIAL PRIMARY KEY,    
    user_id INTEGER,
    login_id INTEGER,
    latitude FLOAT,
    longitude FLOAT,
    area TEXT ,
    county TEXT,
    country TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (login_id) REFERENCES login (id)
);"""
# updates address to latest login or creates new entries each time??

CREATE_PLAYLISTS_TABLE = """
    CREATE TABLE IF NOT EXISTS playlists
    (id SERIAL PRIMARY KEY,
    user_id INTEGER,
    login_id INTEGER,
    playlist_name TEXT,
    playlist_uri TEXT UNIQUE, 
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (login_id) REFERENCES login (id)
);"""


INSERT_USER = "INSERT INTO users (username, age, gender) VALUES (%s, %s, %s) RETURNING id;"

INSERT_LOGIN_RETURNING_ID = "INSERT INTO login (user_id, login_timestamp) VALUES (%s, %s) RETURNING id;"

INSERT_LOCATION = "INSERT INTO location (user_id, login_id, latitude, longitude, area, county, country) VALUES (%s, %s, %s, %s, %s, %s, %s);"

INSERT_PLAYLIST = "INSERT INTO playlists (user_id, login_id, playlist_name, playlist_uri)  VALUES (%s, %s, %s, %s);"


GET_USER_ID = "SELECT id FROM users WHERE username = %s;"

GET_USER_LATEST_LOCATION = "SELECT * FROM location WHERE user_id = %s ORDER BY login_timestamp DESC LIMIT 1;"

# GET_OTHER_USERS_AREA = ""

# GET_OTHER_USERS_COUNTY = ""

# GET_OTHER_USERS_COUNTRY = ""


GET_USER_PLAYLIST = """
    SELECT login_timestamp, playlist_name, playlist_uri FROM users 
    JOIN login ON users.id = login.user_id
    JOIN playlists ON users.id = playlists.user_id
    WHERE username = %s
    ORDER BY login_timestamp DESC LIMIT 1
;"""

USER_LOC_LOOKUP = """
    SELECT DISTINCT ON (username) username, latitude, longitude, login_timestamp FROM users 
    JOIN location ON users.id = location.user_id
    JOIN login ON users.id = login.user_id
;"""

RECALL_LOGIN_ENTRIES = """
    SELECT username, latitude, longitude, login_timestamp FROM users 
    JOIN location ON users.id = location.user_id
    JOIN login ON users.id = login.user_id
;"""

UPDATE_USERNAME = """
    UPDATE users
    SET username = %s
    WHERE id = %s
;"""

UPDATE_lATITUDE = """
    UPDATE location
    SET latitude = %s WHERE login_id = %s
;"""

UPDATE_lONGITUDE = """
    UPDATE location
    SET longitude = %s WHERE login_id = %s
;"""

DELETE_lONGITUDE = """
    DELETE FROM location
    WHERE id = %S
;"""


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_LOGIN_TABLE)
            cursor.execute(CREATE_LOCATION_TABLE)
            cursor.execute(CREATE_PLAYLISTS_TABLE)


def create_user(username: str, age: int, gender: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username, age, gender))
            user_id = cursor.fetchone()[0]     # returns (4,) without [0]
            return user_id


def get_user_id(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_ID, (username, ))
            user_id = cursor.fetchone()
            return user_id


def add_login(user_id: int, login_timestamp: float):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_LOGIN_RETURNING_ID, (user_id, login_timestamp))
            login_id = cursor.fetchone()
            return login_id


def add_location(user_id: int, login_id: int, latitude: float, longitude: float, area: str, county: str, country: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_LOCATION, (user_id, login_id, latitude, longitude, area, county, country))


def add_playlists(user_id: int, login_id: int, playlist_name: str, playlist_uri: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_PLAYLIST, (user_id, login_id, playlist_name, playlist_uri))


def retrieve_user_locations():
    """Gets all login locations + times.
    Returns all data on the last login for username, latitude, longitude.
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(USER_LOC_LOOKUP)
            return cursor.fetchall()


def retrieve_user_playlist(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_PLAYLIST, (username, ))
            return cursor.fetchone()


def view_all_logins():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(RECALL_LOGIN_ENTRIES)
            return cursor.fetchall()


def update_username(new_username: str, user_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_USERNAME, (new_username, user_id))
