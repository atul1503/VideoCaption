cd /app
rm -rf /volume/*
cp -r * /volume
poetry run ./manage.py makemigrations
poetry run ./manage.py makemigrations api 
poetry run ./manage.py migrate
poetry run ./manage.py runserver 0.0.0.0:8000