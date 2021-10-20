import os
import json
import socket
from dotenv import load_dotenv
from dotenv.main import dotenv_values
load_dotenv()

# config = dotenv_values(".env")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG

# ALLOWED_HOSTS = ['localhost', '8000', '127.0.0.1']
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_jwt',
    'rest_framework_jwt.blacklist',
    'django.contrib.sites',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Included providers for allauth
    # 'allauth.socialaccount.providers.auth0',
    'corsheaders',
    'social_django',
    'django_filters',
    'django.contrib.sessions.middleware',
    'channels',
    'quantumapi',
    'quantumforum',
    'quantumadminapp.apps.QuantumadminappConfig',
    # 'webpack_loader',
]

# Config/ routing for Websockets/ chat
ASGI_APPLICATION = "quantumapp.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# WEBPACK_LOADER = {
#     'DEFAULT': {
#         'BUNDLE_DIR_NAME': '',
#         'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json')
#     }
# }

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # These are set globally, as the global authentication schemes. Can also set on a per view basis.
    # Using authentication_classes = [JSONWebTokenAuthentication]..etc...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.RemoteUserAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# env variables sent through context to templates, redirect to Client React App URLS
REACT_APP_FORUM_URL = os.environ.get('REACT_APP_FORUM_URL')
REACT_APP_HOME = os.environ.get('REACT_APP_HOME')
REACT_APP_USER_PROFILE = os.environ.get('REACT_APP_USER_PROFILE')
CLIENT_URL = 'http://localhost:3000'
FORUM_URL = 'http://localhost:8000/index'
ADMIN_URL = 'http://localhost:8000/quantumadmin/'

# Quantum API - Auth0 Credentials (Management API APP(Test Application))
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')

# Quantum API
API_IDENTIFIER = os.environ.get('API_IDENTIFIER')
QUANTUM_COASTERS_API_ID = os.environ.get('QUANTUM_COASTERS_API_ID')


# Management API
# SCOPES = ['openid', 'profile', 'offline_access', 'name', 'given_name', 'family_name', 'nickname', 'email', 'email_verified', 'picture', 'created_at', 'identities', 'phone', 'address']
# AUTH0_OPEN_ID_USERS_SERVER_URL = os.environ.get('AUTH0_OPEN_ID_USERS_SERVER_URL')
AUTH0_OPEN_ID_SERVER_URL = os.environ.get('AUTH0_OPEN_ID_SERVER_URL')
AUTH0_MANAGEMENT_API_ID = os.environ.get('AUTH0_MANAGEMENT_API_ID')
MANAGEMENT_API_PAYLOAD = json.dumps({
    "client_id": os.environ.get('AUTH0_CLIENT_ID'),
    "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
    "audience": os.environ.get('AUTH0_OPEN_ID_SERVER_URL'),
    "grant_type": "client_credentials"
    })
MANAGEMENT_API_AUTHORIZATION_CODE = json.dumps({
    "client_id": os.environ.get('AUTH0_CLIENT_ID'),
    "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
    "audience": os.environ.get('AUTH0_OPEN_ID_SERVER_URL'),
    "grant_type": "authorization_code"
    })

# AUTHORIZATION_PAYLOAD = os.environ.get('AUTHORIZATION_PAYLOAD')

# Auth0 Credentials for Quantum Application
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = os.environ.get('SOCIAL_AUTH_AUTH0_DOMAIN')

# Quantum Coasters Key
SOCIAL_AUTH_AUTH0_KEY = os.environ.get('SOCIAL_AUTH_AUTH0_KEY')

# Quantum Coasters Secret
SOCIAL_AUTH_AUTH0_SECRET = os.environ.get('SOCIAL_AUTH_AUTH0_SECRET')
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email',
]

# Quantum Coasters Machine to Machine
# AUTH0_MACHINE_TO_MACHINE_CLIENT_ID = os.environ.get('AUTH0_MACHINE_TO_MACHINE_CLIENT_ID')
# AUTH0_MACHINE_TO_MACHINE_DOMAIN = os.environ.get('AUTH0_MACHINE_TO_MACHINE_DOMAIN')
# AUTH0_MACHINE_TO_MACHINE_CLIENT_SECRET = os.environ.get('AUTH0_MACHINE_TO_MACHINE_CLIENT_SECRET')


# For Testing, to persist session cookies between redirect when redirecting user from login page.
# Set to false for dev on localhost
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False


