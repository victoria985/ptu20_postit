# syntax=docker/dockerfile:1
FROM python:slim-bullseye
WORKDIR /PTU20_POSTIT/postit_viktorija
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
#RUN python manage.py collectstatic --noinput
#RUN python manage.py migrate
#CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "postit_viktorija.wsgi:application" ]
