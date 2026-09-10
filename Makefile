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

setup:
	uv sync
	uv run python manage.py migrate
	uv run python manage.py tailwind build
	uv run python manage.py collectstatic --noinput
