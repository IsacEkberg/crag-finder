"""
Django settings for project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/

Environment variables to be set:

___Local dev server___
    --

___Local Docker___
    --

___CircleCI___
DOCKER_USER
DOCKER_PASSWORD
DOCKER_EMAIL

___AWS___


"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Determine the running environment. Used determine other settings.
ON_LOCAL_DOCKER = 'LOCAL_RUNNING_DOCKER' in os.environ  # A docker container running locally.
ON_CIRCLE_DOCKER = 'CIRCLE_RUNNING_DOCKER' in os.environ  # a docker container on CircleCI.

ON_AWS = 'ON_AWS' in os.environ  # A docker container running on AWS.
ON_CIRCLECI = 'CIRCLECI' in os.environ  # Running on circleCI
ON_LOCAL_DEV = False
if (not ON_LOCAL_DOCKER) and (not ON_AWS) and (not ON_CIRCLECI):
    ON_LOCAL_DEV = True  # Running a local django dev server.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+tb*r29ojm&cd4t!q*=&62q-n$9@lid!ct5xf-vq=n8o#q(s-l'

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
    'django_api',
]
if ON_AWS:
    INSTALLED_APPS += [
        "storages"
    ]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_app.urls'

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

WSGI_APPLICATION = 'django_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# Case 1: Running dev server = Iportalen-way
# Case 2: Running local docker = Do sqlite?
# Case 3: CircleCI = Use given test database.
# Case 4: On AWS = Use RDS mysql and env variables.

if ON_LOCAL_DEV:
    try:
        from django_app.dev_settings import DEV_DATABASE  # Don't forget to set credentials!
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': DEV_DATABASE["db_name"],
                'PORT': DEV_DATABASE["port"],
                'HOST': DEV_DATABASE["host"],
                'USER': DEV_DATABASE["user"],
                'PASSWORD': DEV_DATABASE["password"]
            }
        }
    except ImportError:
        print("########FALLING BACK TO SQLITE3, SET YOUR DEV_DATABASE!########")
        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
            }
        }

elif ON_LOCAL_DOCKER or ON_CIRCLE_DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
        }
    }
elif ON_CIRCLECI:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'circle_test',
            'USER': 'ubuntu'
        }
    }
elif ON_AWS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/django_static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "ember_app/dist")]
if ON_LOCAL_DEV or ON_LOCAL_DOCKER:
    STATIC_ROOT = os.path.join(BASE_DIR, "static_content")

elif ON_AWS:
    STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, "../static/"))
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    AWS_PRELOAD_METADATA = True  # Only update files which are modified.

    S3_URL = 'https://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
    STATIC_URL = os.environ.get('STATIC_URL', S3_URL + 'static/')

    DEFAULT_FILE_STORAGE = 'django_app.storage.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'django_app.storage.StaticRootS3BotoStorage'

    MEDIA_URL = os.environ.get('MEDIA_URL', S3_URL + 'client/')

    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

