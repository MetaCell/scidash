install: create-db install-frontend install-backend
	@echo "==========================="
	@echo "=        Finished         ="
	@echo "==========================="

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

run-dev: migrate generate-tags
	make run-django & \
	make run-frontend

django-migrate: make-migrations migrate

make-migrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

superuser:
	./manage.py createsuperuser

run-django:
	./manage.py runserver

run-frontend:
	cd static/org.geppetto.frontend/src/main/webapp/; npm run build-dev-noTest:watch;

lint: flake8-lint isort-lint yapf-lint

format: yapf-format isort-format

flake8-lint:
	flake8 .

isort-lint:
	isort --check-only --diff --recursive .

isort-format:
	isort --recursive .

yapf-format:
	yapf -i -r --style .style.yapf -p -e "*/migrations/*.py" -e "env" -e "*/settings.py" .

yapf-lint:
	yapf -d -r --style .style.yapf -e "*/migrations/*.py" -e "env" -e "*/settings.py" .

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
