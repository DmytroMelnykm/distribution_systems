# syntax=docker/dockerfile:1

# pull official base image
FROM hazelcast/hazelcast:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /lab_1/loggin
COPY /lab_1/loggin /lab_1/loggin/


RUN python -m venv venv
ENV PATH venv/bin:$PATH

RUN pip install --upgrade pip
RUN pip install -r requirments-fast-api.txt
EXPOSE 8011/TCP
ENTRYPOINT ["./entrypoint.sh"]