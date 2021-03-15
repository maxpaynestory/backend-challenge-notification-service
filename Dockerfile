FROM python:3.6.10

RUN mkdir app

COPY . /app

WORKDIR app

RUN pip install -r requirements.txt