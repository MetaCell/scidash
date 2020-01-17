[![Build Status](https://img.shields.io/travis/MetaCell/scidash/master.svg?style=flat-square&label=master)](https://travis-ci.org/MetaCell/scidash)
[![Build Status](https://img.shields.io/travis/MetaCell/scidash/development.svg?style=flat-square&label=develop)](https://travis-ci.org/MetaCell/scidash)
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

We recommend you to use a Python 3 (*3.6 or newer at least*) virtual environment for the installation, so you can keep all the dependencies within that environment.

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

Just a reminder before going forward that this project requires at least a Python 3.6 version, if this requirement is not satisfied before proceeding further ensure you have Python 3.6 (or bigger) installed.

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

#### ***Backend and Fronend Installation***
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

## Deployment

For scidash test deployment there are configurations in deploy folder `$PROJECT_ROOT/service/kubernetes/scidash`

What is what:

`scidash-service.yaml`

This configuration describes kubernetes service ([what is service](https://kubernetes.io/docs/concepts/services-networking/service/)) for scidash deployment.

Section with general information:

```yaml
kind: Service
apiVersion: v1
metadata:
  name: scidash
  namespace: scidash-testing
  labels:
    app: scidash
```

Section with port mappings and other important information:

```
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: scidash
```

This service in general is k8 resource with load balancer which provides access to the open ports from your pods ([what is pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/))

`scidash-deployment.yaml`

This file provides management for deploying (and updating) pod with containers (application container and redis container).

To better understanding you can compare k8 pods with composition created by docker-compose.

Section with general information:

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: scidash
  name: scidash
  namespace: scidash-testing
```

Start of actual specification for deployment:

```
spec:
  replicas: 1 # Count of the similar pods that should by launched
  selector:
    matchLabels:
      app: scidash
  strategy:
    rollingUpdate:
      maxSurge: 50%
      maxUnavailable: 50%
    type: RollingUpdate
```
Containers descriptions start here in template:

```
  template:
    metadata:
      labels:
        app: scidash
    spec:
      containers:

      - image: r.cfcr.io/tarelli/metacell/scidash:deployment
        imagePullPolicy: Always
        name: scidash
        ports:
        - containerPort: 8000 # Ports that should be exposed
          protocol: TCP
```

Also example for environment description. And as you can see here it uses secrets ([what is secret](https://kubernetes.io/docs/concepts/configuration/secret/)) as a source for sensible data.

```
        env:
          - name: DB_USER
            valueFrom:
              secretKeyRef:
                name: scidash-secret
                key: DB_USER
          - name: DB_PASSWORD
            valueFrom:
              secretKeyRef:
                name: scidash-secret
                key: DB_PASSWORD
```
Every secret should be mounted as a volume

```
        volumeMounts:
          - name: scidash-secret
            mountPath: /scidash-secret
```

And described in volumes section on the same level as containers:
```
      volumes:
        - name: scidash-secret
          secret:
            secretName: scidash-secret
```

Also codefresh repository requires especial secret for pulling images:

```
      imagePullSecrets:
      - name: codefresh-generated-r.cfcr.io-cfcr-scidash-testing
```
