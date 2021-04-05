FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /quantumapi

RUN pip install --upgrade pip

COPY requirements.txt /quantumapi/
RUN pip install -r requirements.txt

COPY . /quantumapi/
