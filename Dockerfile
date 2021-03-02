FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /quantumapp

RUN pip install --upgrade pip

COPY requirements.txt /quantumapp/
RUN pip install -r requirements.txt

# RUN docker run -p 6379:6379 -d redis:5

COPY . /quantumapp/

# RUN manage.py collectstatic
# RUN python manage.py makemigrations
# RUN python manage.py migrate
