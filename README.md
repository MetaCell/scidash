<p align="center">
  <img src="http://scidash.github.io/assets/scidash-text.png" alt="SciDash logo"/>
</p>
<p align="center">
    <img src="https://github.com/tarelli/bucket/blob/master/geppetto%20logo.png?raw=true" alt="Geppetto logo"/>
</p>

## SciDash 

SciDash is a project that enables the reproducible execution and visualization of data-driven unit test (SciUnit) for assessing model quality.

SciDash is a geppetto / django-based client-server web application. 

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

**Install SciDash**

```
git clone https://github.com/MetaCell/scidash
cd scidash
mkdir static
cd static
git clone https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp
npm install
npm run build-dev-noTest
```

**Install SciDash Geppetto Extension**

Clone the Geppetto SciDash extension into the extensions folder 
```
cd org.geppetto.frontend/src/main/webapp/extensions
git clone https://github.com/MetaCell/geppetto-scidash.git
```

Then manually edit [GeppettoConfiguration.json](https://github.com/openworm/org.geppetto.frontend/blob/master/src/main/webapp/GeppettoConfiguration.json) to look like this:
```
{
    "_README" : "http://docs.geppetto.org/en/latest/build.html",
    "contextPath": "org.geppetto.frontend",
    "useSsl": false,
    "embedded": false,
    "embedderURL": ["/"],
    "noTest": false,
    "extensions": {
        "geppetto-default/ComponentsInitialization": false,
        "geppetto-scidash/ComponentsInitialization": true
    },
    "themes": {
        "geppetto-default/colors": false,
        "geppetto-scidash/colors": true,
    }
}
```

**Install Database**

1. Install PostgreSQL server: [instructions](https://www.postgresql.org/download/linux/ubuntu/) for Ubuntu, [application](https://postgresapp.com/) for MacOS
2. Run: 
```
# navigate to scidash root folder
cd scidash  
# impersonate postgres user (may not be necessary depending on your access rights)
su postgres
# run db creation script located in the scidash folder
./db_create_psql.sh
# to return to your shell user only necessary if you used su
logout 
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


