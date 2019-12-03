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

Python 3.6 virtual environment is required for the installation (3.7+ will break with current django version.), so you can keep all the dependencies within that environment.

**Dependencies**

_Install Redis server (for the sockets communication)_

```
For Ubuntu 16+:
sudo apt-get install redis-server
For OS X:
brew install redis
```

_Install PostgreSQL server_

-   [instructions](https://www.postgresql.org/download/linux/ubuntu/) for Ubuntu
-   [application](https://postgresapp.com/) for MacOS
-   [docker image](https://hub.docker.com/_/postgres) to run in docker.

### **Install SciDash**

#### **_Project root configuration_**

First of all we need to clone the scidash folder from the remote repo, follow the commands below:

```
git clone https://github.com/MetaCell/scidash
cd scidash
```

Once retrieved the data we need to create a .env file in the project root where we are at the moment if you followed the previous commands.
An example can be found in the folder scidash/dotenv/env-docker but you will need to modify this based on your current configuration (e.g. if you want to configure this in your local machine you will need to change DB_HOST from "scidash-postgres" to "localhost", same principle for the other parameters if you want to use different hosts or ports for your deployment).
If you're using docker containers, remember to configure the host names properly.

```
cp service/dotenv/env-docker .env
source .env
```

Or, if you have direnv installed.

```
cp service/dotenv/env-docker .envrc
direnv allow
```

Just a reminder before going forward that this project requires a Python 3.6 version, if this requirement is not satisfied before proceeding further ensure you have Python 3.6 installed.

#### **_Backend and Frontend Installation_**

Since there are different options to install the project dependencies and start coding, you can just run for the bellow command, but, there you can check the other install options on the Makefile.

```
# navigate to scidash root folder
make install
```

If you'd like to verify that all the packages have been correctly installed you can compare the output of the command "pip list" with the file requirements.txt that contains the list of all the packages required.

Once the backend installation is done we can move to the frontend installation:

#### **_Run Scidash_**

##### Start the server

```
make run-dev
```

Go to http://localhost:8000/ and enjoy!

## Requirements to neuronunit test and model classes to work with scidash

> Note: to save compatibility with uploaded results you'll be able to save classes which are not meet requirements, but there is no guarantee that they will work with application

#### **_Model classes requirements_**

Capabilities of the model should be accessible by class method `get_capabilities`

```python
model.get_capabilities()
```

Extra capabilities check should be accessible by class property `extra_capability_checks`

```python
model.extra_capability_checks
```

#### **_Test classes requirements_**

_Observations_

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

_Parameters_

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

_Units_

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
