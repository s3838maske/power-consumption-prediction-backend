"""
Django settings for power consumption prediction project.
Production-ready for Railway (MongoDB, WhiteNoise, secure defaults).
"""

import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security — SECRET_KEY must be set in production (Railway env)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# DEBUG — False in production; set DEBUG=0 or leave unset on Railway
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS — Railway and local; set ALLOWED_HOSTS in Railway for your *.railway.app domain
_allowed = config('ALLOWED_HOSTS', default='.railway.app,localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'apps.authentication',
    'apps.users',
    'apps.devices',
    'apps.categories',
    'apps.consumption',
    'apps.predictions',
    'apps.alerts',
    'apps.reports',
    'apps.admin_panel',
]

AUTH_USER_MODEL = 'authentication.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

APPEND_SLASH = False

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

WSGI_APPLICATION = 'config.wsgi.application'

# ——— Database: MongoDB (Railway MONGO_URL or MONGODB_URI) ———
# Railway MongoDB plugin exposes MONGO_URL; fallback to MONGODB_URI for local/Render.
MONGO_URL = os.environ.get('MONGO_URL') or config('MONGODB_URI', default=None)
MONGODB_NAME = config('MONGODB_NAME', default='power_consumption_db')

if MONGO_URL:
    # Production: single URI (Railway); options in URI to avoid Djongo compatibility issues
    # Short timeouts help cold start on Railway free tier
    _uri = MONGO_URL.strip()
    _suffix = 'retryWrites=true&w=majority&connectTimeoutMS=10000&serverSelectionTimeoutMS=10000'
    if '?' in _uri:
        _uri = f'{_uri}&{_suffix}' if not _uri.endswith('&') else f'{_uri}{_suffix}'
    else:
        _uri = f'{_uri}?{_suffix}'
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': MONGODB_NAME,
            'CLIENT': {
                'host': _uri,
            }
        }
    }
else:
    # Local / dev: individual host, port, auth
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': MONGODB_NAME,
            'CLIENT': {
                'host': config('MONGODB_HOST', default='localhost'),
                'port': int(config('MONGODB_PORT', default=27017)),
                'username': config('MONGODB_USER', default=''),
                'password': config('MONGODB_PASSWORD', default=''),
            }
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ——— Static files (WhiteNoise for Railway) ———
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', default=30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(config('JWT_REFRESH_TOKEN_EXPIRE_DAYS', default=7))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': config('JWT_ALGORITHM', default='HS256'),
    'SIGNING_KEY': config('JWT_SECRET_KEY', default=SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS — include Railway and frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://power-consumption-ai-prediction.vercel.app",
]
# Allow any *.railway.app origin (add exact URL in production if preferred)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://[\w\-]+\.railway\.app$",
]
CORS_ALLOW_CREDENTIALS = True

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# ML Models path — .pkl files loaded once globally via apps.consumption.ml_loader
ML_MODELS_PATH = os.path.join(BASE_DIR, 'ml_models')

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
