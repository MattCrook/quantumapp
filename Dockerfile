FROM python:3.7.3


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /api

RUN pip install --upgrade pip

COPY requirements.txt /api/
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=quantumapp.settings
ENV STATIC_ROOT=quantumforum.static


COPY . /api/


# RUN manage.py collectstatic
# RUN python manage.py makemigrations
# RUN python manage.py migrate


EXPOSE 8000
ENTRYPOINT [ "python" ]
CMD [ "manage.py", "runserver", "0.0.0.0:8000"]
