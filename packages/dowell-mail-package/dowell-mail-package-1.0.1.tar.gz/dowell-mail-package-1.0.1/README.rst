=================
DOWELL MAIL APP
=================

This is a django mail package consuming the Dowell Mail API. It validates each email then sends email once validated.

QUICK START
============

1. Add `maillib` to your INSTALLED_APPS in settings.py like this:

    INSTALLED_APPS = [ 
        ... 
        'maillib', 
    ]

2. Add `import os` then edit TEMPLATES to include `os.path.join(BASE_DIR, 'templates')` in DIRS like: 

    "DIRS" : [ 
        os.path.join(BASE_DIR, 'templates') 
    ]

3. Include maillib URLconf in the projects url.py like this: 

    path('mail', include('maillib.urls')), 

4. The package doesnt have any database so no migrations are necessary

5. Start the server and navigate to `http://127.0.0.1:8000/mail` and start sending emails!

=========
FEATURES
=========

Dowell Mail offers a reliable and user-friendly API for sending and validating emails. Our API services 
provide a seamless experience for sending emails from your own email ID and validating email addresses for 
accuracy. Whether you need to send important notifications or verify email addresses, Dowell Mail API has 
got you covered.

To understand the API calls and their functionality, I recommend reading the documentation. The documentation 
provides comprehensive information on making API requests and utilizing the available endpoints. It explains 
the required parameters, request methods, and response formats for each API call.
