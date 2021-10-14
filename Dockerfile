FROM python:3.8-buster AS builder

# Setup the virtualenv
# RUN python3 -m venv /venv
RUN pip3 install virtualenv
RUN virtualenv venv

# don't write pyc file
ENV PYTHONDONTWRITEBYTECODE 1
# don't buffer log message submission
ENV PYTHONUNBUFFERED 1
# don't check for pip updates
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# Create virtual env for docker container to run python in
ENV PATH "/venv/bin:$PATH"

RUN pip3 install --upgrade pip

COPY requirements.prod.txt .
RUN pip3 install -r requirements.prod.txt --no-cache-dir

# install redis
RUN python3 -m pip install channels_redis
RUN python3 -m pip install selenium
# RUN docker run -p 6379:6379 -d redis:5

#######################################
# App stage #
# Smaller official Debian-based Python image
FROM python:3.8-slim-buster AS app

# ARGS for URLs of the deployed applications. Passed in as arguments when running docker build, or (could..) in docker run:
ARG DEPLOYED_FRONTEND_URI=https://quantum-coasters.uc.r.appspot.com/
# ARG DEPLOYED_BACKEND_URL=http://35.239.130.209

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PATH "/venv/bin:$PATH"

WORKDIR /usr/src/app

# copy in Python environment
COPY --from=builder /venv /venv

ENV DJANGO_SETTINGS_MODULE=quantumapp.settings

# URLs of the deployed applications. Passed in as arguments when running docker build, or docker run:
ENV FRONTEND_URI=$DEPLOYED_FRONTEND_URI
# ENV BACKEND_URL=$DEPLOYED_BACKEND_URL

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
