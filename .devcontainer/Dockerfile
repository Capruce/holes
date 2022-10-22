FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y git

COPY requirements/ /requirements
RUN pip install -r requirements/dev.txt
