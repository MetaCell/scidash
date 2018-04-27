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
pip install -r requirements.txt
mkdir static
cd static
git clone https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp
npm install
npm run build-dev-noTest
```
Optional for development to enable dynamic refresh of client code when editing html/js/css:
```
npm run build-dev-noTest:watch
```

Also you should create an .env file in the project root, an example can be found in the folder: deploy/dotenv.

**Install SciDash Geppetto Extension**

Clone the Geppetto SciDash extension into the extensions folder
```
cd org.geppetto.frontend/src/main/webapp/extensions
git clone https://github.com/MetaCell/geppetto-scidash.git
```

Then edit [GeppettoConfiguration.json](https://github.com/openworm/org.geppetto.frontend/blob/master/src/main/webapp/GeppettoConfiguration.json) to look like this:
```
{
	"_README": "http://docs.geppetto.org/en/latest/build.html",
	"contextPath": "org.geppetto.frontend",
	"useSsl": false,
	"embedded": false,
	"embedderURL": ["/"],
	"rootRedirect": "",
	"noTest": false,
	"extensions": {
		"geppetto-default/ComponentsInitialization": false,
		"geppetto-scidash/ComponentsInitialization": true
	},
	"themes": {
		"geppetto-default/colors": false,
		"geppetto-scidash/styles/colors": true
	},
	"properties": {
		"title": "SciDash",
		"description": "SciDash is a project that enables the reproducible execution and visualization of data-driven unit test for assessing model quality.",
		"type": "website",
		"url": "http://scidash.github.io/",
		"icon": "http://scidash.github.io/assets/icons/favicon-32x32.png",
		"image": "http://scidash.github.io/assets/scidash-text.png"
	}
}
```

**Install Database**

1. Install PostgreSQL server: [instructions](https://www.postgresql.org/download/linux/ubuntu/) for Ubuntu, [application](https://postgresapp.com/) for MacOS
2. Run:
```
# navigate to scidash root folder
cd deploy/scripts
# impersonate postgres user (may not be necessary depending on your access rights)
su postgres
# run db creation script located in the scidash folder
./db_create_psql.sh
# to return to your shell user only necessary if you used su
logout
./manage.py migrate
```

## Start the server
```
python manage.py runserver
```

Go to http://localhost:8000/ and enjoy!
