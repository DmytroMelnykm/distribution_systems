# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.11.1-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc python3-dev musl-dev
RUN apk add --no-cache curl

WORKDIR /lab_1/loggin
RUN python -m venv venv
ENV PATH venv/bin:$PATH
COPY requirments-fast-api.txt /lab_1/loggin/
RUN pip install --upgrade pip
RUN pip install -r requirments-fast-api.txt

COPY /lab_1/loggin /lab_1/loggin/

COPY /lab_1/common_utils /lab_1/loggin/



COPY __init__.py /lab_1/loggin/venv/lib/python3.11/site-packages/hazelcast/__init__.py

ENTRYPOINT ["./entrypoint.sh"]