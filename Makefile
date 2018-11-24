install:
	echo "Install"

install-frontend:
	./service/scripts/install-frontend.sh

install-backend:
	./service/scripts/install-backend.sh

create-db:
	./service/scripts/db-create-psql.sh

run-dev: migrate generate-tags
	make run-django

django-migrate: make-migrations migrate

make-migrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

run-django:
	./manage.py runserver

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

