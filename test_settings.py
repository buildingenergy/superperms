DATABASES = {'default':{
    'NAME':':memory:',
    'TEST_NAME': ':memory:',
    'ENGINE':'django.db.backends.sqlite3'
}}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'organizations',
)

SECRET_KEY = 'Organize the Organizations please'

from django.conf.urls import patterns

urlpatterns = patterns ('',)
