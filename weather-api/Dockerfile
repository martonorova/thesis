FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

RUN mkdir /weather-data

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock ./

# RUN pip install --upgrade pip

RUN pip install pipenv && \
    pipenv install

COPY weather_api.py ./

EXPOSE 7000

ENTRYPOINT [ "pipenv", "run", "python", "weather_api.py" ]