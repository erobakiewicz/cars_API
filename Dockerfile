FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv --no-cache-dir && pipenv install --dev --system --deploy && pipenv --clear

COPY . /app/
