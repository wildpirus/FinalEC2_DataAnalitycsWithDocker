FROM jupyter/minimal-notebook
WORKDIR /datascience
USER root
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    apt-get clean && rm -rf var/lib/apt/list/*
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt