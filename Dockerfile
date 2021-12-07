FROM python:3.8.5

WORKDIR /code

COPY . .

RUN apt-get update -y && apt-get upgrade -y &&\
    apt-get install -y gdal-bin libgdal-dev &&\
    apt-get install -y python3-gdal &&\
    apt-get install -y binutils libproj-dev

RUN pip3 install -r requirements.txt

CMD gunicorn matchmaker.wsgi:application --bind 0.0.0.0:8000