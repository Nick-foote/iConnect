import os
from dotenv import load_dotenv

# /Users/nickfoote/Desktop/PycharmProjects/iConnect/project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # THIRD PARTY
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'leaflet',
    
    # SOCIAL-AUTH
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    
    # LOCAL APPS
    'core',
    'users',
    'playlists',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates/',
            'templates/accounts/login',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # drf_social_oauth2
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', 'postgres')
# CURRENTLY POSTGRES
if DATABASE_ENGINE == 'AWS_RDS':
    pass
else:
    DATABASES = {
        'default': {
            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': os.environ.get('DB_HOST'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'PORT': os.environ.get('DB_PORT', 5432),
            'ATOMIC_REQUESTS': True
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Collectstatic files to
STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = 'web/media'

# Collect static from
STATICFILES_DIRS = (
    '/app/web/static',
)

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/'
# LOGIN_REDIRECT_URL = '/logged-in'
LOGOUT_REDIRECT_URL = '/logged-out'

# If over-riding process
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/users/me/'

# ----------------------------------------------------------------------------
#  --  Social Authentication  --

SOCIAL_AUTH_URL_NAMESPACE = 'social'

AUTHENTICATION_BACKENDS = (
    'drf_social_oauth2.backends.DjangoOAuth2',
    'social_core.backends.spotify.SpotifyOAuth2',
    'django.contrib.auth.backends.ModelBackend'   
)

SOCIAL_AUTH_USER_FIELDS = (
    'email',
    'username',
    'first_name',
    'last_name',
    'password',
)

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write Scope',
        'groups': 'Access to your groups',
    },
    "ACCESS_TOKEN_EXPIRE_SECONDS": 7 * 24 * 60 * 60,
}

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',

    # connect social accounts by email & prevent duplicate accounts
    'social_core.pipeline.social_auth.associate_by_email',

    # over-write original
    # 'user.social_auth.social_account.create_social_user_setup',

    # WIP: Save user detail to Profile & Avatar
    # 'user.social_auth.social_account.save_extra_profile',

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Mobile API Setup - Internal application 
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")



# DOMAIN_ADDRESS = os.environ.get("DOMAIN_ADDRESS")
# spotify_redirect_uri = f'{DOMAIN_ADDRESS}/callback'

# spotify_redirect_uri = "http://127.0.0.1:8000/social/complete/spotify/"
spotify_redirect_uri = "http://127.0.0.1:8000/my-redirect/"
scope = ['user-read-email','user-library-read']

# SOCIAL_AUTH_SPOTIFY_SCOPE = scope
SOCIAL_AUTH_SPOTIFY_KEY = os.environ.get("SPOTIFY_CLIENT_ID")
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")




social_auth_login_for_spotify = """
    https://accounts.spotify.com/en/login?
    continue=https:%2F%2Faccounts.spotify.com%2Fauthorize%3F
    client_id%3D9f660f6108d44080b18f15b3eda4a432%26
    redirect_uri%3Dhttp%253A%252F%252F127.0.0.1%253A8000%252Fsocial%252Fcomplete%252Fspotify%252F%26
    state%3DPua2w1KmaXJYhG5J9vuJez5TMMPyqsty%26
    response_type%3Dcode
"""

fb_redirect = """
https://www.facebook.com/v7.0/dialog/oauth?
client_id=174829003346&
state=AQD0a%2FInADovwsKdigcIsX%2Fsv%2FtymvAZCdGpi6KGpI%2FGyraeljBRqZdpRMglULUY0rVxpazHVzD4GrrFTbWBDC7RJX8qrrCZACUjm58bqUkOdwtZg%2FCa02HU25wdbmRR8EQY08Ky5zANfV4cqQm6T2l8TPlC6hjelk056o55VZs2%2Fqp%2FSB95UHGxOmpzFLy6zKKRXfJ6bSlnbSUAjUZfsgo9fvVbo3u8g57Im5qNXwdKMk7%2FMsLqDVJhqwCsI7oWtpLk%2FHA2LlltkON9UcQfeyQYx6m382btbl394A6sE4quNU3SleGrCHgkloe7%2B9ReKJasXZK%2BLarQEIgmfdQBiiglnw4NuFj3CujqbuQ6jCbx9P7kQuKVwFd5aXEBsag6kMUl7mI%2FaJnpW%2FI48RJAQ17Lt5E8MnWogMOPWYazTVxdzsQd3llhwuj5yoE2Cy6fs%2FeB7%2FgPThTXXkCkYnJYpFrrzhGJ0dpjdOoCLlxNUk%2FDwekCS%2B4SiA%3D%3D&
redirect_uri=https%3A%2F%2Faccounts.spotify.com%2Flogin%2Ffacebook%2Fredirect
"""

unsure = """
https://accounts.spotify.com/en/login/facebook?continue=https%3A%2F%2Faccounts.spotify.com%2Fauthorize%3Fclient_id%3D9f660f6108d44080b18f15b3eda4a432%26redirect_uri%3Dhttp%253A%252F%252F127.0.0.1%253A8000%252Fsocial%252Fcomplete%252Fspotify%252F%26state%3DPua2w1KmaXJYhG5J9vuJez5TMMPyqsty%26response_type%3Dcode"""



# ----------------------------------------------------------------------------
#  --  Leaflet & GeoDjango  --

LEAFLET_CONFIG = {
    # 'DEFAULT_CENTER': (-0.12, 51.51),                   # London coords
    'DEFAULT_CENTER': (51.51, -0.12),                   # London coords
    'DEFAULT_ZOOM': 8,
    'MAX_ZOOM': 20,
    'SCALE': 'both',                                    # Could fix to only miles
    'ATTRIBUTION_PREFIX': 'API-Music Playlists Map',

}