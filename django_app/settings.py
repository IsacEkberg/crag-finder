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
# TODO: ON_CIRCLE_DOCKER does not enter the circleCI env, run command in circle.yml
ON_AWS = 'ON_AWS' in os.environ  # A docker container running on AWS.
ON_CIRCLECI = 'CIRCLECI' in os.environ  # Running on circleCI
ON_LOCAL_DEV = False
if (not ON_LOCAL_DOCKER) and (not ON_AWS) and (not ON_CIRCLECI):
    ON_LOCAL_DEV = True  # Running a local django dev server.

ADMINS = [('Jonathan Anderson', 'jonathan@cragfinder.se'), ('Isac Ekberg', 'isac@cragfinder.se')]
MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ.get('DJANGO_SECRET_KEY'))

DEBUG = False
if ON_LOCAL_DEV:
    DEBUG = True
ALLOWED_HOSTS = [
    'd28my8itslow12.cloudfront.net',
    '.cragfinder.se',
    'crag-finder-dev.eu-west-1.elasticbeanstalk.com'
]

import requests
EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=1).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)


# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'reversion',
    'django_api',
    'django_filters',
    'pagedown',
    'captcha',
]

SITE_ID = 1

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
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ]
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

if ON_CIRCLECI:
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
else:
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

LANGUAGE_CODE = 'sv-se'  # en-us

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email settings:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # This is a dummy backend which prints emails as a
                                                                  # normal print() statement (i.e. to stdout)
EMAIL_HOST_USER = 'noreply-cragfinder@jonathananderson.se'

DEFAULT_FROM_EMAIL = 'noreply@cragfinder.se'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

if ON_AWS:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/django_static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "ember_app/dist")]
if ON_LOCAL_DEV or ON_LOCAL_DOCKER:
    STATIC_ROOT = os.path.join(BASE_DIR, "static_content")

    MEDIA_URL = "/admin/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

elif ON_AWS:
    STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, "../static/"))
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    AWS_PRELOAD_METADATA = True  # Only update files which are modified.

    S3_URL = 'https://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
    STATIC_URL = os.environ.get('STATIC_URL', S3_URL)

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
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

PAGEDOWN_SHOW_PREVIEW = True
PAGEDOWN_WIDGET_CSS = ('/django_static/pagedown/demo/browser/demo.css', "django_api/pagedown_custom.css",)

ADMIN_TOOLS_MENU = 'django_app.menu.CustomMenu'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'django_app.dashboard.CustomAppIndexDashboard'
ADMIN_TOOLS_INDEX_DASHBOARD = 'django_app.dashboard.CustomIndexDashboard'
