django-custom-auth
==================

Implements email based login with Django >= 1.5.

# Installation
pip install django-custom-auth

# Add this to your settings
INSTALLED_APPS += (
    'custom_auth',
)

AUTHENTICATION_BACKENDS = ('custom_auth.auth.Authenticate',)  
AUTH_USER_MODEL = 'custom_auth.User'

# URLs

url(r'^accounts/', include('custom_auth.urls')),

# Utilization in your models
user = models.ForeignKey(settings.AUTH_USER_MODEL)

# To access the user model
from django.contrib.auth import get_user_model
