FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV APP_DIR=/app
ENV SRC_DIR=${APP_DIR}/src

# TODO: add user

COPY ../requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY ../src ${SRC_DIR}

WORKDIR ${SRC_DIR}
