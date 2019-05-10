FROM python:3.7-alpine

RUN apk add --no-cache ffmpeg sox jq bash

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

CMD python bot.py
