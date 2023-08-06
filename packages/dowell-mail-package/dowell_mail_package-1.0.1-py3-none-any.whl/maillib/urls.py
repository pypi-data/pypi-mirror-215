"""
This module defines the URL patterns for the maillib app.

The urlpatterns list maps URLs to the `home` view functions. There is one URL pattern call to
the path() function, which takes three arguments: the URL pattern, the view
function that should handle the URL, and an optional name for the URL pattern.

urlpatterns = [
    path('', views.home, name='home'),
]

This maps the '' (root) URL to the views.home function, and names the URL pattern
'home'. The name can be used in templates to create links to this URL.

Returns:
        list: A list of URL patterns that map to view functions.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
