
FROM python:3.9-slim-buster

WORKDIR /fastapi-daraja

COPY ./requirements.txt /fastapi-daraja/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi-daraja/requirements.txt

#
COPY ./app /fastapi-daraja/app

