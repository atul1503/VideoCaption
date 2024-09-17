cd /app
poetry run ./manage.py makemigrations
poetry run ./manage.py migrate
poetry run ./manage.py runserver 0.0.0.0:8000