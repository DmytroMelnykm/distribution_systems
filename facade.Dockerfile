# syntax=docker/dockerfile:1

# pull official base image
FROM python:3.11.1-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc python3-dev musl-dev

WORKDIR /lab_1/facade
COPY /lab_1/facade /lab_1/facade/
COPY requirments-fast-api.txt /lab_1/facade/
COPY /lab_1/common_utils /lab_1/facade/

RUN python -m venv venv
ENV PATH venv/bin:$PATH

RUN pip install --upgrade pip
RUN pip install -r requirments-fast-api.txt

COPY __init__.py /lab_1/facade/venv/lib/python3.11/site-packages/hazelcast/__init__.py

EXPOSE 8015/TCP
ENTRYPOINT ["./entrypoint.sh"]