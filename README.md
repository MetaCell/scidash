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

We recommend you to use a virtual environment for the installation, so you can keep all the dependencies within that environment.

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

**Install SciDash**

```
git clone https://github.com/MetaCell/scidash
cd scidash
make install
```

Also you should create an .env file in the project root, an example can be found in the folder: service/dotenv.

**Configure Database**
Run:
```
# navigate to scidash root folder
cd service/scripts
# impersonate postgres user (may not be necessary depending on your access rights)
su postgres
# run db creation script located in the scidash folder
./db_create_psql.sh
# to return to your shell user only necessary if you used su
logout
make django-migrate
```

## Start the server
```
make run-dev
```

Go to http://localhost:8000/ and enjoy!


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
