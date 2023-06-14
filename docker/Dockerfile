FROM python:3.11.2-slim-bullseye
ENV BOT_NAME = $BOT_NAME
COPY ./src "/usr/src/app/${BOT_NAME}"
COPY ./build/requirements.txt /usr/src/app/${BOT_NAME}
RUN mkdir "/usr/src/app/${BOT_NAME}" & \
    pip install -r "/usr/src/app/${BOT_NAME}/requirements.txt"
WORKDIR "/usr/src/app/${BOT_NAME}"
