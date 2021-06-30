[![Build Status](https://img.shields.io/travis/MetaCell/scidash/master.svg?style=flat-square&label=master)](https://travis-ci.org/MetaCell/scidash)
[![Build Status](https://img.shields.io/travis/MetaCell/scidash/development.svg?style=flat-square&label=develop)](https://travis-ci.org/MetaCell/scidash)
[![Coverage Status](coverage.svg)](https://travis-ci.org/MetaCell/scidash)
<p align="center">
  <img src="http://scidash.github.io/assets/scidash-text.png" alt="SciDash logo"/>
</p>
<p align="center">
    <img src="https://github.com/tarelli/bucket/blob/master/geppetto%20logo.png?raw=true" alt="Geppetto logo"/>
</p>

## SciDash

SciDash is a project that enables the reproducible execution and visualization of data-driven unit test (SciUnit) for assessing model quality.

SciDash is a geppetto / django-based client-server web application.

## Installation with Docker

This installation procedure relies on the use of docker and docker-compose, if you don't have these already installed in your machine you can follow these [link 1](https://docs.docker.com/install/) and [link 2](https://docs.docker.com/compose/install/).

In order to install scidash in your machine you will need to clone the scidash repository

```
git clone https://github.com/metacell/scidash.git
```

Then, we need to access the repository at the folder scidash/service/docker, for instance if you are using linux you can type in your terminal the below:

```
cd ./scidash/service/docker
```

Inside this folder you will find the 3 docker files needed to build and run scidash locally.
Running the 3 commands below we will build 3 docker images that we will re-use through our docker-compose.yml file in order to run scidash. You can now proceed with the 3 commands below to build the 3 images required (note, it might take roughly 1 hour to build all the 3 images and the time can vary depending on your internet connection speed since these steps will have to download other software from the web):

```
docker build -f Dockerfile-postgres -t metacell/scidash_db:my_local_tag .
docker build -f Dockerfile-virgo -t metacell/scidash_virgo:my_local_tag .
docker build -f Dockerfile-scidash -t metacell/scidash:my_local_tag .
```

Once the 3 images have been created we can now move to the deployment folder, on the same level of the current docker folder, for instance in linux we can run:

```
cd ../deployment
```

At this point we need to edit the docker-compose.yml with our favourite editor (vim obviously, unless you are one of those who use emacs, I am sorry for you) and replace the tag with the one used during the manual build.
If you did a copy paste of the commands, you will need to replace the tag latest with the my_local_tag string, for instance:

    image: metacell/scidash_db:latest

will become:

    image: metacell/scidash_db:my_local_tag

Once we finish to edit the file with the correct tag we are ready to run scidash, so sit down, relax and run:

```
docker-compose up -d
```

Wait 1-2 mins that docker compose will bring up all the service and enjoy Scidash!

## Installation in my machine

We recommend you to use a Python 3.6 virtual environment for the installation, so you can keep all the dependencies within that environment.

**Dependencies**

*Install Redis server (for the sockets communication)*
```
For Ubuntu 16:
sudo apt-get install redis-server
For OS X:
brew install redis
```

*Install PostgreSQL server*
- [instructions](https://www.postgresql.org/download/linux/ubuntu/) for Ubuntu
- [application](https://postgresapp.com/) for MacOS

### **Install SciDash**

#### ***Project root configuration***
First of all we need to clone the scidash folder from the remote repo, follow the commands below:

```
git clone https://github.com/MetaCell/scidash
cd scidash
```

Once retrieved the data we need to create a .env file in the project root where we are at the moment if you followed the previous commands.
An example can be found in the folder scidash/dotenv/env-docker but you will need to modify this based on your current configuration (e.g. if you want to configure this in your local machine you will need to change DB_HOST from "scidash-postgres" to "localhost", same principle for the other parameters if you want to use different hosts or ports for your deployment).

```
cp service/dotenv/env-docker .env
source .env
```

As a developer you may add the git pre-commit hook to you .git repo. Besides updating the coverage badge, this hook runs some more commands before committing your changes. To install the pre-commit hook copy the hook to your .git folder

```shell script
cp service/hooks/pre-commit .git
chmod +x .git/hooks/pre-commit
```

You should install the requirements-dev.txt to use the coverage and more code testing tools

```shell script
pip install -r requirements-dev.txt
```

To update the coverage badge manually run
```shell script
make coverage-badge
```

Just a reminder before going forward that this project requires a Python 3.6 version, if this requirement is not satisfied before proceeding further ensure you have Python 3.6 installed.

#### ***Configure Database***
In order to configure the database you need the PostgreSQL server installed as per dependencies listed above, then you can proceed with the steps below that will need to be run as postgres user:

```
# navigate to scidash root folder
cd service/scripts
# impersonate postgres user (may not be necessary depending on your access rights)
sudo su postgres
# run db creation script located in the scidash folder
./db_create_psql.sh
# to return to your shell user only necessary if you used su
logout
```

#### ***Backend and Frontend Installation***
Once done with the database configuration you can proceed with the backend (first) and the frontend (second) installation.
First we start with the backend installation with the command below:
```
# navigate to scidash root folder
make install-backend
```
If you'd like to verify that all the packages have been correctly installed you can compare the output of the command "pip list" with the file requirements.txt that contains the list of all the packages required.

Once the backend installation is done we can move to the fronend installation:
```
# navigate to scidash root folder
make install-frontend
```

#### ***Run Scidash***

##### Start the server
```
make run-dev
```

Go to http://localhost:8000/ and enjoy!


## Requirements to neuronunit test and model classes to work with scidash

> Note: to save compatibility with uploaded results you'll be able to save classes which are not meet requirements, but there is no guarantee that they will work with application

#### ***Model classes requirements***

Capabilities of the model should be accessible by class method `get_capabilities`

```python
model.get_capabilities()
```

Extra capabilities check should be accessible by class property `extra_capability_checks`

```python
model.extra_capability_checks
```

#### ***Test classes requirements***

*Observations*

Should be accessible by class property `observation_schema`

```python
test.observation_schema
```

Supported schema

```python
[(
    "<schema_name>",
    {
        '<observation_field_name>': {<cerberus_validation_schema>},
        ...<other_fields>
    }
), ...<other_schemas>]
```

In case there are more than one schema. And if there is only one

```python
(
    "<schema_name>",
    {
        '<observation_field_name>': {<cerberus_validation_schema>},
        ...<other_fields>
    }
)
```

Iterable observations should have `iterable: True` in validation schema.

*Parameters*

Should be accessible by class property `params_schema`

```python
test.params_schema
```

Supported format

```python
{
    '<param_name>': {<cerberus_validation_schema>},
    ...<other_params>
}
```

Should have `type` property in validation schema

*Units*

Should be accessible with class property `units`

```python
test.units
```

Supported formats

```python
pq.Unit # importable string
```

```python
pq.UnitQuantity('megaohm', pq.ohm*1e6, symbol='Mohm') # custom unit
```

```python
{'v': pq.V, 'i': pq.pA} # mapping
```

## Post install steps

For copying/cloning initial model instances and test instances please update the DEMO_USER_ID in the settings file
to point to the user (id) from where the models and test instances should be cloned.

