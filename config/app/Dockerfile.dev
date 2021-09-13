FROM python:3.8-slim
LABEL MAINTAINER="Nick Foote"

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/scripts:${PATH}"

COPY ./requirements /requirements

RUN apt-get update && apt-get install -qq -y  \
    libpq-dev libffi-dev netcat gcc postgresql --no-install-recommends \
    libcurl4-openssl-dev libssl-dev python3-dev

# GDAL setup for geospatial data formats
RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin python-gdal python3-gdal 
    
RUN pip3 install --upgrade pip && \
    pip install -r /requirements/requirements.txt && \
    mkdir /app

COPY . /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

# TODO: Add Docker user

CMD ["entrypoint_development.sh"]
