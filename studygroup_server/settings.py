"""
Django settings for studygroup_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3hgb2+a_%v8k=72-bk)i_^gqqo-y7qyxp#)tfqe!*ey#-w(h93'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'server',
    'rest_framework.authtoken',
    'corsheaders',   
    'debug_toolbar',
    'typedmodels',
    'conversejs',
)

REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES' : (
    #     'rest_framework.renderers.JSONRenderer',
    #     ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),   
    'TEST_REQUEST_DEFAULT_FORMAT' : 'json',
    'TEST_REQUEST_RENDERER_CLASSES' : (
        'rest_framework.renderers.JSNORenderer',
    ), 
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()


ROOT_URLCONF = 'studygroup_server.urls'

WSGI_APPLICATION = 'studygroup_server.wsgi.application'

CONVERSEJS_BOSH_SERVICE_URL = 'http://localhost:5280/http-bind'
CONVERSEJS_AUTO_REGISTER = 'localhost' #127.0.0.1'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'guzelow',
    #     'USER': 'guzelow',
    #     'PASSWORD': 'Study4l!fe',
    #     'HOST': 'guzelow.db.10377017.hostedresource.com',
    # }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "server.Student"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/server.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}