# # Use with Ngnix configuration
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Custom User Model - models.User/ views.UserViewset
AUTH_USER_MODEL = 'quantumapi.User'


JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'quantumapi.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'quantumapi.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': API_IDENTIFIER,
    'JWT_ISSUER': os.environ.get('JWT_ISSUER'),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}


AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'quantumapi.auth0_backend.Auth0',
    'django.contrib.auth.backends.RemoteUserBackend',
    'quantumapi.auth0_backend.QuantumAdminOpenID',
    # Take into account that backends must be defined in AUTHENTICATION_BACKENDS or Django won’t pick them when trying to authenticate the user.
    'social_core.backends.google_openidconnect.GoogleOpenIdConnect',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.open_id_connect.OpenIdConnectAuth'

    # `allauth` specific authentication methods, such as login by e-mail
    # 'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'quantumapp.urls'


CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:3000',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [[os.path.join(BASE_DIR, "quantumadminapp")],],
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'quantumapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3')
        }
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
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
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# For Quantum Coasters React app
LOGIN_URL = os.environ.get('LOGIN_URL')
LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL')
LOGOUT_URL = os.environ.get('LOGOUT_URL')
LOGOUT_REDIRECT_URL = os.environ.get('LOGOUT_REDIRECT_URL')

# QuantumAdminApp
QUANTUMADMIN_REGISTER_URL = os.environ.get('QUANTUMADMIN_REGISTER_URL')

# Social Auth Configs (For Django full stack app)
# https://readthedocs.org/projects/python-social-auth/downloads/pdf/latest/
# https://python-social-auth.readthedocs.io/en/latest/configuration/django.html

# The OpenID backend will check for a username key in the values returned by the server, but default to first-name
# + last-name if that key is missing. It’s possible to indicate the username key in the values If the username is under
# a different key with a setting, but backends should have defined a default value.
# SOCIAL_AUTH_FEDORA_USERNAME_KEY = 'email'

# authorize endpoint in Auth0 backend to authorize user.
SOCIAL_AUTH_LOGIN_URL = os.environ.get('SOCIAL_AUTH_LOGIN_URL')



# Redirect url that Auth0 will redirect to after auth0/complete
SOCIAL_AUTH_LOGIN_REDIRECT_URL = os.environ.get('SOCIAL_AUTH_LOGIN_REDIRECT_URL')
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = os.environ.get('SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL')

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = [
    'username', 'first_name', 'last_name', 'email'
]

SOCIAL_AUTH_USER_MODEL = 'quantumapi.User'
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_CLEAN_USERNAMES = True
# SOCIAL_AUTH_PROTECTED_USER_FIELDS = os.environ.get('SOCIAL_AUTH_PROTECTED_USER_FIELDS')
# SOCIAL_AUTH_AUTH0_WHITELISTED_DOMAINS = os.environ.get('SOCIAL_AUTH_AUTH0_WHITELISTED_DOMAINS')
# SOCIAL_AUTH_AUTH0_WHITELISTED_DOMAINS = os.environ.get('SOCIAL_AUTH_AUTH0_WHITELISTED_DOMAINS')

# SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.debug.debug',
)

# Django All-Auth Settings (SocialAccount)
# https://django-allauth.readthedocs.io/en/latest/configuration.html

SOCIALACCOUNT_PROVIDERS = {
    'auth0': {
        'AUTH0_URL': os.environ.get('SOCIALACCOUNT_DOMAIN'),
    }
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_STORE_TOKENS = True

# Email verification
# https://django-allauth.readthedocs.io/en/latest/views.html#e-mail-verification
# https://django-allauth.readthedocs.io/en/latest/views.html#e-mails-management-account-email
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/?verification=1'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/?verification=1'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = False
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'None'
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'None'

# Used to override forms, for example: {'signup': 'myapp.forms.SignupForm'}
# SOCIALACCOUNT_FORMS = {}

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'quantumapi.views.UserSerializer'
}
REST_SESSION_LOGIN = True

# Django only sends a cookie if it needs to. If you don’t set any session data, it won’t send a session cookie, unless this is set to true.
SESSION_SAVE_EVERY_REQUEST = True

# When doing dumpdata, specifies fixture dir to put fixture in. *Comment out when running loaddata or will throw error bc it duplicates.
FIXTURE_DIRS = '/Users/matthewcrook/code/nss/frontEnd/quantumapp/quantumapi/fixtures'
