install:
	uv add django gunicorn

migrate:
	uv run python manage.py migrate

tailwind_build:
	uv run python manage.py tailwind build

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi
