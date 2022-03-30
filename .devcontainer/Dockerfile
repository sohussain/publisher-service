################################
# @author: abdullahrkw
################################
FROM python:3.8-slim-buster

WORKDIR /workspace

RUN apt update &&\
    apt install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pytest==5.4.1 \
                coverage==5.0.4 \
                prometheus_client==0.7.1

RUN pip install paho-mqtt==1.5.0 redis==3.5.3

ENV PYTHONPATH="/workspaces/publisher-tbd:/workspaces/publisher-tbd/config/config_files"

ENV MODE="DEVELOPMENT"

ENV PUBLISHER_ID="cloud_publisher_testing_vscode"

RUN apt-get update &&\
    apt-get install -y mosquitto redis-server
