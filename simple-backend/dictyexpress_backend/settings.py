"""
Django settings for dictyexpress_backend project with Resolwe integration.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-development-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'guardian',
    'mathfilters',
    'versionfield',
    'channels',
    
    # Resolwe apps
    'resolwe.storage',
    'resolwe.permissions',
    'resolwe',
    'resolwe.flow',
    'resolwe.toolkit',
    # 'resolwe.elastic',
    
    # Resolwe Bio apps
    'resolwe_bio',
    'resolwe_bio.kb',
    'resolwe_bio.variants',
    
    # Your app
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dictyexpress_backend.urls'

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

WSGI_APPLICATION = 'dictyexpress_backend.wsgi.application'

# Database - Resolwe requires PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'dictyexpress_resolwe'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# Cache configuration (Redis required for Resolwe)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0'),
    }
}

# Celery configuration for async task processing
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')

# Channels configuration for WebSocket support
ASGI_APPLICATION = 'dictyexpress_backend.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')],
        },
    },
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (for Resolwe data storage)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',  # For file uploads
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
     "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
APPEND_SLASH = False

# ===============================
# RESOLWE CONFIGURATION
# ===============================

# Resolwe settings
RESOLWE_HOST_URL = os.environ.get('RESOLWE_HOST_URL', 'http://localhost:8000')

# Flow API host URL (sometimes required as separate setting)
FLOW_API_HOST = os.environ.get('FLOW_API_HOST', 'http://localhost:8000')

# Flow API settings - required by Resolwe (simple configuration)
FLOW_API = {
    'PERMISSIONS': 'api.permissions',
}

# Data storage
FLOW_EXECUTOR = {
    'NAME': 'resolwe.flow.executors.docker',
    'SETTINGS': {
        'CONTAINER_TIMEOUT': 3600,
    },
}
# Resolwe permissions
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Resolwe v44+ storage config (replaces old FLOW_STORAGE / FLOW_DOCKER_MAPPINGS)
RESOLWE_STORAGE = {
    "connectors": {
        "local": {
            "connector": "resolwe.storage.connectors.localconnector.LocalFilesystemConnector",
            "config": {
                # where Resolwe will store data; make sure it exists & is writable
                "path": str(BASE_DIR / "resolwe-storage"),
            },
            "priority": 10,
        },
    },
    "mappings": {
        # logical buckets -> connector(s)
        "data": ["local:"],
        "descriptor": ["local:"],
        "upload": ["local:"],
        "executions": ["local:"],
    },
}

# Anonymous user settings for resolwe.permissions (and align with guardian)
ANONYMOUS_USER_NAME = "anonymous"
GUARDIAN_ANONYMOUS_USER_NAME = "anonymous"  # keep them in sync



# Guardian settings
GUARDIAN_RAISE_403 = False

# Resolwe process resource limits
FLOW_PROCESS_MAX_CORES = 1
FLOW_PROCESS_MAX_MEMORY = 4096  # MB


# Resolwe logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'resolwe': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

