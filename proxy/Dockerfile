FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install

COPY proxy.py ./

EXPOSE 5000

ENTRYPOINT [ "pipenv", "run", "python", "proxy.py" ]