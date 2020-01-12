
VENV:=$(shell if [ -d "venv" ]; then echo "venv/bin/"; else echo ""; fi)
PYTHON:=$(VENV)python3
PIP:=$(VENV)/bin/pip
MANAGE:="manage.py"
MANAGECMD=$(PYTHON) $(MANAGE)

install: create-db install-sciunit-neuronunit install-frontend install-backend
	@echo "==========================="
	@echo "=        Finished         ="
	@echo "==========================="

install-sciunit-neuronunit:
	@echo "============================"
	@echo "=  Install sci/neuronunit  ="
	@echo "============================"
	@./service/scripts/install-sciunit-neuronunit.sh

update-sciunit-neuronunit:
	@echo "============================"
	@echo "=  Update sci/neuronunit   ="
	@echo "============================"
	@./service/scripts/update-sciunit-neuronunit.sh

install-frontend:
	@echo "==========================="
	@echo "=    Install frontend     ="
	@echo "==========================="
	@./service/scripts/install-frontend.sh

codefresh-install-frontend:
	@echo "==========================="
	@echo "=    Install frontend     ="
	@echo "==========================="
	@./service/scripts/codefresh-install-frontend.sh

install-backend:
	@echo "==========================="
	@echo "=    Install backend      ="
	@echo "==========================="
	@./service/scripts/install-backend.sh

install-backend-with-env:
	@echo "==========================="
	@echo "=    Install backend      ="
	@echo "==========================="
	@./service/scripts/install-backend.sh -v $(ARGS)

create-db:
	@echo "==========================="
	@echo "=    Create database      ="
	@echo "==========================="
	@./service/scripts/db-create-psql.sh

install-dev:
	@echo "==========================="
	@echo "=    Install dev deps     ="
	@echo "==========================="
	pip install -r requirements-dev.txt

run-dev: migrate
	make run-django & \
	make run-frontend

run-staging: migrate
	make run-django-staging & \
	make run-celery & \
	make run-celery-beat

django-migrate: migrations migrate

migrations:
	$(MANAGECMD) makemigrations

migrate:
	$(MANAGECMD) migrate

superuser:
	$(MANAGECMD) createsuperuser

run-django:
	$(MANAGECMD) runserver

run-django-staging:
	$(MANAGECMD) runserver --insecure 0.0.0.0:8000

run-frontend:
	cd static/org.geppetto.frontend/src/main/webapp/; npm run build-dev-noTest:watch;

run-celery:
	celery -A scidash.main worker -l info --concurrency=5 --maxtasksperchild=20

run-celery-beat:
	celery -A scidash.main beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pidfile=

run-virgo-staging:
	/bin/bash /opt/virgo/bin/startup.sh

manage/%:
	$(MANAGECMD) $*

run-tests: run-django-tests

run-django-tests:
	$(MANAGECMD) test

coverage:
	coverage run $(MANAGE) test
	coverage report -m

lint: flake8-lint isort-lint yapf-lint

format: yapf-format isort-format

flake8-lint:
	flake8 .

isort-lint:
	isort --check-only --diff --recursive .

isort-format:
	isort --recursive .

yapf-format:
	yapf -i -r --style .style.yapf -p -e "*/migrations/*.py" -e "env" -e "*/settings.py" . -e "**/neuronunit/**" -e "**/sciunit/**"

yapf-lint:
	yapf -d -r --style .style.yapf -e "*/migrations/*.py" -e "env" -e "*/settings.py" . -e "neuronunit/**" -e "sciunit/**"

generate-tags:
	ctags -R --exclude=.git --exclude=node_modules --exclude=dist --exclude=env .

build-scidash:
	@echo "==========================="
	@echo "=      Build scidash      ="
	@echo "==========================="
	@./service/scripts/build-image-scidash.sh

build-scidash-db:
	@echo "==========================="
	@echo "=    Build scidash db     ="
	@echo "==========================="
	@./service/scripts/build-image-db.sh

build-virgo:
	@echo "======================="
	@echo "=     Build virgo     ="
	@echo "======================="
	@./service/scripts/build-image-virgo.sh

push-scidash:
	@echo "==========================="
	@echo "=   Push scidash image    ="
	@echo "==========================="
	@./service/scripts/push-image-scidash.sh

push-scidash-db:
	@echo "==========================="
	@echo "=  Push scidash db image  ="
	@echo "==========================="
	@./service/scripts/push-image-scidash-db.sh
%:
    @:
