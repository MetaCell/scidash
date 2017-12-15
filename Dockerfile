FROM python:3

# BUILD VARIABLES

ARG ROOT=/
ARG APP_DIR=/app
ARG GEPPETTO_REPO=https://github.com/openworm/org.geppetto.frontend.git
ARG SCIDASH_EXTENSION_REPO=https://github.com/MetaCell/geppetto-scidash.git
ARG VENV_PATH=/venv
ARG DOTENV_FILE=env-docker
ARG STATIC_DIR=$APP_DIR/static
ARG EXTENSION_DIR=$STATIC_DIR/org.geppetto.frontend/src/main/webapp/extensions

WORKDIR $ROOT

# PYTHON INSTALL
RUN pip install virtualenv
RUN virtualenv -p python3 $VENV_PATH
ENV PATH $VENV_PATH/bin:$PATH
ENV PYTHONUNBUFFERED 1

# CREATING PROJECT FOLDERS

RUN mkdir $APP_DIR

#COPYING PROJECT

WORKDIR $APP_DIR
ADD . $APP_DIR

# INSTALLING REQUIREMENTS

RUN pip install -r $APP_DIR/requirements.txt

# CLONING FRONTEND

RUN mkdir $STATIC_DIR
WORKDIR $STATIC_DIR

RUN git clone $GEPPETTO_REPO
WORKDIR $EXTENSION_DIR
RUN git clone $SCIDASH_EXTENSION_REPO
