import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1", 
    "localhost", 
    "iconnect",
    ]

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
    'social_django.middleware.SocialAuthExceptionMiddleware',
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
    DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('RDS_ENDPOINT'),
        'NAME': os.environ.get('RDS_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'PORT': os.environ.get('RDS_PORT', 5432),
    }
}
else:
    DATABASES = {
        'default': {
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
DATA_UPLOAD_MAX_MEMORY_SIZE = None


# ----------------------------------------------------------------------------
#  --  Social Authentication  --

LOGIN_URL = '/'

# If over-riding process
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/api/v1/accounts/login/'

# SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'

AUTHENTICATION_BACKENDS = (
    'drf_social_oauth2.backends.DjangoOAuth2',
    'social_core.backends.spotify.SpotifyOAuth2',
    'django.contrib.auth.backends.ModelBackend',
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
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Mobile API Setup - Internal application 
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


spotify_redirect_uri = "http://127.0.0.1:8000/my-redirect/"
scope = ['user-read-email', 'user-library-read']

SOCIAL_AUTH_SPOTIFY_KEY = os.environ.get("SPOTIFY_CLIENT_ID")
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SOCIAL_AUTH_SPOTIFY_SCOPE = scope
SOCIAL_REDIRECT_URL = spotify_redirect_uri


# ----------------------------------------------------------------------------
#  --  Leaflet & GeoDjango  --

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (51.51, -0.1),                   # London
    'DEFAULT_ZOOM': 8,
    'MAX_ZOOM': 20,
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'API-Music Playlists Map',
}