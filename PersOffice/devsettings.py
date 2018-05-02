from .settings import *
import json


config_path = os.path.join(BASE_DIR, 'devconf.json')
with open(config_path, 'r') as f:
    data = json.load(f)
    
SECRET_KEY = data['SECRET_KEY']

DEBUG = True

MIDDLEWARE.remove('django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE.remove('django.middleware.cache.FetchFromCacheMiddleware')
MIDDLEWARE.remove('django.middleware.cache.CacheMiddleware')
del CACHES
#ROOT_URLCONF = 'project.devurls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': data['DB_NAME'],
        'USER': data['DB_USER'],
        'PASSWORD': data['DB_PASSWORD'],
        'HOST': data['HOST'],
        'PORT': data['PORT'],
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')