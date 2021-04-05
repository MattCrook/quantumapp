#!/bin/bash


# python manage.py runserver
# docker run -it -d -p 8000:8000 application
# docker run -it -d -p 8000:8020 application
# docker exec -it 571516d84688de77173d7f1f35d4c7df6edf10779e63b9d34539e78777fbe0bd /bin/sh

cd quantumadminapp && npm install && npm run watch
cd ..
python manage.py.runserver 0.0.0.0:8000
