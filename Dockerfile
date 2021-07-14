FROM python:3.8-buster AS builder
# FROM python:3.7.3


# Setup the virtualenv
RUN python -m venv /venv

# don't write pyc file
ENV PYTHONDONTWRITEBYTECODE 1
# don't buffer log message submission
ENV PYTHONUNBUFFERED 1
# don't check for pip updates
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PATH "/venv/bin:$PATH"

# WORKDIR /quantumapp

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

# install redis
# python3 -m pip install channels_redis
# python3 -m pip install selenium
# RUN docker run -p 6379:6379 -d redis:5

#######################################
# App stage #
# Smaller official Debian-based Python image
FROM python:3.8-slim-buster AS app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PATH "/venv/bin:$PATH"

WORKDIR /usr/src/app

# copy in Python environment
COPY --from=builder /venv /venv

COPY . .

ENV DJANGO_SETTINGS_MODULE=quantumapp.settings
ENV DJANGO_SECRET_KEY "${DJANGO_SECRET_KEY}"

# RUN manage.py collectstatic
# RUN python manage.py makemigrations
# RUN python manage.py migrate

EXPOSE 8000

# ENTRYPOINT [ "python" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
