#!/bin/bash

cd /volume
cp -r /app/api /app/videocaption /app/manage.py /app/build /app/media .
python3 manage.py makemigrations
python3 manage.py makemigrations api 
python3 manage.py migrate
gunicorn -w 3 -b 0.0.0.0:8000 videocaption.wsgi:application
#python3 manage.py runserver 0.0.0.0:8000