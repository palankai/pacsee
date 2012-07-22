# -*- coding: utf-8 -*-
import os
import sys
import socket

gettext = lambda s: s

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SOLUTION_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__),"..",".."))
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

sys.path.append(os.path.join(SOLUTION_PATH,"applications")) 
sys.path.append(os.path.join(SOLUTION_PATH,"vendor")) 

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Budapest'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'hu'

LANGUAGES = (
    ('hu', 'Magyar'),
    ('en', 'English'),
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

USE_X_FORWARDED_HOST = True
PREPEND_WWW = True

SESSION_SAVE_EVERY_REQUEST = False

AUTH_PROFILE_MODULE = None

LOGIN_REDIRECT_URL = "/accounts/profile/"
LOGIN_URL = "/accounts/"
LOGOUT_URL = "/accounts/logout/"


WWW_ROOT = os.path.join(SOLUTION_PATH, "public")

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(WWW_ROOT, "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, "uploads")
FILEBROWSER_DIRECTORY = 'uploads/'

FILEBROWSER_MAX_UPLOAD_SIZE = 10485760
FILEBROWSER_DEFAULT_PERMISSIONS = 0775

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(WWW_ROOT, "static/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"


# Make this unique, and don't share it with anybody.
SECRET_KEY = '9p(i7_=_=*2ya)ns(=7@s#lb@kh2wx980oxt3vp2%ej0&amp;9_q&amp;='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "locale"),
)

AUTHENTICATION_BACKENDS = (
    'xadrpy.auth.backends.EmailBackend',    
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'xadrpy.i18n.middleware.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

ROOT_URLCONF = 'pacsee.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pacsee.wsgi.application'
WSGI_PATH = os.path.join(PROJECT_PATH, "wsgi.py")

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'rosetta-grappelli',
    'rosetta',
    'django.contrib.admin',

    'ckeditor',
    'south',
    'imagekit',

    'xadrpy.vendor.extjs',
    'xadrpy.auth',
    'xadrpy.api',
    'xadrpy.templates',
    
    'xadrpy.router',
    'xadrpy.contrib.pages',
    'xadrpy.contrib.html',
)

GRAPPELLI_ADMIN_TITLE = "Pacsee"
GRAPPELLI_INDEX_DASHBOARD = {
    'django.contrib.admin.site': 'pacsee.dashboard.CustomIndexDashboard',
}

FILEBROWSER_MAX_UPLOAD_SIZE = 10 * 1024 * 1024
FILEBROWSER_DEFAULT_PERMISSIONS = 0775

ROSETTA_MESSAGES_PER_PAGE = 20

ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
BING_APP_ID = None

ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = "en"
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = "English"

ROSETTA_WSGI_AUTO_RELOAD = False

PAGES_DEFAULT_TEMPLATE = "main.html"

PAGES_TEMPLATES = (
    ('main.html', gettext("Main template")),
)


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline','Strike',
              '-', 'Subscript','Superscript',
              '-', 'Link', 'Unlink', 'Anchor',
              '-', 'Maximize',
            ],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            [      'HorizontalRule',
              '-', 'Table',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
              '-', 'SpecialChar',
              '-', 'Source',
              '-', 'About',
            ]
        ],
        'width': 600,
        'height': 300,
        'disableNativeSpellChecker': True,
        'scayt_autoStartup': False,
        'entities' : False,
        'startupOutlineBlocks': True,
        'startupShowBorders': True,
        'format_tags': "h2;h3;p",
        'resize_enabled': False,
        'language': 'hu',
        'toolbarCanCollapse': False,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(SOLUTION_PATH,"local","cache")
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(name)s - %(message)s'
        },
     },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'allfile': {
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(SOLUTION_PATH,"local/logs/all.log"),
            'when': 'd',
            'interval': 1,
            'level': 'DEBUG',               
            'formatter': 'simple',
        },                 
        'debugfile': {
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(SOLUTION_PATH,"local/logs/debug.log"),
            'when': 'd',
            'interval': 1,
            'level': 'DEBUG',               
            'formatter': 'simple',
        },                 
        'infofile': {
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(SOLUTION_PATH,"local/logs/info.log"),
            'when': 'd',
            'interval': 1,
            'level': 'INFO',               
            'formatter': 'simple',
        } 
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['allfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        None: {
            'handlers': ['console', 'debugfile', 'infofile','allfile'],
            'level': 'DEBUG',
            'propagate': True,
        },                
    }
}

try:
    host_settings = __import__( "settings_%s" % socket.gethostname(),globals(), locals(), ['*'] )
    for k in dir(host_settings):
        locals()[k] = getattr(host_settings, k)
except ImportError:
    pass
    
try:
    from settings_local import * #@UnusedWildImport
except ImportError:
    pass
