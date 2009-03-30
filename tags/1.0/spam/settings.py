# Django settings for spam project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Arjan', 'arjan@scherpenisse.net'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'bluespam'             # Or path to database file if using sqlite3.
DATABASE_USER = 'mobile'             # Not used with sqlite3.
DATABASE_PASSWORD = 'mvn01'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# laptop
#MEDIA_ROOT = '/home/arjan/devel-linux/spam/trunk/spam/media/'
# zeus
#MEDIA_ROOT = '/home/arjan/devel/code/spam/trunk/spam/media/'
# onsignal-1
#MEDIA_ROOT = '/home/arjan/devel-linux/spam/trunk/spam/media/'
# mvn
MEDIA_ROOT = '/opt/spam/tags/1.0/spam/media/'


# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'adsf3322=872kd_1t*c4b11$sp_@8w26xqsh3-4wqd3s+12x218c^)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'spam.urls'

TEMPLATE_DIRS = (
    # laptop
    #"/home/arjan/devel-linux/spam/trunk/spam/site/templates"
    # zeus
    #"/home/arjan/devel/code/spam/trunk/spam/site/templates"
    # onsignal-1
    #"/home/arjan/devel/code/spam/trunk/spam/site/templates"
    # mvn
    "/opt/spam/tags/1.0/spam/site/templates"
    
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'spammer',
)
