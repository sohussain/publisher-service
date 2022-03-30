################################
# @authors: abdullahrkw, bilalm19
################################
FROM python:3.8-slim-buster as base_image

WORKDIR /workspace

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/workspace:/workspace/config/config_files"

CMD ["python", "publisher/main.py"]

COPY ./ ./
################################################# Test Stage
FROM base_image as testing_stage

ENV MODE="PRODUCTION"

RUN apt-get update &&\
    apt-get install -y mosquitto redis-server

ARG PUBLISHER_ID="test_cloud_publisher"

# RUN py.test --stepwise tests
RUN  coverage run --source='publisher,config' -m py.test tests -o log_cli=True -o log_level=Debug &&\
    coverage report > coverage-report.txt
################################################ x86_64_development
FROM base_image as x86_64_development

ENV MODE="DEVELOPMENT"
############################################## x86_64_production
FROM base_image as x86_64_production

ENV MODE="PRODUCTION"

RUN mkdir artifacts

COPY --from=testing_stage /workspace/coverage-report.txt .
############################################# aarch64_development
FROM base_image as aarch64_development

ENV MODE="DEVELOPMENT"
########################################### aarch64_production
FROM base_image as aarch64_production

ENV MODE="PRODUCTION"

RUN mkdir artifacts

COPY --from=testing_stage /workspace/coverage-report.txt .
