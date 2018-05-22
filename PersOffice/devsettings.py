from .settings import *
import json


config_path = os.path.join(BASE_DIR, 'devconf.json')
with open(config_path, 'r') as f:
    data = json.load(f)
    
SECRET_KEY = data['SECRET_KEY']
DATABASES.pop('report')

DEBUG = True

MIDDLEWARE.remove('django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE.remove('django.middleware.cache.FetchFromCacheMiddleware')
MIDDLEWARE.remove('django.middleware.cache.CacheMiddleware')
del CACHES
#ROOT_URLCONF = 'project.devurls'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')