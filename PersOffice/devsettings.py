
from .settings import *
import json


with open(os.path.join(BASE_DIR, 'devconf.json'), 'r') as f:
    DATA = json.load(f)


CSRF_COOKIE_SECURE = False
SECRET_KEY = DATA['SECRET_KEY']

DATABASES.pop('report')
#DATABASES.pop('default')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATA['DB_NAME_DEFAULT'],
        'USER': DATA['DB_USER_DEFAULT'],
        'PASSWORD': DATA['DB_PASSWORD_DEFAULT'],
        'HOST': DATA['HOST_DEFAULT'],
        'PORT': DATA['PORT_DEFAULT'],
    }
}

ALLOWED_HOSTS.append('localhost')

DEBUG = True

MIDDLEWARE.remove('django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE.remove('django.middleware.cache.FetchFromCacheMiddleware')
MIDDLEWARE.remove('django.middleware.cache.CacheMiddleware')
del CACHES
#ROOT_URLCONF = 'project.devurls'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')