from django.test import TestCase
from django.urls import reverse, resolve
from maillib.views import home

class TestUrls(TestCase):

    '''
    Test cases for the maillib urls in the maillib Django app's urls.py.

    Methods:
    - test_home_url_resolved: Tests that the call to the `home` url name resolves successfully
    '''
    
    def test_home_url_resolved(self):
        '''
        Tests that the call to the `home` url name resolves successfully
        '''
        url = reverse('home')
        self.assertEquals(resolve(url).func,home)
