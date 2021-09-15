FROM python:3.7.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /quantumforum

RUN pip install --upgrade pip

COPY requirements.txt /quantumforum/

RUN pip install -r requirements.txt

COPY . /quantumforum/
