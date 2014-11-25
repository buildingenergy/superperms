![CircleCI Status][]

[CircleCI Status]: https://circleci.com/gh/buildingenergy/superperms.png?circle-token=25e8d7e5568a06a231161d4bffe8918f8ebb4902


superperms
==========
![HappyTrees](https://dl.dropboxusercontent.com/u/5586906/images/HappyLittleTrees.jpg)



## Install

install superperms

```py
pip install superperms
```

add superperms to your `INSTALLED_APPS`

```py
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admin',
    'south',
    'superperms.orgs',
)
```

Run migrations to create the database tables

```py
python manage.py migrate superperms.orgs
```

Note: if your app uses a custom AUTH_USER_MODEL (a user model that is not django.contrib.auth.User), you will need to create the table for your user before you run the migrations for superperms. You can declare this dependency in the initial migration for the custom user as show below. This is necessary so that superperm organizations can have a foreign key to the custom user model.

```py
class Migration(SchemaMigration):

    needed_by = (
        ('superperms.orgs', '0001_initial'),
    )
```

## Configuration Options

 -  ``ALLOW_SUPER_USER_PERMS``: Allows Django super_user class accounts to bypass permissions checks. This is useful mainly for development, but defaults to ``True``.



## Example Usage

- To limit views to people who have member-level roles and above, you could use the following decorator definiition. Users who are ``viewers`` will recieve a Django ``HttpRequestNotAuthorized`` response (e.g. a 403) without ever executing the code inside the view.


```python

from superperms.orgs.decorators import has_perm #  Imports our decorator factory.

# This view will be protected against anybody whose account is "lower"
# than a member. Default role types include ['owner', 'member', 'viewer'].
@has_perm('requires_member')
def protected_view(request):
    pass

```


## Development and Testing

clone the repo and install requirements

```console
$ git clone git@github.com:buildingenergy/superperms.git
$ mkvirtualenv superperms
(superperms)$ cd superperms
(superperms)$ pip install -r requirements.txt
```

tests should pass, PEP8 is enforced

```console
(superperms)$ ./test.sh
```
