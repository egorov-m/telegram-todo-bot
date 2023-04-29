FROM python:3.11.2-slim-bullseye
ENV BOT_NAME = $BOT_NAME

RUN mkdir /usr/src/app/"${BOT_NAME}"
WORKDIR /usr/src/app/"${BOT_NAME}"

COPY ./src /usr/src/app/"${BOT_NAME}"
COPY ./requirements.txt /usr/src/app/"${BOT_NAME}"
RUN pip install -r /usr/src/app/"${BOT_NAME:}"/requirements.txt
