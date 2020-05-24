import os
import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.settings import APISettings
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8boax9dercf7r8hfio78yez768j@5+z2x^9)hh!o18__8kt$ft'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'quantumapi',
    # 'quantumfrontend',
    'cloudinary',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.renderers.JSONRenderer',

    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',

    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

USER_SETTINGS = getattr(settings, 'JWT_AUTH', None)

# Custom Serializers for UserProfile to override Django User model
# REST_AUTH_SERIALIZERS = { 'USER_DETAILS_SERIALIZER':'users.serializers.UserProfileSerializer' }
# AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# Custom User to Override and tie Django user to UserProfile
# AUTHENTICATION_BACKENDS = (
#     'myproject.auth_backends.UserProfileModelBackend',
# )


# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     load_dotenv(ENV_FILE)

# AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
# API_IDENTIFIER = os.environ.get('API_IDENTIFIER')
# PUBLIC_KEY = None
# JWT_ISSUER = None

# if AUTH0_DOMAIN:
#     JWT_ISSUER = 'https://' + AUTH0_DOMAIN + '/'

# JWT_AUTH = {
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#         'auth0authorization.utils.jwt_get_username_from_payload_handler',
#     'JWT_DECODE_HANDLER':
#         'auth0authorization.utils.jwt_decode_token',
#     'JWT_ALGORITHM': 'RS256',
#     'JWT_AUDIENCE': API_IDENTIFIER,
#     'JWT_ISSUER': JWT_ISSUER,
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
# }


JWT_AUTH = {
    'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_PUBLIC_KEY': None,
    # 'JWT_ALGORITHM': 'HS256',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_payload',

    # 'JWT_DECODE_HANDLER':
    #     'rest_framework_jwt.utils.jwt_decode_token',
    'JWT_DECODE_HANDLER':
        'auth0authorization.utils.jwt_decode_token',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_create_payload',

    # 'JWT_PAYLOAD_GET_USERNAME_HANDLER':
    #     'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'auth0authorization.utils.jwt_get_username_from_payload_handler',

    'JWT_PAYLOAD_INCLUDE_USER_ID': True,
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_create_response_payload',
    'JWT_AUTH_COOKIE': None,
    # 'JWT_AUTH_COOKIE': 'quantumapp_token',

    # 'JWT_AUTH_COOKIE_DOMAIN': 'http://localhost:8000',
    'JWT_AUTH_COOKIE_DOMAIN': None,

    'JWT_AUTH_COOKIE_PATH': '/',
    'JWT_AUTH_COOKIE_SECURE': True,
    'JWT_AUTH_COOKIE_SAMESITE': 'Lax',
    'JWT_IMPERSONATION_COOKIE': None,
    'JWT_DELETE_STALE_BLACKLISTED_TOKENS': False,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
]


CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
)


ROOT_URLCONF = 'quantumapp.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quantumapp.wsgi.application'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_ROOT =

CLOUDINARY_URL = "cloudinary://418576712586226:IaXis96Iz93J6NH7PTrU1clKpGM@capstone-project"


cloudinary.config(
    cloud_name="capstone-project",
    api_key="418576712586226",
    api_secret="IaXis96Iz93J6NH7PTrU1clKpGM"
)


# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'JWT_ENCODE_HANDLER',
    'JWT_DECODE_HANDLER',
    'JWT_PAYLOAD_HANDLER',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER',
    'JWT_RESPONSE_PAYLOAD_HANDLER',
    'JWT_GET_USER_SECRET_KEY',
)


api_settings = APISettings(USER_SETTINGS, JWT_AUTH, IMPORT_STRINGS)


# check if settings have valid values
if not isinstance(api_settings.JWT_EXPIRATION_DELTA, datetime.timedelta):  # pragma: no cover

    raise ImproperlyConfigured(
        '`JWT_EXPIRATION_DELTA` setting must be instance of '
        '`datetime.timedelta`')

if not isinstance(
        api_settings.JWT_REFRESH_EXPIRATION_DELTA, datetime.timedelta):  # pragma: no cover

    raise ImproperlyConfigured(
        '`JWT_REFRESH_EXPIRATION_DELTA` setting must be instance of '
        '`datetime.timedelta`')
