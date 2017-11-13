<p align="center">
  <img src="https://github.com/tarelli/bucket/blob/master/geppetto%20logo.png?raw=true" alt="Geppetto logo"/>
</p>

# Geppetto Django Template
Geppetto Django Template provides a template to develop a Geppetto Instance in Python. This Django application illustrates how to integrate the pygeppetto_server (https://github.com/MetaCell/pygeppetto-django), a module which provides the basic functionality, and establishes the skeleton to customize Geppetto server side.

This template provides a very basic python infrastructure to serve the static content. The static content (JS + HTML) can be found at org.geppetto.frontend (https://github.com/openworm/org.geppetto.frontend) and the same module is reused for the Geppetto Java Version. Note, however, that the python server implementation is a work in progress and some features have not been migrated from Java yet.

## Installation

**Dependencies**
```
pip install pygeppetto-django
```

*Install Redis server (for the sockets communication)*
```
For Ubuntu 16:
sudo apt-get install redis-server
For OS X:
brew install redis
```

**Install Django Template**

```
git clone https://github.com/MetaCell/geppetto-django-template
cd geppetto-django-template
mkdir static
cd static
git clone https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp
npm install
npm run build-dev-noTest
```

## Start the server
```
python manage.py runserver
```

Go to http://localhost:8000/ and enjoy!

## How to develop

Any change you make in the python code will be automatically redeployed by the Django server.

JS/HTML code can be found inside `static/org.geppetto.frontend/src/main/webapp/`. The code needs to be rebuilt with webpack everytime there is a change. The recommended way is to run in `/static/org.geppetto.frontend/src/main/webapp/` this command:
```
npm run build-dev-noTest:watch
```

Additionally, if you want to extend the Geppetto core functionality, have a look at https://github.com/MetaCell/pygeppetto-django repo. README describes how to install pygeppetto_server in development mode and modify the code.

## Features

**How to develop a RESTFUL API**

An example of a very simple REST API is provided together with this skeleton. You will find it at the 'api' folder.

The routing happens at urls.py:
```
from api import views

urlpatterns = [
    ...
    url(r'^api/people/', views.people)
]
```

Inside api.views a very simple webservice answering GET and POST request has been implemented.

This REST API, at the moment, is not connected to any database. If you want to have a database have a look at the 'What is missing?' section below and then follow any tutorial regarding the Django Rest Framework(https://realpython.com/blog/python/django-rest-framework-quick-start/ or https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django are very good options).

**How to extend Geppetto Websockets**

**Integration with pygeppetto-django**
This module implements the basic functionality to start a Python Geppetto Instance. To integrate pygeppetto-django module, the following actions have been performed:

- Add "pygeppetto_server" to your INSTALLED_APPS setting (settings.py) like this::
    ```
    INSTALLED_APPS = [
        ...
        'pygeppetto_server',
    ]
    ```

- Include the pygeppetto_server URLconf in your project urls.py like this::
    ```
    url(r'^', include('pygeppetto_server.urls')),
    ```
- Add routing for the sockest like this:
    ```
    include('pygeppetto_server.routing.server_routing', path=r"^/org.geppetto.frontend/Geppetto"),
    ```
- Add channels and rest framework application to your INSTALLED_APPS setting (settings.py) like this::
    ```
    INSTALLED_APPS = [
        ...
    'channels',
    'rest_framework',
    ]
    ```

**What is missing?**

This skeleton app is not connected to any database but, as it is implemented on top of the Django server, it should be quite simple to integrate any SQL DB. In the settings.py you will find commented out the binding for the sqlite DBS provided by default with Django. These are two links with some useful tips to start with:
https://docs.djangoproject.com/en/1.11/topics/install/#database-installation
https://docs.djangoproject.com/en/1.9/ref/settings/#databases


