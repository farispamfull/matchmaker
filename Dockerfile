FROM python:3.8.5

WORKDIR /code

COPY . .

RUN pip3 install -r requirements.txt

CMD gunicorn matchmaker.wsgi:applfication --bind 0.0.0.0:8000