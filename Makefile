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
	@./service/scripts/install-backend.sh -v

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
	make run-celery-beat & \
	make run-virgo-staging

django-migrate: migrations migrate

migrations:
	./manage.py makemigration

migrate:
	./manage.py migrate

superuser:
	./manage.py createsuperuser

run-django:
	./manage.py runserver

run-django-staging:
	python3.6 manage.py runserver 0.0.0.0:8000

run-frontend:
	cd static/org.geppetto.frontend/src/main/webapp/; npm run build-dev-noTest:watch;

run-celery:
	celery -A scidash.main worker -l info

run-celery-beat:
	celery -A scidash.main beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

run-virgo-staging:
	./service/scripts/run-virgo-staging.sh

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
