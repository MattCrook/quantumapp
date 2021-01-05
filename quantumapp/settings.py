import os
import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from datetime import timedelta
# import dotenv


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8boax9dercf7r8hfio78yez768j@5+z2x^9)hh!o18__8kt$ft'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
    'allauth.socialaccount',
    'allauth.account',
    'corsheaders',
    'social_django',
    'django_filters',
    'quantumapi',
    'django.contrib.sessions.middleware',
]

# Config/ routing for Websockets/ chat
ASGI_APPLICATION = "quantumapi.views.websockets.routing.application"
CHANNEL_LAYERS = {
  "default": {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
      "hosts": [("127.0.0.1", 6379)],
    },
  },
}


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
]


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# Quantum API - Auth0 Credentials
AUTH0_CLIENT_ID = 'rXCAbUgNjWCbflgAiUU97Uux1eiXUNZu'
AUTH0_DOMAIN = "dev-405n1e6w.auth0.com"
AUTH0_CLIENT_SECRET = 'Xttgkp1Z99NSFJow7Jp2_RNO_MixGlGnwtJhY821KQ7MpVy9DslCddEb_uQamsu7'
API_IDENTIFIER = 'https://api.quantumcoasters.com'
AUTH0_OPEN_ID_SERVER_URL = 'https://dev-405n1e6w.auth0.com/api/v2/users/'


# Auth0 Credentials for Quantum Application
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = 'dev-405n1e6w.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'ouQeFaroORjm08Dp6slPLQaNYri0sNY5'
SOCIAL_AUTH_AUTH0_SECRET = 'moWYcL19X4PtwLFqtRx2QiB5l7KfzUqIM1LZ31rzXjuWNeJx_w1OJqoueYKP_4kx'
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]

# For Testing, to persist session cookies between redirect when redirecting user from login page.
# SESSION_COOKIE_SECURE = True
# # USe with Ngnix configuration
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# CSRF_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False

# Custom User Model - models.User/ views.UserViewset
AUTH_USER_MODEL = 'quantumapi.User'


JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'quantumapi.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'quantumapi.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': API_IDENTIFIER,
    'JWT_ISSUER': 'https://dev-405n1e6w.auth0.com/',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}


AUTHENTICATION_BACKENDS = {
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
}
# FOR DJANGO WEB APP BACKEND
# 'quantumapi.auth0_views.Auth0',


ROOT_URLCONF = 'quantumapp.urls'


CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:3000',
    'http://localhost:3000',
    'http://localhost:8000',
)


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
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quantumcoastersdb',
        'USER': 'matthewcrook',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
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
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


LOGIN_URL = '/login/auth0'
LOGIN_REDIRECT_URL = '/home'
LOGOUT_URL = 'logout/'
LOGOUT_REDIRECT_URL = '/'


# Social Auth Configs
# https://readthedocs.org/projects/python-social-auth/downloads/pdf/latest/
SOCIAL_AUTH_LOGIN_URL = '/authorize'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/complete/auth0'

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = [
    'username', 'first_name', 'last_name', 'email'
]

SOCIAL_AUTH_USER_MODEL = 'quantumapi.User'
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_CLEAN_USERNAMES = True
SOCIAL_AUTH_AUTH0_WHITELISTED_DOMAINS = ['http://127.0.0.1:3000', 'http://localhost:3000', 'http://localhost:8000', ]
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_PIPELINE = (
'social_core.pipeline.social_auth.social_details',
'social_core.pipeline.social_auth.social_uid',
'social_core.pipeline.social_auth.social_user',
'social_core.pipeline.user.get_username',
'social_core.pipeline.social_auth.associate_by_email',
'social_core.pipeline.user.create_user',
'social_core.pipeline.social_auth.associate_user',
'social_core.pipeline.social_auth.load_extra_data',
'social_core.pipeline.user.user_details',
)

# Django All-Auth Settings
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/?verification=1'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/?verification=1'
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'None'
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'None'

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'quantumapi.views.UserSerializer'
    }
# REST_SESSION_LOGIN = True

# Django only sends a cookie if it needs to. If you don’t set any session data, it won’t send a session cookie, unless this is set to true.
SESSION_SAVE_EVERY_REQUEST = True

# When doing dumpdata, specifies fixture dir to put fixture in. *Comment out when running loaddata or will throw error bc it duplicates.
FIXTURE_DIRS = '/Users/matthewcrook/code/nss/frontEnd/quantumapp/quantumapi/fixtures'
