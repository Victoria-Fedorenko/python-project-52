install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt || pip install .

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:$$PORT