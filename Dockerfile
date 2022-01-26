FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv --no-cache-dir && pipenv install --dev --system --deploy && pipenv --clear

COPY . /code/
