django-custom-auth
==================

Implements email based login with Django 1.5.

# Installation
pip install git+https://github.com/endthestart/django-custom-auth#egg=django-custom-auth

# Add this to your settings
AUTHENTICATION_BACKENDS = ('custom_auth.auth.Authenticate',)  
AUTH_USER_MODEL = 'custom_auth.User'

# In your models you reference a User like this
user = models.ForeignKey(settings.AUTH_USER_MODEL)

# In your models you reference a User like this
from custom_auth.models import User
