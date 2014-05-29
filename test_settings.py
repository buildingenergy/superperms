DATABASES = {'default':{
    'NAME':':memory:',
    'ENGINE':'django.db.backends.sqlite3'
}}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'organizations',
)

from django.conf.urls import patterns

urlpatterns = patterns ('',)
