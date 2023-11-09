FROM python:3.10.12

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /api

COPY requirements.txt /api/
RUN pip install -r /api/requirements.txt

COPY . /api
WORKDIR /api