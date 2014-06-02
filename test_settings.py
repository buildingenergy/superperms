DATABASES = {'default':{
    'NAME':':memory:',
    'ENGINE':'django.db.backends.sqlite3'
}}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'superperms',
)

SECRET_KEY = 'Organize the Organizations please'

from django.conf.urls import patterns

urlpatterns = patterns ('',)
